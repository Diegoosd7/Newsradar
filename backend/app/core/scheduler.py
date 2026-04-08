# app/core/scheduler.py
#
# Responsabilidad: gestionar el ciclo de vida del scheduler de tareas
# programadas y mantener sincronizados los jobs con las alertas en BD.
#
# Por qué APScheduler (ver ADR-001):
#   - No requiere infraestructura externa (sin Redis, sin Celery broker).
#   - Los jobs se pueden añadir/modificar/eliminar en tiempo de ejecución.
#   - Se integra limpiamente con los eventos startup/shutdown de FastAPI.
#   - Si el contenedor se reinicia, los jobs se recargan desde BD en startup.
#
# Contrato con el resto del sistema:
#   - alerts/service.py llama a register_alert_job() al crear una alerta.
#   - alerts/service.py llama a update_alert_job() al actualizar una alerta.
#   - alerts/service.py llama a remove_alert_job() al eliminar una alerta.
#   - main.py llama a start_scheduler() en el evento startup de FastAPI.
#   - main.py llama a stop_scheduler() en el evento shutdown de FastAPI.

import logging
from functools import partial

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.base import JobLookupError
from sqlalchemy.orm import Session

from app.db.models import Alert

logger = logging.getLogger(__name__)

# Instancia global del scheduler.
# Es global porque necesita ser accesible desde service.py (para registrar
# jobs cuando se crean/modifican alertas) y desde main.py (para el ciclo
# de vida). En una arquitectura más grande usaríamos inyección de
# dependencias, pero para este proyecto la instancia global es suficiente
# y evita complejidad innecesaria.
scheduler = BackgroundScheduler(
    job_defaults={
        # Si un job tarda más de lo previsto y llega la siguiente ejecución,
        # APScheduler puede acumular ejecuciones pendientes. Con max_instances=1
        # garantizamos que una alerta no se monitoriza dos veces en paralelo.
        "max_instances": 1,
        # Si el sistema estuvo caído y hay ejecuciones perdidas, no las
        # recuperamos — simplemente esperamos la siguiente. Esto evita una
        # avalancha de jobs al reiniciar.
        "misfire_grace_time": 60,
        "coalesce": True,
    }
)


def start_scheduler(db: Session) -> None:
    """
    Arranca el scheduler y registra un job por cada alerta activa en BD.

    Llamar en el evento startup de FastAPI. Recibe una Session para leer
    las alertas existentes y registrarlas como jobs iniciales.

    Args:
        db: Session de SQLAlchemy. Solo se usa durante el arranque para
            cargar las alertas — el scheduler no la mantiene abierta.
    """
    # Importación local para evitar importación circular:
    # scheduler.py → monitor.py → models.py → (no importa scheduler)
    from app.features.alerts.monitor import run_alert_monitor_job
    from app.db.database import SessionLocal

    alerts = db.query(Alert).all()
    logger.info("Scheduler: cargando %d alertas desde BD...", len(alerts))

    for alert in alerts:
        _register_job(
            alert_id=alert.id,
            cron_expression=alert.cron_expression,
            SessionLocal=SessionLocal,
        )

    scheduler.start()
    logger.info("Scheduler iniciado. Jobs activos: %d", len(scheduler.get_jobs()))


def stop_scheduler() -> None:
    """
    Detiene el scheduler limpiamente.
    Llamar en el evento shutdown de FastAPI.
    """
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Scheduler detenido.")


def register_alert_job(alert_id: int, cron_expression: str) -> None:
    """
    Registra un nuevo job para una alerta recién creada.
    Llamar desde AlertsService.create_user_alert() después del commit.

    Args:
        alert_id:        ID de la alerta en BD.
        cron_expression: Expresión cron de la alerta (ej: "0 * * * *").
    """
    from app.db.database import SessionLocal

    if not scheduler.running:
        logger.warning(
            "Scheduler no está corriendo. Job para alerta %d no registrado.", alert_id
        )
        return

    _register_job(alert_id, cron_expression, SessionLocal)
    logger.info(
        "Job registrado para alerta %d con cron '%s'.", alert_id, cron_expression
    )


def update_alert_job(alert_id: int, cron_expression: str) -> None:
    """
    Actualiza el cron de un job existente.
    Llamar desde AlertsService.update_user_alert() si cambia cron_expression.

    Si el job no existe (caso edge: scheduler reiniciado entre operaciones),
    lo crea de nuevo en lugar de fallar.
    """
    from app.db.database import SessionLocal

    job_id = _job_id(alert_id)
    try:
        scheduler.reschedule_job(
            job_id,
            trigger=_make_trigger(cron_expression),
        )
        logger.info(
            "Job actualizado para alerta %d con nuevo cron '%s'.",
            alert_id,
            cron_expression,
        )
    except JobLookupError:
        logger.warning(
            "Job para alerta %d no encontrado al actualizar. Creando de nuevo.",
            alert_id,
        )
        _register_job(alert_id, cron_expression, SessionLocal)


def remove_alert_job(alert_id: int) -> None:
    """
    Elimina el job de una alerta borrada.
    Llamar desde AlertsService.delete_user_alert() antes o después del commit.

    Si el job no existe, no hace nada (operación idempotente).
    """
    job_id = _job_id(alert_id)
    try:
        scheduler.remove_job(job_id)
        logger.info("Job eliminado para alerta %d.", alert_id)
    except JobLookupError:
        logger.debug(
            "Job para alerta %d no encontrado al eliminar (ya inexistente).", alert_id
        )


# ---------------------------------------------------------------------------
# Helpers privados
# ---------------------------------------------------------------------------

def _job_id(alert_id: int) -> str:
    """
    Genera el identificador único del job a partir del ID de la alerta.
    Prefijo 'alert_' para evitar colisiones con otros posibles jobs futuros.
    """
    return f"alert_{alert_id}"


def _make_trigger(cron_expression: str) -> CronTrigger:
    """
    Convierte una expresión cron estándar (5 campos) en un CronTrigger
    de APScheduler.

    Formato esperado: "minuto hora día_mes mes día_semana"
    Ejemplos:
        "0 * * * *"    → cada hora en punto
        "*/30 * * * *" → cada 30 minutos
        "0 8 * * 1-5"  → a las 8:00 de lunes a viernes

    Si la expresión es inválida, APScheduler lanzará ValueError aquí,
    que alerts/service.py debe capturar y convertir en HTTP 422.
    """
    fields = cron_expression.strip().split()
    if len(fields) != 5:
        raise ValueError(
            f"Expresión cron inválida: '{cron_expression}'. "
            f"Se esperan 5 campos (minuto hora día_mes mes día_semana)."
        )
    minute, hour, day, month, day_of_week = fields
    return CronTrigger(
        minute=minute,
        hour=hour,
        day=day,
        month=month,
        day_of_week=day_of_week,
        timezone="UTC",
    )


def _register_job(alert_id: int, cron_expression: str, SessionLocal) -> None:
    """
    Registra o reemplaza el job de una alerta en el scheduler.

    Usa 'replace_existing=True' para que sea idempotente: si el job ya
    existe (por ejemplo, startup tras reinicio), lo reemplaza sin error.

    Usamos functools.partial para "congelar" el alert_id y SessionLocal
    como argumentos del job. APScheduler necesita que el callable sea
    serializable — partial cumple ese requisito.
    """
    from app.features.alerts.monitor import run_alert_monitor_job

    try:
        trigger = _make_trigger(cron_expression)
    except ValueError as exc:
        logger.error(
            "Cron inválido para alerta %d ('%s'): %s. Job no registrado.",
            alert_id,
            cron_expression,
            exc,
        )
        return

    job_callable = partial(
        run_alert_monitor_job,
        alert_id=alert_id,
        SessionFactory=SessionLocal,
    )

    scheduler.add_job(
        func=job_callable,
        trigger=trigger,
        id=_job_id(alert_id),
        name=f"Monitor alerta {alert_id}",
        replace_existing=True,
    )