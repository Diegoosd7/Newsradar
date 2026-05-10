from typing import List
from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from .schemas import (
    InformationSourceResponse,
    InformationSourceCreate,
    InformationSourceUpdate,
)
from .service import InformationSourcesService
from ...db.database import get_db
from ...core.security import get_current_user
from ...core.shared_schemas import UserInDB

router = APIRouter(prefix="/information-sources", tags=["information-sources"])


def get_information_sources_service(db: Session = Depends(get_db)):
    return InformationSourcesService(db)


@router.get(
    "",
    response_model=List[InformationSourceResponse],
    tags=["information-sources"],
)
def list_information_sources(
    _: UserInDB = Depends(get_current_user),
    service: InformationSourcesService = Depends(get_information_sources_service),
) -> List[InformationSourceResponse]:
    return service.list_information_sources()


@router.post(
    "",
    response_model=InformationSourceResponse,
    status_code=201,
    tags=["information-sources"],
)
def create_information_source(
    payload: InformationSourceCreate,
    _: UserInDB = Depends(get_current_user),
    service: InformationSourcesService = Depends(get_information_sources_service),
) -> InformationSourceResponse:
    return service.create_information_source(payload)


@router.get(
    "/{source_id}",
    response_model=InformationSourceResponse,
    tags=["information-sources"],
)
def get_information_source(
    source_id: int,
    _: UserInDB = Depends(get_current_user),
    service: InformationSourcesService = Depends(get_information_sources_service),
) -> InformationSourceResponse:
    return service.get_information_source(source_id)


@router.put(
    "/{source_id}",
    response_model=InformationSourceResponse,
    tags=["information-sources"],
)
def update_information_source(
    source_id: int,
    payload: InformationSourceUpdate,
    _: UserInDB = Depends(get_current_user),
    service: InformationSourcesService = Depends(get_information_sources_service),
) -> InformationSourceResponse:
    return service.update_information_source(source_id, payload)


@router.delete(
    "/{source_id}",
    status_code=204,
    response_model=None,
    response_class=Response,
    tags=["information-sources"],
)
def delete_information_source(
    source_id: int,
    _: UserInDB = Depends(get_current_user),
    service: InformationSourcesService = Depends(get_information_sources_service),
) -> None:
    return service.delete_information_source(source_id)
