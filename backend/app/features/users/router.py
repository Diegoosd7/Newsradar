from typing import List
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from .schemas import UserUpdate
from .service import UsersService
from ...db.database import get_db
from ...core.security import get_current_user
from ...core.shared_schemas import UserInDB, UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


def get_users_service(db: Session = Depends(get_db)):
    return UsersService(db)


@router.get("/", response_model=List[UserResponse])
def list_users(
    _: UserInDB = Depends(get_current_user),
    service: UsersService = Depends(get_users_service),
) -> List[UserResponse]:
    return service.list_users()


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    payload: UserCreate,
    _: UserInDB = Depends(get_current_user),
    service: UsersService = Depends(get_users_service),
) -> UserResponse:
    return service.create_user(payload)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    _: UserInDB = Depends(get_current_user),
    service: UsersService = Depends(get_users_service),
) -> UserResponse:
    return service.get_user(user_id)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    payload: UserUpdate,
    _: UserInDB = Depends(get_current_user),
    service: UsersService = Depends(get_users_service),
) -> UserResponse:
    return service.update_user(user_id, payload)


@router.delete(
    "/{user_id}",
    status_code=204,
    response_model=None,
    response_class=Response,
)
def delete_user(
    user_id: int,
    _: UserInDB = Depends(get_current_user),
    service: UsersService = Depends(get_users_service),
) -> None:
    return service.delete_user(user_id)
