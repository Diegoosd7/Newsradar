from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv

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

# Carga las variables del archivo .env
load_dotenv()

API_PREFIX = "/api/v1"

app = FastAPI(
    title="NewsRadar API",
    version="1.0.0",
    description="API REST para gestión de usuarios, alertas, notificaciones, fuentes y canales RSS.",
)

v1_router = APIRouter()
v1_router.include_router(alerts_router)
v1_router.include_router(auth_router)
v1_router.include_router(information_sources_router)
v1_router.include_router(notifications_router)
v1_router.include_router(roles_router)
v1_router.include_router(rss_channels_router)
v1_router.include_router(stats_router)
v1_router.include_router(system_router)
v1_router.include_router(users_router)

app.include_router(v1_router, prefix=API_PREFIX)
