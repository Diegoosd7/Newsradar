from typing import List, Optional
from pydantic import BaseModel, Field
from ...core.shared_schemas import MetricModel
from datetime import datetime


class NotificationBase(BaseModel):
    timestamp: datetime
    metrics: List[MetricModel] = Field(default_factory=list)


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(BaseModel):
    timestamp: Optional[datetime] = None
    metrics: Optional[List[MetricModel]] = None


class NotificationResponse(NotificationBase):
    id: int
    alert_id: int
    news_item_id: Optional[int] = None
    matched_descriptor: Optional[str] = None
    is_read: bool = False
    news_title: Optional[str] = None
    news_summary: Optional[str] = None
    news_url: Optional[str] = None
    news_published: Optional[datetime] = None
    source_name: Optional[str] = None
