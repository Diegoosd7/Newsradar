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
from ...core.url_validation import validate_url_safety


def _normalize_url(url: str) -> str:
    normalized = str(url).strip().lower().rstrip("/")
    return normalized


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
        url_str = str(payload.url)
        validate_url_safety(url_str)

        normalized_url = _normalize_url(url_str)

        existing_by_name = self.db.query(InformationSource).filter(
            InformationSource.name == payload.name
        ).first()
        if existing_by_name is not None:
            raise HTTPException(status_code=409, detail="Ya existe una fuente con ese nombre")

        existing_sources = self.db.query(InformationSource).all()
        for src in existing_sources:
            if _normalize_url(src.url) == normalized_url:
                raise HTTPException(status_code=409, detail="Ya existe una fuente con esa URL")

        new_source = InformationSource(
            name=payload.name,
            url=url_str,
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

        if "url" in data:
            new_url = str(data["url"])
            validate_url_safety(new_url)
            normalized_new = _normalize_url(new_url)
            existing_sources = self.db.query(InformationSource).filter(
                InformationSource.id != source_id
            ).all()
            for src in existing_sources:
                if _normalize_url(src.url) == normalized_new:
                    raise HTTPException(status_code=409, detail="Ya existe una fuente con esa URL")
            source.url = new_url

        if "name" in data:
            source.name = data["name"]

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
