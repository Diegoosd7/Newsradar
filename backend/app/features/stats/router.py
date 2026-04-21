from typing import List
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from .schemas import (
    StatsResponse,
    StatsCreate,
    StatsUpdate,
    DashboardStatsResponse,
)
from .service import StatsService
from ...db.database import get_db
from ...core.security import get_current_user
from ...core.shared_schemas import UserInDB

router = APIRouter(prefix="/stats", tags=["stats"])


def get_stats_service(db: Session = Depends(get_db)):
    return StatsService(db)


@router.get("/", response_model=List[StatsResponse], tags=["stats"])
def list_stats(
    _: UserInDB = Depends(get_current_user),
    service: StatsService = Depends(get_stats_service),
) -> List[StatsResponse]:
    return service.list_stats()


@router.post("/", response_model=StatsResponse, status_code=201, tags=["stats"])
def create_stats(
    payload: StatsCreate,
    _: UserInDB = Depends(get_current_user),
    service: StatsService = Depends(get_stats_service),
) -> StatsResponse:
    return service.create_stats(payload)


@router.get("/dashboard", response_model=DashboardStatsResponse, tags=["stats"])
def get_dashboard_stats(
    _: UserInDB = Depends(get_current_user),
    service: StatsService = Depends(get_stats_service),
) -> DashboardStatsResponse:
    return service.get_dashboard_stats()


@router.get("/{stats_id}", response_model=StatsResponse, tags=["stats"])
def get_stats(
    stats_id: int,
    _: UserInDB = Depends(get_current_user),
    service: StatsService = Depends(get_stats_service),
) -> StatsResponse:
    return service.get_stats(stats_id)


@router.put("/{stats_id}", response_model=StatsResponse, tags=["stats"])
def update_stats(
    stats_id: int,
    payload: StatsUpdate,
    _: UserInDB = Depends(get_current_user),
    service: StatsService = Depends(get_stats_service),
) -> StatsResponse:
    return service.update_stats(stats_id, payload)


@router.delete(
    "/{stats_id}",
    status_code=204,
    response_model=None,
    response_class=Response,
    tags=["stats"],
)
def delete_stats(
    stats_id: int,
    _: UserInDB = Depends(get_current_user),
    service: StatsService = Depends(get_stats_service),
) -> None:
    return service.delete_stats(stats_id)