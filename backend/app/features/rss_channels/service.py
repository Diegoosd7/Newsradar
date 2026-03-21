from typing import List
from sqlalchemy.orm import Session
from .schemas import RSSChannelResponse, RSSChannelCreate, RSSChannelUpdate
from ...core.common_service import CommonService
from app.db.models import RSSChannel


class RSSChannelService(CommonService):
    def __init__(self, db: Session):
        super().__init__(db)

    def list_source_channels(
        self,
        source_id: int,
    ) -> List[RSSChannelResponse]:
        pass

    def create_source_channel(self, source_id: int, payload: RSSChannelCreate) -> RSSChannelResponse:
        new_channel = RSSChannel(
            information_source_id=source_id,
            category_id=payload.category_id,
            url=str(payload.url)
        )
        self.db.add(new_channel)
        self.db.commit()
        self.db.refresh(new_channel)
        return new_channel

    def get_source_channel(
        self,
        source_id: int,
        channel_id: int,
    ) -> RSSChannelResponse:
        pass

    def update_source_channel(
        self,
        source_id: int,
        channel_id: int,
        payload: RSSChannelUpdate,
    ) -> RSSChannelResponse:
        pass

    def delete_source_channel(
        self,
        source_id: int,
        channel_id: int,
    ) -> None:
        pass
