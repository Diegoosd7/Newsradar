from typing import List
from sqlalchemy.orm import Session
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

    def create_information_source(
        self,
        payload: InformationSourceCreate,
    ) -> InformationSourceResponse:
        pass

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
