from typing import Optional
from pydantic import BaseModel, Field, field_validator


class RoleBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=80)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if any(ord(c) < 32 for c in v):
            raise ValueError("El nombre contiene caracteres de control no permitidos")
        stripped = v.strip()
        if not stripped:
            raise ValueError("El nombre no puede ser solo espacios en blanco")
        return stripped


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=80)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if any(ord(c) < 32 for c in v):
            raise ValueError("El nombre contiene caracteres de control no permitidos")
        stripped = v.strip()
        if not stripped:
            raise ValueError("El nombre no puede ser solo espacios en blanco")
        return stripped


class RoleResponse(RoleBase):
    id: int
