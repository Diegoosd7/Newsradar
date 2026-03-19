from typing import Optional
from pydantic import BaseModel, HttpUrl


class RSSChannelBase(BaseModel):
    url: HttpUrl
    category_id: int


class RSSChannelCreate(RSSChannelBase):
    pass


class RSSChannelUpdate(BaseModel):
    url: Optional[HttpUrl] = None
    category_id: Optional[int] = None


class RSSChannelResponse(RSSChannelBase):
    id: int
    information_source_id: int
