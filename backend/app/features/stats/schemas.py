from typing import List, Optional
from pydantic import BaseModel, Field
from ...core.shared_schemas import MetricModel


class StatsBase(BaseModel):
    metrics: List[MetricModel] = Field(default_factory=list)


class StatsCreate(StatsBase):
    pass


class StatsUpdate(BaseModel):
    metrics: Optional[List[MetricModel]] = None


class StatsResponse(StatsBase):
    id: int
