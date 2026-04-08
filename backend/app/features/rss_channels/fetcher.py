# app/features/rss_channels/fetcher.py
#
# Responsabilidad única: descargar un feed RSS y devolver sus noticias
# normalizadas como objetos Python simples.
#
# Por qué este módulo existe separado:
#   El sistema de monitorización necesita leer feeds RSS de múltiples fuentes
#   con formatos ligeramente distintos (RSS 2.0, Atom, RSS 1.0). feedparser
#   abstrae esas diferencias y siempre devuelve la misma estructura. Al
#   aislar esta lógica aquí, el monitor y los tests no dependen de detalles
#   de red ni de formato — solo reciben una lista de NewsItemData.
#
# Decisión de diseño (ver ADR-002):
#   Se usa feedparser en modo síncrono. Para la carga actual (100 canales
#   distribuidos en el tiempo por expresiones cron) es suficiente. Una
#   migración futura a httpx async no requeriría cambiar el contrato de
#   esta función, solo su implementación interna.

import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional

import feedparser

logger = logging.getLogger(__name__)


@dataclass
class NewsItemData:
    """
    Representación normalizada de una noticia extraída de un feed RSS.

    Usamos dataclass en lugar de Pydantic porque este objeto es interno
    al sistema de procesamiento — nunca viaja por la API REST. Pydantic
    añadiría validación innecesaria en un objeto que nosotros mismos
    construimos de forma controlada.

    Campos:
        url         — URL canónica del artículo. Es la clave de deduplicación.
                      Si el feed no tiene link, se descarta la entrada.
        title       — Título del artículo. Obligatorio.
        summary     — Resumen o descripción. Puede estar vacío.
        published   — Fecha de publicación según el feed. Puede ser None
                      si el feed no la incluye o tiene formato no reconocible.
        channel_id  — ID del canal RSS del que proviene, para trazabilidad.
    """
    url: str
    title: str
    summary: str
    published: Optional[datetime]
    channel_id: int


def fetch_news_from_channel(channel_id: int, channel_url: str) -> List[NewsItemData]:
    """
    Descarga y parsea un canal RSS. Devuelve una lista (posiblemente vacía)
    de NewsItemData normalizados.

    No lanza excepciones: si el feed falla (timeout, formato inválido,
    servidor caído), registra el error y devuelve lista vacía. Esto es
    intencional — un canal RSS caído no debe interrumpir la monitorización
    del resto de alertas activas.

    Args:
        channel_id:  ID del RSSChannel en base de datos (para trazabilidad).
        channel_url: URL del feed a descargar.

    Returns:
        Lista de NewsItemData. Vacía si el feed falla o no tiene entradas.
    """
    try:
        # feedparser hace la petición HTTP internamente.
        # bozo=True indica que el feed tiene errores de formato pero es
        # parseable; lo procesamos igualmente.
        feed = feedparser.parse(channel_url)

        if feed.bozo and feed.bozo_exception:
            # Algunos feeds tienen XML mal formado pero feedparser los
            # recupera parcialmente. Registramos el aviso pero continuamos.
            logger.warning(
                "Feed con formato irregular en canal %d (%s): %s",
                channel_id,
                channel_url,
                feed.bozo_exception,
            )

        items: List[NewsItemData] = []

        for entry in feed.entries:
            # La URL es obligatoria — es la clave de deduplicación.
            url = _extract_url(entry)
            if not url:
                logger.debug(
                    "Entrada sin URL en canal %d, descartada: %s",
                    channel_id,
                    entry.get("title", "(sin título)"),
                )
                continue

            title = _extract_title(entry)
            if not title:
                logger.debug(
                    "Entrada sin título en canal %d (%s), descartada.",
                    channel_id,
                    url,
                )
                continue

            summary = _extract_summary(entry)
            published = _extract_published(entry)

            items.append(
                NewsItemData(
                    url=url,
                    title=title,
                    summary=summary,
                    published=published,
                    channel_id=channel_id,
                )
            )

        logger.info(
            "Canal %d (%s): %d noticias obtenidas.",
            channel_id,
            channel_url,
            len(items),
        )
        return items

    except Exception as exc:
        # Captura genérica para que un canal problemático no tumbe el job
        # completo. El error queda en logs para diagnóstico.
        logger.error(
            "Error al procesar canal %d (%s): %s",
            channel_id,
            channel_url,
            exc,
            exc_info=True,
        )
        return []


# ---------------------------------------------------------------------------
# Helpers privados de extracción de campos
# ---------------------------------------------------------------------------

def _extract_url(entry) -> Optional[str]:
    """
    Extrae la URL del artículo. feedparser usa 'link' en la mayoría de
    formatos, pero algunos feeds Atom usan 'id' como URL canónica.
    """
    url = entry.get("link") or entry.get("id")
    if not url:
        return None
    url = url.strip()
    # Descartamos IDs que no sean URLs (algunos feeds Atom usan UUIDs como id)
    if not url.startswith("http"):
        return None
    return url


def _extract_title(entry) -> Optional[str]:
    """Extrae y limpia el título. feedparser siempre tiene 'title' si existe."""
    title = entry.get("title", "").strip()
    return title if title else None


def _extract_summary(entry) -> str:
    """
    Extrae el resumen. feedparser expone esto en 'summary' (RSS 2.0) o
    'content' (Atom). Si hay content (Atom), tomamos el primero disponible.
    Devuelve string vacío si no hay resumen — nunca None, para simplificar
    el matching posterior.
    """
    # Atom: content es una lista de objetos con .value
    if entry.get("content"):
        return entry.content[0].get("value", "").strip()

    # RSS 2.0 / RSS 1.0: summary o description
    summary = entry.get("summary") or entry.get("description") or ""
    return summary.strip()


def _extract_published(entry) -> Optional[datetime]:
    """
    Convierte la fecha de publicación del feed a datetime UTC.

    feedparser intenta parsear la fecha en 'published_parsed' (tupla
    time.struct_time en UTC) o 'updated_parsed'. Si ninguno está presente
    o es parseable, devuelve None — preferible a inventar una fecha.
    """
    time_struct = entry.get("published_parsed") or entry.get("updated_parsed")
    if not time_struct:
        return None
    try:
        # time.struct_time -> datetime UTC
        return datetime(*time_struct[:6], tzinfo=timezone.utc)
    except (TypeError, ValueError):
        return None