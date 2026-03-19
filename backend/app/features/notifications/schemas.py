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
