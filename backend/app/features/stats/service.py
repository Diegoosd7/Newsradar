from typing import List
from sqlalchemy.orm import Session
from .schemas import StatsResponse, StatsCreate, StatsUpdate
from ...core.common_service import CommonService


class StatsService(CommonService):
    def __init__(self, db: Session):
        super().__init__(db)

    def list_stats(self) -> List[StatsResponse]:
        pass

    def create_stats(
        self,
        payload: StatsCreate,
    ) -> StatsResponse:
        pass

    def get_stats(
        self,
        stats_id: int,
    ) -> StatsResponse:
        pass

    def update_stats(
        self,
        stats_id: int,
        payload: StatsUpdate,
    ) -> StatsResponse:
        pass

    def delete_stats(
        self,
        stats_id: int,
    ) -> None:
        pass
