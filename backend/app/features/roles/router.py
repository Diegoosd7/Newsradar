from typing import List
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from .schemas import RoleResponse, RoleCreate, RoleUpdate
from .service import RolesService
from ...db.database import get_db
from ...core.security import get_current_user
from ...core.shared_schemas import UserInDB

router = APIRouter(prefix="/roles", tags=["roles"])


def get_roles_service(db: Session = Depends(get_db)):
    return RolesService(db)


@router.get("/", response_model=List[RoleResponse], tags=["roles"])
def list_roles(
    _: UserInDB = Depends(get_current_user),
    service: RolesService = Depends(get_roles_service),
) -> List[RoleResponse]:
    return service.list_roles()


@router.post("/", response_model=RoleResponse, status_code=201, tags=["roles"])
def create_role(
    payload: RoleCreate,
    _: UserInDB = Depends(get_current_user),
    service: RolesService = Depends(get_roles_service),
) -> RoleResponse:
    return service.create_role(payload)


@router.get("/{role_id}", response_model=RoleResponse, tags=["roles"])
def get_role(
    role_id: int,
    _: UserInDB = Depends(get_current_user),
    service: RolesService = Depends(get_roles_service),
) -> RoleResponse:
    return service.get_role(role_id)


@router.put("/{role_id}", response_model=RoleResponse, tags=["roles"])
def update_role(
    role_id: int,
    payload: RoleUpdate,
    _: UserInDB = Depends(get_current_user),
    service: RolesService = Depends(get_roles_service),
) -> RoleResponse:
    return service.update_role(role_id, payload)


@router.delete(
    "/{role_id}",
    status_code=204,
    response_model=None,
    response_class=Response,
    tags=["roles"],
)
def delete_role(
    role_id: int,
    _: UserInDB = Depends(get_current_user),
    service: RolesService = Depends(get_roles_service),
) -> None:
    return service.delete_role(role_id)
