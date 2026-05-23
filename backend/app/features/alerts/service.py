import os
import json
import re
import google.generativeai as genai
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from .schemas import AlertResponse, AlertCreate, AlertUpdate
from ...core.common_service import CommonService
from ...core.scheduler import register_alert_job, update_alert_job, remove_alert_job
from ...db.models import (
    User,
    Alert,
    Descriptor,
    AlertCategoryItem,
    CrossAlertDescriptor,
    CrossAlertAlertCategoryItem,
    CrossAlertRSSChannel,
    CrossAlertInformationSource,
    InformationSource,
    RSSChannel,
    Notification,
)

_WORD_RE = re.compile(r"[a-záéíóúñüàèìòùâêîôûäëïöü]{3,}", re.IGNORECASE)
_GENERIC_DESCRIPTORS = [
    "noticias", "información", "actualidad", "análisis", "novedades",
    "eventos", "tendencias", "informe", "resumen", "datos",
]


def _expand_descriptors(descriptors: List[str], alert_name: str) -> List[str]:
    seen: set[str] = set()
    result: List[str] = []

    def _add(word: str) -> None:
        key = word.strip().lower()
        if key and key not in seen:
            seen.add(key)
            result.append(word.strip())

    for d in descriptors:
        _add(d)

    if len(result) < 3:
        for word in _WORD_RE.findall(alert_name):
            _add(word)

    if len(result) < 3:
        for generic in _GENERIC_DESCRIPTORS:
            if len(result) >= 3:
                break
            _add(generic)

    return result[:10]


class AlertsService(CommonService):
    def __init__(self, db: Session):
        super().__init__(db)

    def suggest_keywords_with_ai(self, keyword: str) -> List[str]:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="Falta la API Key de Gemini en el entorno.")

        try:
            genai.configure(api_key=api_key)

            valid_model_name = None
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    valid_model_name = m.name
                    break

            if not valid_model_name:
                raise HTTPException(status_code=500, detail="Tu cuenta de Google no tiene acceso a ningún modelo de texto.")

            model = genai.GenerativeModel(valid_model_name)

            prompt = f"""
            Actúa como un experto lingüista. Para la palabra clave '{keyword}',
            proporciona entre 3 y 10 sinónimos o palabras estrechamente relacionadas.
            Devuelve ÚNICAMENTE un array en formato JSON con las palabras, sin texto adicional ni formato markdown.
            Ejemplo: ["palabra1", "palabra2", "palabra3"]
            """

            response = model.generate_content(prompt)
            cleaned_text = response.text.replace("```json", "").replace("```", "").strip()
            try:
                suggestions = json.loads(cleaned_text)
            except json.JSONDecodeError:
                start = cleaned_text.find("[")
                end = cleaned_text.rfind("]")
                if start != -1 and end != -1 and end > start:
                    suggestions = json.loads(cleaned_text[start : end + 1])
                else:
                    raise HTTPException(status_code=500, detail="La IA no devolvió JSON válido.")

            if not isinstance(suggestions, list):
                raise HTTPException(status_code=500, detail="La IA no devolvió una lista JSON.")

            suggestions = [str(x).strip() for x in suggestions if str(x).strip()]

            seen = set()
            deduped = []
            for x in suggestions:
                key = x.lower()
                if key not in seen:
                    seen.add(key)
                    deduped.append(x)
            suggestions = deduped

            suggestions = suggestions[:10]

            if len(suggestions) < 3:
                raise HTTPException(status_code=500, detail="La IA devolvió menos de 3 sugerencias.")
            return suggestions[:10]

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error comunicándose con la IA: {str(e)}")

    def list_user_alerts(self, user_id: int) -> List[AlertResponse]:
        self._ensure_user_exists(user_id)
        alerts = self.db.query(Alert).filter(Alert.user_id == user_id).all()
        return [self._to_response(alert) for alert in alerts]

    def create_user_alert(self, user_id: int, payload: AlertCreate) -> AlertResponse:
        self._ensure_user_exists(user_id)

        alert_count = self.db.query(Alert).filter(Alert.user_id == user_id).count()
        if alert_count >= 20:
            raise HTTPException(
                status_code=400,
                detail="Límite máximo de 20 alertas alcanzado para este usuario.",
            )

        self._ensure_unique_alert_name(user_id, payload.name)

        if payload.rss_channels_ids:
            self._ensure_rss_channels_exist(payload.rss_channels_ids)
        if payload.information_sources_ids:
            self._ensure_information_sources_exist(payload.information_sources_ids)

        expanded_descriptors = _expand_descriptors(payload.descriptors, payload.name)

        alert = Alert(
            user_id=user_id,
            name=payload.name.strip(),
            cron_expression=payload.cron_expression,
        )
        self.db.add(alert)
        self.db.flush()

        self._replace_descriptors(alert.id, expanded_descriptors)
        self._replace_categories(alert.id, payload.categories)
        self._replace_rss_channels(alert.id, payload.rss_channels_ids)
        self._replace_information_sources(alert.id, payload.information_sources_ids)

        self.db.commit()
        self.db.refresh(alert)

        register_alert_job(alert.id, alert.cron_expression)

        return self._to_response(alert)

    def get_user_alert(self, user_id: int, alert_id: int) -> AlertResponse:
        alert = self._get_alert_for_user_or_404(user_id, alert_id)
        return self._to_response(alert)

    def update_user_alert(
        self,
        user_id: int,
        alert_id: int,
        payload: AlertUpdate,
    ) -> AlertResponse:
        alert = self._get_alert_for_user_or_404(user_id, alert_id)
        data = payload.model_dump(exclude_unset=True)

        if "name" in data:
            self._ensure_unique_alert_name(user_id, data["name"], exclude_alert_id=alert_id)
            alert.name = data["name"].strip()
        if "cron_expression" in data:
            alert.cron_expression = data["cron_expression"]
        if "descriptors" in data:
            expanded = _expand_descriptors(data["descriptors"], alert.name)
            self._replace_descriptors(alert_id, expanded)
        if "categories" in data:
            self._replace_categories(alert_id, data["categories"])
        if "rss_channels_ids" in data:
            self._ensure_rss_channels_exist(data["rss_channels_ids"])
            self._replace_rss_channels(alert_id, data["rss_channels_ids"])
        if "information_sources_ids" in data:
            self._ensure_information_sources_exist(data["information_sources_ids"])
            self._replace_information_sources(alert_id, data["information_sources_ids"])

        self.db.commit()
        self.db.refresh(alert)

        if "cron_expression" in data:
            update_alert_job(alert.id, alert.cron_expression)

        return self._to_response(alert)

    def delete_user_alert(self, user_id, alert_id) -> None:
        self._get_alert_for_user_or_404(user_id, alert_id)

        remove_alert_job(alert_id)

        self.db.query(Notification).filter(
            Notification.alert_id == alert_id
        ).delete(synchronize_session=False)

        self.db.query(CrossAlertDescriptor).filter(
            CrossAlertDescriptor.alert_id == alert_id
        ).delete(synchronize_session=False)

        self.db.query(CrossAlertAlertCategoryItem).filter(
            CrossAlertAlertCategoryItem.alert_id == alert_id
        ).delete(synchronize_session=False)

        self.db.query(CrossAlertRSSChannel).filter(
            CrossAlertRSSChannel.alert_id == alert_id
        ).delete(synchronize_session=False)

        self.db.query(CrossAlertInformationSource).filter(
            CrossAlertInformationSource.alert_id == alert_id
        ).delete(synchronize_session=False)

        self.db.query(Alert).filter(Alert.id == alert_id).delete(
            synchronize_session=False
        )
        self.db.commit()

    def _ensure_user_exists(self, user_id: int) -> User:
        user = self.db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user

    def _ensure_unique_alert_name(
        self, user_id: int, name: str, exclude_alert_id: int | None = None
    ) -> None:
        normalized = name.strip().lower()
        alerts = self.db.query(Alert).filter(Alert.user_id == user_id).all()
        for alert in alerts:
            if exclude_alert_id is not None and alert.id == exclude_alert_id:
                continue
            if alert.name.strip().lower() == normalized:
                raise HTTPException(
                    status_code=409,
                    detail="Ya existe una alerta con ese nombre para este usuario",
                )

    def _ensure_rss_channels_exist(self, channel_ids: List[int]) -> None:
        found = self.db.query(RSSChannel.id).filter(RSSChannel.id.in_(channel_ids)).all()
        found_ids = {cid for (cid,) in found}
        missing = [cid for cid in channel_ids if cid not in found_ids]
        if missing:
            raise HTTPException(
                status_code=422,
                detail=f"Canales RSS no encontrados: {missing}",
            )

    def _ensure_information_sources_exist(self, source_ids: List[int]) -> None:
        found = self.db.query(InformationSource.id).filter(InformationSource.id.in_(source_ids)).all()
        found_ids = {sid for (sid,) in found}
        missing = [sid for sid in source_ids if sid not in found_ids]
        if missing:
            raise HTTPException(
                status_code=422,
                detail=f"Fuentes de información no encontradas: {missing}",
            )

    def _get_alert_for_user_or_404(self, user_id: int, alert_id: int) -> Alert:
        self._ensure_user_exists(user_id)
        alert = (
            self.db.query(Alert)
            .filter(Alert.id == alert_id, Alert.user_id == user_id)
            .first()
        )
        if alert is None:
            raise HTTPException(
                status_code=404, detail="Alerta no encontrada para el usuario"
            )
        return alert

    def _replace_descriptors(self, alert_id: int, descriptors: List[str]) -> None:
        self.db.query(CrossAlertDescriptor).filter(
            CrossAlertDescriptor.alert_id == alert_id
        ).delete(synchronize_session=False)

        for descriptor_name in descriptors:
            descriptor = (
                self.db.query(Descriptor)
                .filter(Descriptor.name == descriptor_name)
                .first()
            )
            if descriptor is None:
                descriptor = Descriptor(name=descriptor_name)
                self.db.add(descriptor)
                self.db.flush()

            self.db.add(
                CrossAlertDescriptor(alert_id=alert_id, descriptor_id=descriptor.id)
            )

    def _replace_rss_channels(self, alert_id: int, channel_ids: List[int]) -> None:
        self.db.query(CrossAlertRSSChannel).filter(
            CrossAlertRSSChannel.alert_id == alert_id
        ).delete(synchronize_session=False)

        seen: set[int] = set()
        for channel_id in channel_ids or []:
            if channel_id in seen:
                continue
            seen.add(channel_id)
            self.db.add(
                CrossAlertRSSChannel(alert_id=alert_id, rss_channel_id=channel_id)
            )

    def _replace_information_sources(self, alert_id: int, source_ids: List[int]) -> None:
        self.db.query(CrossAlertInformationSource).filter(
            CrossAlertInformationSource.alert_id == alert_id
        ).delete(synchronize_session=False)

        seen: set[int] = set()
        for source_id in source_ids or []:
            if source_id in seen:
                continue
            seen.add(source_id)
            self.db.add(
                CrossAlertInformationSource(
                    alert_id=alert_id, information_source_id=source_id
                )
            )

    def _replace_categories(self, alert_id: int, categories: List[dict]) -> None:
        self.db.query(CrossAlertAlertCategoryItem).filter(
            CrossAlertAlertCategoryItem.alert_id == alert_id
        ).delete(synchronize_session=False)

        for category in categories:
            code = category.code if hasattr(category, "code") else category["code"]
            label = category.label if hasattr(category, "label") else category["label"]
            category_item = (
                self.db.query(AlertCategoryItem)
                .filter(
                    AlertCategoryItem.code == code,
                    AlertCategoryItem.label == label,
                )
                .first()
            )
            if category_item is None:
                category_item = AlertCategoryItem(code=code, label=label)
                self.db.add(category_item)
                self.db.flush()

            self.db.add(
                CrossAlertAlertCategoryItem(
                    alert_id=alert_id,
                    alert_category_item_id=category_item.id,
                )
            )

    def _to_response(self, alert: Alert) -> AlertResponse:
        descriptors = [
            name
            for (name,) in (
                self.db.query(Descriptor.name)
                .join(
                    CrossAlertDescriptor,
                    CrossAlertDescriptor.descriptor_id == Descriptor.id,
                )
                .filter(CrossAlertDescriptor.alert_id == alert.id)
                .all()
            )
        ]

        categories = [
            {"code": code, "label": label}
            for code, label in (
                self.db.query(AlertCategoryItem.code, AlertCategoryItem.label)
                .join(
                    CrossAlertAlertCategoryItem,
                    CrossAlertAlertCategoryItem.alert_category_item_id == AlertCategoryItem.id,
                )
                .filter(CrossAlertAlertCategoryItem.alert_id == alert.id)
                .all()
            )
        ]

        rss_channels_ids = [
            cid
            for (cid,) in (
                self.db.query(CrossAlertRSSChannel.rss_channel_id)
                .filter(CrossAlertRSSChannel.alert_id == alert.id)
                .all()
            )
        ]

        information_sources_ids = [
            sid
            for (sid,) in (
                self.db.query(CrossAlertInformationSource.information_source_id)
                .filter(CrossAlertInformationSource.alert_id == alert.id)
                .all()
            )
        ]

        return AlertResponse(
            id=alert.id,
            user_id=alert.user_id,
            name=alert.name,
            cron_expression=alert.cron_expression,
            descriptors=descriptors,
            categories=categories,
            rss_channels_ids=rss_channels_ids,
            information_sources_ids=information_sources_ids,
        )
