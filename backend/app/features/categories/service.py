from typing import List
from sqlalchemy.orm import Session
from .schemas import CategoryResponse, CategoryCreate, CategoryUpdate
from ...core.common_service import CommonService


class CategoriesService(CommonService):
    def __init__(self, db: Session):
        super().__init__(db)

    def list_categories(self) -> List[CategoryResponse]:
        pass

    def create_category(self, payload: CategoryCreate) -> CategoryResponse:
        pass

    def get_category(
        self,
        category_id: int,
    ) -> CategoryResponse:
        pass

    def update_category(
        self,
        category_id: int,
        payload: CategoryUpdate,
    ) -> CategoryResponse:
        pass

    def delete_category(self, category_id: int) -> None:
        pass
