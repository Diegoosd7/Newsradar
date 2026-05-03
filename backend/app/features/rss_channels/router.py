from typing import List
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from .schemas import RSSChannelResponse, RSSChannelCreate, RSSChannelUpdate
from .service import RSSChannelService
from ...db.database import get_db
from ...core.security import get_current_user
from ...core.shared_schemas import UserInDB

router = APIRouter(tags=["rss-channels"])


def get_rss_channels_service(db: Session = Depends(get_db)):
    return RSSChannelService(db)


@router.get(
    "/rss-channels",
    response_model=List[RSSChannelResponse],
    tags=["rss-channels"],
)
def list_rss_channels(
    _: UserInDB = Depends(get_current_user),
    service: RSSChannelService = Depends(get_rss_channels_service),
) -> List[RSSChannelResponse]:
    return service.list_rss_channels()


@router.get(
    "/information-sources/{source_id}/rss-channels",
    response_model=List[RSSChannelResponse],
    tags=["rss-channels"],
)
def list_source_channels(
    source_id: int,
    _: UserInDB = Depends(get_current_user),
    service: RSSChannelService = Depends(get_rss_channels_service),
) -> List[RSSChannelResponse]:
    return service.list_source_channels(source_id)


@router.post(
    "/information-sources/{source_id}/rss-channels",
    response_model=RSSChannelResponse,
    status_code=201,
    tags=["rss-channels"],
)
def create_source_channel(
    source_id: int,
    payload: RSSChannelCreate,
    _: UserInDB = Depends(get_current_user),
    service: RSSChannelService = Depends(get_rss_channels_service),
) -> RSSChannelResponse:
    return service.create_source_channel(source_id, payload)


@router.get(
    "/information-sources/{source_id}/rss-channels/{channel_id}",
    response_model=RSSChannelResponse,
    tags=["rss-channels"],
)
def get_source_channel(
    source_id: int,
    channel_id: int,
    _: UserInDB = Depends(get_current_user),
    service: RSSChannelService = Depends(get_rss_channels_service),
) -> RSSChannelResponse:
    return service.get_source_channel(source_id, channel_id)


@router.put(
    "/information-sources/{source_id}/rss-channels/{channel_id}",
    response_model=RSSChannelResponse,
    tags=["rss-channels"],
)
def update_source_channel(
    source_id: int,
    channel_id: int,
    payload: RSSChannelUpdate,
    _: UserInDB = Depends(get_current_user),
    service: RSSChannelService = Depends(get_rss_channels_service),
) -> RSSChannelResponse:
    return service.update_source_channel(source_id, channel_id, payload)


@router.delete(
    "/information-sources/{source_id}/rss-channels/{channel_id}",
    status_code=204,
    response_model=None,
    response_class=Response,
    tags=["rss-channels"],
)
def delete_source_channel(
    source_id: int,
    channel_id: int,
    _: UserInDB = Depends(get_current_user),
    service: RSSChannelService = Depends(get_rss_channels_service),
) -> None:
    return service.delete_source_channel(source_id, channel_id)