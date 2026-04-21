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


class CategoryCountItem(BaseModel):
    category_code: str
    category_label: str
    count: int


class TrendingWordItem(BaseModel):
    text: str
    value: int


class TrendingCategoryItem(BaseModel):
    category_code: str
    category_label: str
    words: List[TrendingWordItem]


class DashboardSummary(BaseModel):
    sources: int
    rss_channels: int
    news: int
    alerts: int


class DashboardStatsResponse(BaseModel):
    summary: DashboardSummary
    news_by_category: List[CategoryCountItem]
    alerts_by_category: List[CategoryCountItem]
    trending_by_category: List[TrendingCategoryItem]