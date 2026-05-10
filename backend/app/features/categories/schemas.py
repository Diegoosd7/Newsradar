from typing import Optional
from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    source: str = Field(..., pattern="^IPTC$")
    code: Optional[str] = Field(default=None, max_length=8)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=120)
    source: Optional[str] = Field(None, pattern="^IPTC$")
    code: Optional[str] = Field(None, max_length=8)


class CategoryResponse(BaseModel):
    id: int
    name: str
    source: str
