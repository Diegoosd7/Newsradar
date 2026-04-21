from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from .schemas import RSSChannelResponse, RSSChannelCreate, RSSChannelUpdate
from ...core.common_service import CommonService
from ...db.models import RSSChannel, InformationSource, Category


class RSSChannelService(CommonService):
    def __init__(self, db: Session):
        super().__init__(db)

    def list_rss_channels(self) -> List[RSSChannelResponse]:
        channels = self.db.query(RSSChannel).all()
        return [
            RSSChannelResponse(
                id=channel.id,
                information_source_id=channel.information_source_id,
                category_id=channel.category_id,
                url=channel.url,
            )
            for channel in channels
        ]

    def list_source_channels(
        self,
        source_id: int,
    ) -> List[RSSChannelResponse]:
        self._ensure_information_source_exists(source_id)
        channels = (
            self.db.query(RSSChannel)
            .filter(RSSChannel.information_source_id == source_id)
            .all()
        )
        return [
            RSSChannelResponse(
                id=channel.id,
                information_source_id=channel.information_source_id,
                category_id=channel.category_id,
                url=channel.url,
            )
            for channel in channels
        ]

    def create_source_channel(self, source_id: int, payload: RSSChannelCreate) -> RSSChannelResponse:
        self._ensure_information_source_exists(source_id)
        self._ensure_category_exists(payload.category_id)

        new_channel = RSSChannel(
            information_source_id=source_id,
            category_id=payload.category_id,
            url=str(payload.url)
        )
        self.db.add(new_channel)
        self.db.commit()
        self.db.refresh(new_channel)
        return RSSChannelResponse(
            id=new_channel.id,
            information_source_id=new_channel.information_source_id,
            category_id=new_channel.category_id,
            url=new_channel.url,
        )

    def get_source_channel(
        self,
        source_id: int,
        channel_id: int,
    ) -> RSSChannelResponse:
        self._ensure_information_source_exists(source_id)
        channel = self._get_channel_for_source_or_404(source_id, channel_id)
        return RSSChannelResponse(
            id=channel.id,
            information_source_id=channel.information_source_id,
            category_id=channel.category_id,
            url=channel.url,
        )

    def update_source_channel(
        self,
        source_id: int,
        channel_id: int,
        payload: RSSChannelUpdate,
    ) -> RSSChannelResponse:
        self._ensure_information_source_exists(source_id)
        channel = self._get_channel_for_source_or_404(source_id, channel_id)
        data = payload.model_dump(exclude_unset=True)

        if "category_id" in data:
            self._ensure_category_exists(data["category_id"])
            channel.category_id = data["category_id"]
        if "url" in data:
            channel.url = str(data["url"])

        self.db.commit()
        self.db.refresh(channel)
        return RSSChannelResponse(
            id=channel.id,
            information_source_id=channel.information_source_id,
            category_id=channel.category_id,
            url=channel.url,
        )

    def delete_source_channel(
        self,
        source_id: int,
        channel_id: int,
    ) -> None:
        self._ensure_information_source_exists(source_id)
        channel = self._get_channel_for_source_or_404(source_id, channel_id)
        self.db.delete(channel)
        self.db.commit()

    def _ensure_information_source_exists(self, source_id: int) -> None:
        source = (
            self.db.query(InformationSource)
            .filter(InformationSource.id == source_id)
            .first()
        )
        if source is None:
            raise HTTPException(status_code=404, detail="Fuente de información no encontrada")

    def _ensure_category_exists(self, category_id: int) -> None:
        category = self.db.query(Category).filter(Category.id == category_id).first()
        if category is None:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")

    def _get_channel_for_source_or_404(self, source_id: int, channel_id: int) -> RSSChannel:
        channel = (
            self.db.query(RSSChannel)
            .filter(
                RSSChannel.id == channel_id,
                RSSChannel.information_source_id == source_id,
            )
            .first()
        )
        if channel is None:
            raise HTTPException(status_code=404, detail="Canal RSS no encontrado para la fuente")
        return channel