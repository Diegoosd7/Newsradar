from __future__ import annotations

import re
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator

# IPTC catalog: mapping from normalized name to (code, canonical_name)
IPTC_CATALOG: dict[str, tuple[str, str]] = {
    name.strip().lower(): (code, name)
    for code, name in [
        ("01000000", "Artes, cultura, entretenimiento y medios"),
        ("03000000", "Catástrofes y accidentes"),
        ("13000000", "Ciencia y tecnología"),
        ("16000000", "Conflicto, guerra y paz"),
        ("15000000", "Deporte"),
        ("04000000", "Economía, negocios y finanzas"),
        ("05000000", "Educación"),
        ("10000000", "Estilo de vida y tiempo libre"),
        ("08000000", "Interés humano, animales, insólito"),
        ("09000000", "Mano de obra"),
        ("06000000", "Medio ambiente"),
        ("17000000", "Meteorología"),
        ("02000000", "Policía y justicia"),
        ("11000000", "Política"),
        ("12000000", "Religión y culto"),
        ("07000000", "Salud"),
        ("14000000", "Sociedad"),
    ]
}

# Mapping code → canonical name
IPTC_CODE_TO_NAME: dict[str, str] = {
    code: name for _, (code, name) in IPTC_CATALOG.items()
}

_CRON_FIELD_RE = re.compile(
    r"^(\*|(\d{1,2})([-,]\d{1,2})*(\/\d{1,2})?)$"
)


def _is_valid_cron(expression: str) -> bool:
    parts = expression.strip().split()
    if len(parts) != 5:
        return False
    for part in parts:
        if not re.match(r'^[\d\*\/\-\,]+$', part):
            return False
    return True


class AlertCategoryItem(BaseModel):
    code: str = Field(..., min_length=1, max_length=60, example="04000000")
    label: str = Field(..., min_length=1, max_length=120, example="Economía, negocios y finanzas")


class AlertBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, example="Alerta economía")
    descriptors: List[str] = Field(default_factory=list, example=["economía", "inflación", "PIB"])
    categories: List[AlertCategoryItem] = Field(default_factory=list)
    rss_channels_ids: List[int] = Field(default_factory=list)
    information_sources_ids: List[int] = Field(default_factory=list)
    cron_expression: str = Field(..., min_length=1, max_length=120, example="* * * * *")

    @field_validator("cron_expression")
    @classmethod
    def validate_cron(cls, v: str) -> str:
        if not _is_valid_cron(v):
            raise ValueError(
                "cron_expression must be a valid 5-field cron expression (e.g. '0 9 * * 1-5')"
            )
        return v

    @field_validator("categories")
    @classmethod
    def validate_categories(cls, v: List[AlertCategoryItem]) -> List[AlertCategoryItem]:
        if len(v) > 1:
            raise ValueError("Se permite como máximo una categoría por alerta")

        seen_codes = set()
        for item in v:
            if item.code in seen_codes:
                raise ValueError(f"Categoría duplicada: {item.code}")
            seen_codes.add(item.code)

            expected_name = IPTC_CODE_TO_NAME.get(item.code)
            if expected_name is None:
                raise ValueError(f"Código de categoría no reconocido en catálogo IPTC: {item.code}")

            if item.label.strip().lower() != expected_name.strip().lower():
                raise ValueError(
                    f"El label '{item.label}' no corresponde al código IPTC '{item.code}' "
                    f"(esperado: '{expected_name}')"
                )

        return v

    @field_validator("descriptors")
    @classmethod
    def validate_descriptors(cls, v: List[str]) -> List[str]:
        seen: set[str] = set()
        for d in v:
            key = d.strip().lower()
            if key in seen:
                raise ValueError(f"Descriptor duplicado: '{d}'")
            seen.add(key)
        return v

    @field_validator("rss_channels_ids")
    @classmethod
    def validate_rss_channels_ids(cls, v: List[int]) -> List[int]:
        if len(v) != len(set(v)):
            raise ValueError("rss_channels_ids contiene identificadores duplicados")
        return v

    @field_validator("information_sources_ids")
    @classmethod
    def validate_information_sources_ids(cls, v: List[int]) -> List[int]:
        if len(v) != len(set(v)):
            raise ValueError("information_sources_ids contiene identificadores duplicados")
        return v


class AlertCreate(AlertBase):
    pass


class AlertUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    descriptors: Optional[List[str]] = None
    categories: Optional[List[AlertCategoryItem]] = None
    rss_channels_ids: List[int] = Field(default_factory=list)
    information_sources_ids: List[int] = Field(default_factory=list)
    cron_expression: Optional[str] = Field(None, min_length=1, max_length=120)

    @field_validator("cron_expression")
    @classmethod
    def validate_cron(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not _is_valid_cron(v):
            raise ValueError(
                "cron_expression must be a valid 5-field cron expression (e.g. '0 9 * * 1-5')"
            )
        return v

    @field_validator("categories")
    @classmethod
    def validate_categories(cls, v: Optional[List[AlertCategoryItem]]) -> Optional[List[AlertCategoryItem]]:
        if v is None:
            return v
        if len(v) > 1:
            raise ValueError("Se permite como máximo una categoría por alerta")

        seen_codes = set()
        for item in v:
            if item.code in seen_codes:
                raise ValueError(f"Categoría duplicada: {item.code}")
            seen_codes.add(item.code)

            expected_name = IPTC_CODE_TO_NAME.get(item.code)
            if expected_name is None:
                raise ValueError(f"Código de categoría no reconocido en catálogo IPTC: {item.code}")

            if item.label.strip().lower() != expected_name.strip().lower():
                raise ValueError(
                    f"El label '{item.label}' no corresponde al código IPTC '{item.code}'"
                )

        return v


class AlertResponse(BaseModel):
    id: int
    user_id: int
    name: str
    descriptors: List[str] = Field(default_factory=list)
    categories: List[AlertCategoryItem] = Field(default_factory=list)
    rss_channels_ids: List[int] = Field(default_factory=list)
    information_sources_ids: List[int] = Field(default_factory=list)
    cron_expression: str


class KeywordSuggestionRequest(BaseModel):
    keyword: str = Field(..., min_length=1, max_length=100, description="Palabra clave original")


class KeywordSuggestionResponse(BaseModel):
    suggestions: List[str] = Field(..., description="Lista de 3 a 10 sinónimos o palabras relacionadas")
