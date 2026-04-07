import os
import json
import google.generativeai as genai
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from .schemas import AlertResponse, AlertCreate, AlertUpdate
from ...core.common_service import CommonService
from ...db.models import (
    User,
    Alert,
    Descriptor,
    AlertCategoryItem,
    CrossAlertDescriptor,
    CrossAlertAlertCategoryItem,
    Notification,
)


class AlertsService(CommonService):
    def __init__(self, db: Session):
        super().__init__(db)

    def suggest_keywords_with_ai(self, keyword: str) -> List[str]:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="Falta la API Key de Gemini en el entorno.")

        try:
            genai.configure(api_key=api_key)
            
            # 1. Buscar en Google qué modelos tiene disponibles y soportan generación de texto
            valid_model_name = None
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    valid_model_name = m.name
                    break
            
            if not valid_model_name:
                raise HTTPException(status_code=500, detail="Tu cuenta de Google no tiene acceso a ningún modelo de texto.")

            # 2. Usar el modelo
            model = genai.GenerativeModel(valid_model_name) 
            
            prompt = f"""
            Actúa como un experto lingüista. Para la palabra clave '{keyword}', 
            proporciona entre 3 y 10 sinónimos o palabras estrechamente relacionadas.
            Devuelve ÚNICAMENTE un array en formato JSON con las palabras, sin texto adicional ni formato markdown.
            Ejemplo: ["palabra1", "palabra2", "palabra3"]
            """
            
            response = model.generate_content(prompt)
            
            # Limpiamos la respuesta por si la IA mete etiquetas Markdown
            cleaned_text = response.text.replace("```json", "").replace("```", "").strip()
            suggestions = json.loads(cleaned_text)
            
            # Aseguramos que devuelva un máximo de 10
            return suggestions[:10]
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error comunicándose con la IA: {str(e)}")

    def list_user_alerts(self, user_id: int) -> List[AlertResponse]:
        self._ensure_user_exists(user_id)
        alerts = self.db.query(Alert).filter(Alert.user_id == user_id).all()
        return [self._to_response(alert) for alert in alerts]

    def create_user_alert(self, user_id: int, payload: AlertCreate) -> AlertResponse:
        user = self._ensure_user_exists(user_id)

        # Límite de 20 alertas
        alert_count = self.db.query(Alert).filter(Alert.user_id == user_id).count()
        if alert_count >= 20:
            raise HTTPException(status_code=400, detail="Límite máximo de 20 alertas alcanzado para este usuario.")

        alert = Alert(
            user_id=user_id,
            name=payload.name,
            cron_expression=payload.cron_expression,
        )
        self.db.add(alert)
        self.db.flush()

        self._replace_descriptors(alert.id, payload.descriptors)
        self._replace_categories(alert.id, payload.categories)

        self.db.commit()
        self.db.refresh(alert)
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
            alert.name = data["name"]
        if "cron_expression" in data:
            alert.cron_expression = data["cron_expression"]
        if "descriptors" in data:
            self._replace_descriptors(alert_id, data["descriptors"])
        if "categories" in data:
            self._replace_categories(alert_id, data["categories"])

        self.db.commit()
        self.db.refresh(alert)
        return self._to_response(alert)

    def delete_user_alert(self, user_id, alert_id) -> None:
        self._get_alert_for_user_or_404(user_id, alert_id)

        (
            self.db.query(Notification)
            .filter(Notification.alert_id == alert_id)
            .delete(synchronize_session=False)
        )
        (
            self.db.query(CrossAlertDescriptor)
            .filter(CrossAlertDescriptor.alert_id == alert_id)
            .delete(synchronize_session=False)
        )
        (
            self.db.query(CrossAlertAlertCategoryItem)
            .filter(CrossAlertAlertCategoryItem.alert_id == alert_id)
            .delete(synchronize_session=False)
        )
        self.db.query(Alert).filter(Alert.id == alert_id).delete(synchronize_session=False)
        self.db.commit()

    def _ensure_user_exists(self, user_id: int) -> User:
            user = self.db.query(User).filter(User.id == user_id).first()
            if user is None:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            return user

    def _get_alert_for_user_or_404(self, user_id: int, alert_id: int) -> Alert:
        self._ensure_user_exists(user_id)
        alert = (
            self.db.query(Alert)
            .filter(Alert.id == alert_id, Alert.user_id == user_id)
            .first()
        )
        if alert is None:
            raise HTTPException(status_code=404, detail="Alerta no encontrada para el usuario")
        return alert

    def _replace_descriptors(self, alert_id: int, descriptors: List[str]) -> None:
        (
            self.db.query(CrossAlertDescriptor)
            .filter(CrossAlertDescriptor.alert_id == alert_id)
            .delete(synchronize_session=False)
        )

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

    def _replace_categories(self, alert_id: int, categories: List[dict]) -> None:
        (
            self.db.query(CrossAlertAlertCategoryItem)
            .filter(CrossAlertAlertCategoryItem.alert_id == alert_id)
            .delete(synchronize_session=False)
        )

        for category in categories:
            category_item = (
                self.db.query(AlertCategoryItem)
                .filter(
                    AlertCategoryItem.code == category.code,
                    AlertCategoryItem.label == category.label,
                )
                .first()
            )
            if category_item is None:
                category_item = AlertCategoryItem(code=category.code, label=category.label)
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
                .join(CrossAlertDescriptor, CrossAlertDescriptor.descriptor_id == Descriptor.id)
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

        return AlertResponse(
            id=alert.id,
            user_id=alert.user_id,
            name=alert.name,
            cron_expression=alert.cron_expression,
            descriptors=descriptors,
            categories=categories,
        )
