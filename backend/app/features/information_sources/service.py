from typing import List
from sqlalchemy.orm import Session
from app.db.models import InformationSource
from .schemas import (
    InformationSourceResponse,
    InformationSourceCreate,
    InformationSourceUpdate,
)
from ...core.common_service import CommonService


class InformationSourcesService(CommonService):
    def __init__(self, db: Session):
        super().__init__(db)

    def list_information_sources(self) -> List[InformationSourceResponse]:
        pass

    def create_information_source(self, payload: InformationSourceCreate) -> InformationSourceResponse:
        # Convertimos la URL de Pydantic a string para la BD
        new_source = InformationSource(
            name=payload.name, 
            url=str(payload.url)
        )
        self.db.add(new_source)
        self.db.commit()
        self.db.refresh(new_source)
        return new_source

    def get_information_source(self, source_id: int) -> InformationSourceResponse:
        pass

    def update_information_source(
        self,
        source_id: int,
        payload: InformationSourceUpdate,
    ) -> InformationSourceResponse:
        pass

    def delete_information_source(self, source_id: int) -> None:
        pass
