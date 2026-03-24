from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ...db.models import InformationSource, RSSChannel
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
        sources = self.db.query(InformationSource).all()
        return [
            InformationSourceResponse(id=source.id, name=source.name, url=source.url)
            for source in sources
        ]

    def create_information_source(self, payload: InformationSourceCreate) -> InformationSourceResponse:
        # Convertimos la URL de Pydantic a string para la BD
        new_source = InformationSource(
            name=payload.name, 
            url=str(payload.url)
        )
        self.db.add(new_source)
        self.db.commit()
        self.db.refresh(new_source)
        return InformationSourceResponse(id=new_source.id, name=new_source.name, url=new_source.url)

    def get_information_source(self, source_id: int) -> InformationSourceResponse:
        source = self._get_source_or_404(source_id)
        return InformationSourceResponse(id=source.id, name=source.name, url=source.url)

    def update_information_source(
        self,
        source_id: int,
        payload: InformationSourceUpdate,
    ) -> InformationSourceResponse:
        source = self._get_source_or_404(source_id)
        data = payload.model_dump(exclude_unset=True)

        if "name" in data:
            source.name = data["name"]
        if "url" in data:
            source.url = str(data["url"])

        self.db.commit()
        self.db.refresh(source)
        return InformationSourceResponse(id=source.id, name=source.name, url=source.url)

    def delete_information_source(self, source_id: int) -> None:
        source = self._get_source_or_404(source_id)
        (
            self.db.query(RSSChannel)
            .filter(RSSChannel.information_source_id == source_id)
            .delete(synchronize_session=False)
        )
        self.db.delete(source)
        self.db.commit()

    def _get_source_or_404(self, source_id: int) -> InformationSource:
        source = self.db.query(InformationSource).filter(InformationSource.id == source_id).first()
        if source is None:
            raise HTTPException(status_code=404, detail="Fuente de información no encontrada")
        return source
