# app/features/alerts/monitor.py
#
# Responsabilidad: ejecutar el ciclo completo de monitorización para una
# alerta concreta. Esta función es invocada por APScheduler según la
# cron_expression almacenada en cada alerta.
#
# Flujo de ejecución:
#   1. Cargar la alerta y sus descriptores desde BD.
#   2. Obtener todos los canales RSS relevantes (de la categoría de la alerta).
#   3. Para cada canal, descargar y parsear el feed (fetcher).
#   4. Filtrar las noticias que contienen algún descriptor (matcher).
#   5. Para cada noticia candidata:
#      a. Registrar la noticia en news_item (deduplicación por URL).
#      b. Crear una Notification en BD (deduplicación por alerta+noticia).
#   6. Crear la notificación en buzón interno y enviar email al usuario.
#
# Decisión de diseño:
#   Este módulo recibe una SessionFactory (callable que devuelve Session)
#   en lugar de una Session directa. Esto es necesario porque APScheduler
#   ejecuta los jobs en hilos propios, fuera del ciclo de vida de FastAPI.
#   Las Sessions de SQLAlchemy no son thread-safe — cada hilo debe crear
#   la suya. Por eso el monitor crea y cierra su propia sesión en cada
#   ejecución, sin depender del sistema de inyección de dependencias de
#   FastAPI (que gestiona Sessions por request HTTP).

import logging
from datetime import datetime, timezone
from typing import Callable, List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from app.core.matcher import filter_matching_news, MatchResult
from app.features.notifications.service import NotificationsService
from app.features.rss_channels.fetcher import fetch_news_from_channel, NewsItemData
from app.db.models import (
    Alert,
    Descriptor,
    CrossAlertDescriptor,
    RSSChannel,
    NewsItem,
    Notification,
    User,
)

logger = logging.getLogger(__name__)


def run_alert_monitor_job(alert_id: int, SessionFactory: Callable[[], Session]) -> None:
    """
    Punto de entrada del job de monitorización. APScheduler llama a esta
    función según la cron_expression de cada alerta.

    Args:
        alert_id:       ID de la alerta a monitorizar.
        SessionFactory: Callable que devuelve una nueva Session de SQLAlchemy.
                        Se pasa como argumento para facilitar el testing
                        (se puede inyectar una sesión de prueba).
    """
    db: Session = SessionFactory()
    try:
        _execute_monitor(alert_id, db)
    except Exception as exc:
        logger.error(
            "Error inesperado en monitor de alerta %d: %s",
            alert_id,
            exc,
            exc_info=True,
        )
    finally:
        db.close()


def _execute_monitor(alert_id: int, db: Session) -> None:
    """
    Lógica principal del monitor. Separada de run_alert_monitor_job para
    que los tests puedan llamarla directamente con una sesión controlada
    sin necesidad de pasar un SessionFactory.
    """

    # ------------------------------------------------------------------
    # Paso 1: Cargar la alerta
    # ------------------------------------------------------------------
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if alert is None:
        # La alerta fue eliminada después de registrar el job en el scheduler.
        # El scheduler la eliminará en el próximo ciclo; aquí simplemente
        # salimos sin error.
        logger.warning("Monitor: alerta %d no encontrada en BD. Job huérfano.", alert_id)
        return

    logger.info("Monitor iniciado para alerta '%s' (id=%d)", alert.name, alert_id)

    user = db.query(User).filter(User.id == alert.user_id).first()
    if user is None:
        logger.warning("Monitor: usuario %d no encontrado para alerta %d.", alert.user_id, alert_id)
        return

    notifications_service = NotificationsService(db)

    # ------------------------------------------------------------------
    # Paso 2: Cargar los descriptores de la alerta
    # Los descriptores incluyen la palabra clave original + los sinónimos
    # generados por Gemini que el usuario aceptó al crear la alerta.
    # ------------------------------------------------------------------
    descriptors: List[str] = [
        name
        for (name,) in (
            db.query(Descriptor.name)
            .join(CrossAlertDescriptor, CrossAlertDescriptor.descriptor_id == Descriptor.id)
            .filter(CrossAlertDescriptor.alert_id == alert_id)
            .all()
        )
    ]

    if not descriptors:
        logger.warning(
            "Alerta '%s' (id=%d) no tiene descriptores. No hay nada que monitorizar.",
            alert.name,
            alert_id,
        )
        return

    logger.info(
        "Alerta '%s': %d descriptores cargados: %s",
        alert.name,
        len(descriptors),
        descriptors,
    )

    # ------------------------------------------------------------------
    # Paso 3: Obtener los canales RSS a monitorizar.
    #
    # Estrategia de selección de canales (del enunciado):
    #   "por omisión serán todos los que pertenezcan a la misma categoría"
    #
    # La alerta tiene categorías IPTC asociadas (CrossAlertAlertCategoryItem).
    # Buscamos todos los RSSChannel cuya category_id coincida con alguna
    # de esas categorías. Si la alerta no tiene categorías asignadas,
    # monitorizamos TODOS los canales disponibles (comportamiento de
    # fallback para alertas sin categoría explícita).
    # ------------------------------------------------------------------
    from app.db.models import CrossAlertAlertCategoryItem, AlertCategoryItem

    category_codes = [
        code
        for (code,) in (
            db.query(AlertCategoryItem.code)
            .join(
                CrossAlertAlertCategoryItem,
                CrossAlertAlertCategoryItem.alert_category_item_id == AlertCategoryItem.id,
            )
            .filter(CrossAlertAlertCategoryItem.alert_id == alert_id)
            .all()
        )
    ]

    if category_codes:
        # Tomamos todos los canales cuya category esté entre las de la alerta.
        # Category en RSSChannel referencia Category, no AlertCategoryItem —
        # usamos el nombre como puente.
        from app.db.models import Category
        category_ids = [
            cid
            for (cid,) in (
                db.query(Category.id)
                .filter(Category.name.in_(category_codes))
                .all()
            )
        ]
        channels = (
            db.query(RSSChannel)
            .filter(RSSChannel.category_id.in_(category_ids))
            .all()
        ) if category_ids else db.query(RSSChannel).all()
    else:
        # Sin categorías explícitas: todos los canales
        channels = db.query(RSSChannel).all()

    if not channels:
        logger.warning(
            "Alerta '%s' (id=%d): no hay canales RSS disponibles para monitorizar.",
            alert.name,
            alert_id,
        )
        return

    logger.info(
        "Alerta '%s': monitorizando %d canales RSS.",
        alert.name,
        len(channels),
    )

    # ------------------------------------------------------------------
    # Paso 4: Descargar y filtrar noticias
    # ------------------------------------------------------------------
    all_news: List[NewsItemData] = []
    for channel in channels:
        news = fetch_news_from_channel(channel.id, str(channel.url))
        all_news.extend(news)

    logger.info(
        "Alerta '%s': %d noticias totales descargadas de %d canales.",
        alert.name,
        len(all_news),
        len(channels),
    )

    if not all_news:
        logger.info("Alerta '%s': sin noticias nuevas en esta ejecución.", alert.name)
        return

    matches: List[MatchResult] = filter_matching_news(all_news, descriptors)

    logger.info(
        "Alerta '%s': %d noticias candidatas tras el matching.",
        alert.name,
        len(matches),
    )

    if not matches:
        return

    # ------------------------------------------------------------------
    # Paso 5: Persistir noticias y crear notificaciones
    # ------------------------------------------------------------------
    now = datetime.now(timezone.utc)
    notifications_created = 0

    for match in matches:
        news_item_db = _get_or_create_news_item(db, match.news_item, now)
        if news_item_db is None:
            # Error al persistir la noticia — ya logueado en el helper
            continue

        created = notifications_service.create_and_dispatch_notification(
            alert=alert,
            user=user,
            news_item=news_item_db,
            matched_descriptor=match.matched_descriptor,
            timestamp=now,
        )
        if created:
            notifications_created += 1

    logger.info(
        "Alerta '%s': %d notificaciones nuevas creadas.",
        alert.name,
        notifications_created,
    )

    if notifications_created > 0:
        _log_pending_notifications(db, alert_id, alert.name)


# ---------------------------------------------------------------------------
# Helpers privados
# ---------------------------------------------------------------------------

def _get_or_create_news_item(
    db: Session,
    news_data: NewsItemData,
    created_at: datetime,
) -> NewsItem | None:
    """
    Devuelve el NewsItem existente para esa URL, o crea uno nuevo.

    La deduplicación se basa en la constraint UNIQUE de news_item.url.
    Si dos ejecuciones concurrentes intentan insertar la misma URL,
    IntegrityError captura el conflicto y devolvemos el registro ya
    existente (patrón get-or-create thread-safe).

    Returns:
        El NewsItem (nuevo o existente), o None si hay un error inesperado.
    """
    existing = db.query(NewsItem).filter(NewsItem.url == news_data.url).first()
    if existing:
        return existing

    new_item = NewsItem(
        url=news_data.url,
        title=news_data.title[:500],   # respetamos el límite del modelo
        summary=news_data.summary or "",
        published=news_data.published,
        channel_id=news_data.channel_id,
        created_at=created_at,
    )
    try:
        db.add(new_item)
        db.flush()   # flush sin commit para mantener la transacción abierta
        return new_item
    except IntegrityError:
        db.rollback()
        # Otra ejecución concurrente insertó la misma URL entre nuestro
        # SELECT y nuestro INSERT — recuperamos el registro existente.
        return db.query(NewsItem).filter(NewsItem.url == news_data.url).first()
    except Exception as exc:
        db.rollback()
        logger.error("Error al persistir NewsItem (%s): %s", news_data.url, exc)
        return None


def _log_pending_notifications(db: Session, alert_id: int, alert_name: str) -> None:
    """
    Registra en el log un resumen de las notificaciones pendientes de leer
    para esta alerta. Útil para diagnóstico durante el desarrollo.
    """
    count = (
        db.query(Notification)
        .filter(Notification.alert_id == alert_id, Notification.is_read == False)
        .count()
    )
    logger.info(
        "Alerta '%s': %d notificaciones sin leer en buzón.",
        alert_name,
        count,
    )