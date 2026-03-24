from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from .schemas import CategoryResponse, CategoryCreate, CategoryUpdate
from ...core.common_service import CommonService
from ...db.models import Category, RSSChannel


class CategoriesService(CommonService):
    def __init__(self, db: Session):
        super().__init__(db)

    def list_categories(self) -> List[CategoryResponse]:
        categories = self.db.query(Category).all()
        return [
            CategoryResponse(id=category.id, name=category.name, source=category.source)
            for category in categories
        ]

    def create_category(self, payload: CategoryCreate) -> CategoryResponse:
        category = Category(name=payload.name, source=payload.source)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return CategoryResponse(id=category.id, name=category.name, source=category.source)

    def get_category(
        self,
        category_id: int,
    ) -> CategoryResponse:
        category = self._get_category_or_404(category_id)
        return CategoryResponse(id=category.id, name=category.name, source=category.source)

    def update_category(
        self,
        category_id: int,
        payload: CategoryUpdate,
    ) -> CategoryResponse:
        category = self._get_category_or_404(category_id)
        data = payload.model_dump(exclude_unset=True)
        if "name" in data:
            category.name = data["name"]
        if "source" in data:
            category.source = data["source"]

        self.db.commit()
        self.db.refresh(category)
        return CategoryResponse(id=category.id, name=category.name, source=category.source)

    def delete_category(self, category_id: int) -> None:
        category = self._get_category_or_404(category_id)
        used_by_channel = (
            self.db.query(RSSChannel)
            .filter(RSSChannel.category_id == category_id)
            .first()
        )
        if used_by_channel is not None:
            raise HTTPException(status_code=409, detail="Categoría asociada a canales RSS")

        self.db.delete(category)
        self.db.commit()

    def _get_category_or_404(self, category_id: int) -> Category:
        category = self.db.query(Category).filter(Category.id == category_id).first()
        if category is None:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        return category
