from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from pathlib import Path

from app.features.alerts.router import router as alerts_router
from app.features.auth.router import router as auth_router
from app.features.categories.router import router as categories_router
from app.features.information_sources.router import router as information_sources_router
from app.features.notifications.router import router as notifications_router
from app.features.roles.router import router as roles_router
from app.features.rss_channels.router import router as rss_channels_router
from app.features.stats.router import router as stats_router
from app.features.system.router import router as system_router
from app.features.users.router import router as users_router
from app.db.database import SessionLocal, engine
from app.db.models import Base
from app.core.scheduler import start_scheduler, stop_scheduler

ENV_FILE = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=ENV_FILE)

API_PREFIX = "/api/v1"

app = FastAPI(
    title="NewsRadar API",
    version="1.0.0",
    description="API REST para gestión de usuarios, alertas, notificaciones, fuentes y canales RSS.",
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        start_scheduler(db)
    finally:
        db.close()


@app.on_event("shutdown")
def on_shutdown() -> None:
    stop_scheduler()


v1_router = APIRouter()
v1_router.include_router(alerts_router)
v1_router.include_router(auth_router)
v1_router.include_router(categories_router)
v1_router.include_router(information_sources_router)
v1_router.include_router(notifications_router)
v1_router.include_router(roles_router)
v1_router.include_router(rss_channels_router)
v1_router.include_router(stats_router)
v1_router.include_router(system_router)
v1_router.include_router(users_router)

app.include_router(v1_router, prefix=API_PREFIX)