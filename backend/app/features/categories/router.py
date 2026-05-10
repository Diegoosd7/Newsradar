from typing import List
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from .schemas import CategoryResponse, CategoryCreate, CategoryUpdate
from .service import CategoriesService
from ...db.database import get_db
from ...core.security import get_current_user
from ...core.shared_schemas import UserInDB

router = APIRouter(prefix="/categories", tags=["categories"])


def get_categories_service(db: Session = Depends(get_db)):
    return CategoriesService(db)


@router.get("", response_model=List[CategoryResponse], tags=["categories"])
def list_categories(
    _: UserInDB = Depends(get_current_user),
    service: CategoriesService = Depends(get_categories_service),
) -> List[CategoryResponse]:
    return service.list_categories()


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=201,
    tags=["categories"],
)
def create_category(
    payload: CategoryCreate,
    _: UserInDB = Depends(get_current_user),
    service: CategoriesService = Depends(get_categories_service),
) -> CategoryResponse:
    return service.create_category(payload)


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    tags=["categories"],
)
def get_category(
    category_id: int,
    _: UserInDB = Depends(get_current_user),
    service: CategoriesService = Depends(get_categories_service),
) -> CategoryResponse:
    return service.get_category(category_id)


@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
    tags=["categories"],
)
def update_category(
    category_id: int,
    payload: CategoryUpdate,
    _: UserInDB = Depends(get_current_user),
    service: CategoriesService = Depends(get_categories_service),
) -> CategoryResponse:
    return service.update_category(category_id, payload)


@router.delete(
    "/{category_id}",
    status_code=204,
    response_model=None,
    response_class=Response,
    tags=["categories"],
)
def delete_category(
    category_id: int,
    _: UserInDB = Depends(get_current_user),
    service: CategoriesService = Depends(get_categories_service),
) -> None:
    return service.delete_category(category_id)
