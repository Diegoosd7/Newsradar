from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from .schemas import CategoryResponse, CategoryCreate, CategoryUpdate
from ...core.common_service import CommonService
from ...db.models import Category, RSSChannel

IPTC_CATALOG: dict[str, str] = {
    name.strip().lower(): code
    for code, name in [
        ("01000000", "Artes, cultura, entretenimiento y medios"),
        ("03000000", "Catástrofes y accidentes"),
        ("13000000", "Ciencia y tecnología"),
        ("16000000", "Conflicto, guerra y paz"),
        ("15000000", "Deporte"),
        ("04000000", "Economía, negocios y finanzas"),
        ("05000000", "Educación"),
        ("10000000", "Estilo de vida y tiempo libre"),
        ("08000000", "Interés humano, animales, insólito"),
        ("09000000", "Mano de obra"),
        ("06000000", "Medio ambiente"),
        ("17000000", "Meteorología"),
        ("02000000", "Policía y justicia"),
        ("11000000", "Política"),
        ("12000000", "Religión y culto"),
        ("07000000", "Salud"),
        ("14000000", "Sociedad"),
    ]
}

IPTC_CODE_TO_NAME: dict[str, str] = {
    code: name
    for code, name in [
        ("01000000", "Artes, cultura, entretenimiento y medios"),
        ("03000000", "Catástrofes y accidentes"),
        ("13000000", "Ciencia y tecnología"),
        ("16000000", "Conflicto, guerra y paz"),
        ("15000000", "Deporte"),
        ("04000000", "Economía, negocios y finanzas"),
        ("05000000", "Educación"),
        ("10000000", "Estilo de vida y tiempo libre"),
        ("08000000", "Interés humano, animales, insólito"),
        ("09000000", "Mano de obra"),
        ("06000000", "Medio ambiente"),
        ("17000000", "Meteorología"),
        ("02000000", "Policía y justicia"),
        ("11000000", "Política"),
        ("12000000", "Religión y culto"),
        ("07000000", "Salud"),
        ("14000000", "Sociedad"),
    ]
}


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
        name = payload.name.strip()
        iptc_code = IPTC_CATALOG.get(name.lower())
        if iptc_code is None:
            raise HTTPException(
                status_code=422,
                detail=f"El nombre '{name}' no pertenece al catálogo IPTC cerrado",
            )

        if payload.code is not None and payload.code != iptc_code:
            raise HTTPException(
                status_code=422,
                detail=f"El code '{payload.code}' no corresponde al nombre '{name}' en el catálogo IPTC (esperado '{iptc_code}')",
            )

        # Use IPTC code integer as the category primary key
        category_id = int(iptc_code)
        existing = self.db.query(Category).filter(Category.id == category_id).first()
        if existing is not None:
            raise HTTPException(status_code=409, detail="Esta categoría del catálogo IPTC ya existe")

        canonical_name = IPTC_CODE_TO_NAME[iptc_code]
        category = Category(id=category_id, name=canonical_name, source=payload.source, code=iptc_code)
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
            new_name = data["name"].strip()
            iptc_code = IPTC_CATALOG.get(new_name.lower())
            if iptc_code is None:
                raise HTTPException(
                    status_code=422,
                    detail=f"El nombre '{new_name}' no pertenece al catálogo IPTC cerrado",
                )
            canonical_name = IPTC_CODE_TO_NAME[iptc_code]
            category.name = canonical_name
            category.code = iptc_code
        if "source" in data:
            category.source = data["source"]

        self.db.commit()
        self.db.refresh(category)
        return CategoryResponse(id=category.id, name=category.name, source=category.source)

    def delete_category(self, category_id: int) -> None:
        category = self._get_category_or_404(category_id)
        self.db.query(RSSChannel).filter(
            RSSChannel.category_id == category_id
        ).delete(synchronize_session=False)
        self.db.delete(category)
        self.db.commit()

    def _get_category_or_404(self, category_id: int) -> Category:
        category = self.db.query(Category).filter(Category.id == category_id).first()
        if category is None:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        return category
