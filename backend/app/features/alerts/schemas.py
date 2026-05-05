from typing import List, Optional
from pydantic import BaseModel, Field


class AlertCategoryItem(BaseModel):
    code: str = Field(..., min_length=1, max_length=60, example="04000000")
    label: str = Field(..., min_length=1, max_length=120, example="Economía, negocios y finanzas")


class AlertBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, example="Alerta economía")
    descriptors: List[str] = Field(..., min_length=1, example=["economía", "inflación", "PIB"])
    categories: List[AlertCategoryItem] = Field(default_factory=list)
    rss_channels_ids: List[str] = Field(default_factory=list)
    information_sources_ids: List[str] = Field(default_factory=list)
    cron_expression: str = Field(..., min_length=1, max_length=120, example="* * * * *")


class AlertCreate(AlertBase):
    pass


class AlertUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    descriptors: Optional[List[str]] = None
    categories: Optional[List[AlertCategoryItem]] = None
    rss_channels_ids: List[str] = Field(default_factory=list)
    information_sources_ids: List[str] = Field(default_factory=list)
    cron_expression: Optional[str] = Field(None, min_length=1, max_length=120)


class AlertResponse(AlertBase):
    id: int
    user_id: int


class KeywordSuggestionRequest(BaseModel):
    keyword: str = Field(..., min_length=1, max_length=100, description="Palabra clave original")


class KeywordSuggestionResponse(BaseModel):
    suggestions: List[str] = Field(..., description="Lista de 3 a 10 sinónimos o palabras relacionadas")