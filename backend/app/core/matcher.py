# app/core/matcher.py
#
# Responsabilidad única: determinar si una noticia es candidata para una
# alerta comparando su contenido con la lista de descriptores de esa alerta.
#
# Por qué este módulo existe en /core y no en /features/alerts:
#   La lógica de matching no pertenece a ninguna feature concreta — es
#   infraestructura transversal que el monitor usa para evaluar todas las
#   alertas. Colocarlo en /core comunica esa intención claramente y evita
#   dependencias circulares (alerts importando de alerts).
#
# Decisión de diseño (ver ADR-003):
#   Se usa búsqueda de subcadena case-insensitive sobre título + resumen.
#   No se usa spaCy ni lematización en este sprint por dos razones:
#     1. El enunciado dice "que contenga las palabras" — matching literal.
#     2. spaCy requiere descargar modelos de idioma en el build de Docker,
#        lo que puede romper el despliegue automático en máquina limpia.
#   Si en el futuro se quiere matching semántico, este módulo es el único
#   punto a modificar — el resto del sistema no cambia.

import logging
import re
from dataclasses import dataclass
from typing import List, Optional

from app.features.rss_channels.fetcher import NewsItemData

logger = logging.getLogger(__name__)


@dataclass
class MatchResult:
    """
    Resultado de evaluar una noticia contra los descriptores de una alerta.

    Campos:
        matched         — True si al menos un descriptor hizo match.
        matched_descriptor — El primer descriptor que produjo el match.
                             None si matched=False.
                             Se guarda en Notification.matched_descriptor
                             para el asunto del email:
                             "Actualización de <alerta> en <día/hora>".
        news_item       — La noticia evaluada (referencia al mismo objeto
                          recibido, sin copiar datos).
    """
    matched: bool
    matched_descriptor: Optional[str]
    news_item: NewsItemData


def match_news_against_descriptors(
    news_item: NewsItemData,
    descriptors: List[str],
) -> MatchResult:
    """
    Evalúa si una noticia contiene alguno de los descriptores dados.

    El texto donde se busca es la concatenación de título y resumen,
    normalizado a minúsculas. Cada descriptor se busca como palabra
    completa usando una expresión regular con word boundaries (\\b),
    lo que evita falsos positivos como "mar" dentro de "emark" o
    "ia" dentro de "hacia".

    Args:
        news_item:    Noticia a evaluar (NewsItemData del fetcher).
        descriptors:  Lista de strings con las palabras clave de la alerta,
                      incluyendo los sinónimos generados por Gemini.

    Returns:
        MatchResult con matched=True y el descriptor que hizo match,
        o matched=False si ninguno coincide.

    Ejemplos:
        >>> from app.features.rss_channels.fetcher import NewsItemData
        >>> noticia = NewsItemData(
        ...     url="https://ejemplo.com/noticia",
        ...     title="El Banco Central sube los tipos de interés",
        ...     summary="La decisión afecta a las hipotecas variables.",
        ...     published=None,
        ...     channel_id=1,
        ... )
        >>> match_news_against_descriptors(noticia, ["tipos de interés", "inflación"])
        MatchResult(matched=True, matched_descriptor='tipos de interés', ...)
        >>> match_news_against_descriptors(noticia, ["criptomonedas"])
        MatchResult(matched=False, matched_descriptor=None, ...)
    """
    if not descriptors:
        return MatchResult(matched=False, matched_descriptor=None, news_item=news_item)

    # Texto donde buscamos: título + espacio + resumen, todo en minúsculas.
    # El espacio entre ambos evita que una palabra del final del título
    # se "fusione" con el inicio del resumen al concatenar.
    search_text = f"{news_item.title} {news_item.summary}".lower()

    for descriptor in descriptors:
        if not descriptor or not descriptor.strip():
            continue

        descriptor_clean = descriptor.strip().lower()

        # Usamos word boundary (\b) para evitar falsos positivos.
        # re.escape protege descriptores con caracteres especiales
        # (ej: "C++" o "I.A.").
        # Para descriptores de múltiples palabras ("tipos de interés"),
        # \b en los extremos es suficiente.
        pattern = r"\b" + re.escape(descriptor_clean) + r"\b"

        if re.search(pattern, search_text):
            logger.debug(
                "Match encontrado: descriptor '%s' en noticia '%s'",
                descriptor_clean,
                news_item.title[:60],
            )
            return MatchResult(
                matched=True,
                matched_descriptor=descriptor,  # guardamos el original, no el lower
                news_item=news_item,
            )

    return MatchResult(matched=False, matched_descriptor=None, news_item=news_item)


def filter_matching_news(
    news_items: List[NewsItemData],
    descriptors: List[str],
) -> List[MatchResult]:
    """
    Aplica match_news_against_descriptors a una lista de noticias y
    devuelve solo las que han hecho match.

    Esta función es la que llama el monitor en cada ejecución de cron:
    recibe todas las noticias de todos los canales RSS de una alerta
    y filtra las candidatas.

    Args:
        news_items:  Lista de noticias obtenidas por el fetcher.
        descriptors: Lista de descriptores de la alerta.

    Returns:
        Lista de MatchResult donde matched=True. Puede estar vacía.
    """
    results = []
    for item in news_items:
        result = match_news_against_descriptors(item, descriptors)
        if result.matched:
            results.append(result)

    logger.info(
        "Matching completado: %d/%d noticias candidatas con descriptores %s",
        len(results),
        len(news_items),
        descriptors[:3],  # solo los 3 primeros para no saturar el log
    )
    return results