from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from .schemas import NotificationResponse, NotificationCreate, NotificationUpdate
from ...core.common_service import CommonService
from ...db.models import (
    Alert,
    Notification,
    Metric,
    CrossMetricNotification,
)


class NotificationsService(CommonService):
    def __init__(self, db: Session):
        super().__init__(db)

    def list_alert_notifications(
        self,
        user_id: int,
        alert_id: int,
    ) -> List[NotificationResponse]:
        self._get_alert_for_user_or_404(user_id, alert_id)
        notifications = (
            self.db.query(Notification)
            .filter(Notification.alert_id == alert_id)
            .all()
        )
        return [self._to_response(notification) for notification in notifications]

    def create_alert_notification(
        self,
        user_id: int,
        alert_id: int,
        payload: NotificationCreate,
    ) -> NotificationResponse:
        self._get_alert_for_user_or_404(user_id, alert_id)

        notification = Notification(
            alert_id=alert_id,
            timestamp=payload.timestamp,
        )
        self.db.add(notification)
        self.db.flush()

        self._replace_metrics(notification.id, payload.metrics)

        self.db.commit()
        self.db.refresh(notification)
        return self._to_response(notification)

    def get_alert_notification(
        self,
        user_id: int,
        alert_id: int,
        notification_id: int,
    ) -> NotificationResponse:
        self._get_alert_for_user_or_404(user_id, alert_id)
        notification = self._get_notification_for_alert_or_404(alert_id, notification_id)
        return self._to_response(notification)

    def update_alert_notification(
        self,
        user_id: int,
        alert_id: int,
        notification_id: int,
        payload: NotificationUpdate,
    ) -> NotificationResponse:
        self._get_alert_for_user_or_404(user_id, alert_id)
        notification = self._get_notification_for_alert_or_404(alert_id, notification_id)
        data = payload.model_dump(exclude_unset=True)

        if "timestamp" in data:
            notification.timestamp = data["timestamp"]
        if "metrics" in data:
            self._replace_metrics(notification_id, data["metrics"])

        self.db.commit()
        self.db.refresh(notification)
        return self._to_response(notification)

    def delete_alert_notification(
        self,
        user_id: int,
        alert_id: int,
        notification_id: int,
    ) -> None:
        self._get_alert_for_user_or_404(user_id, alert_id)
        notification = self._get_notification_for_alert_or_404(alert_id, notification_id)

        (
            self.db.query(CrossMetricNotification)
            .filter(CrossMetricNotification.notification_id == notification_id)
            .delete(synchronize_session=False)
        )
        self.db.delete(notification)
        self.db.commit()

    def _get_alert_for_user_or_404(self, user_id: int, alert_id: int) -> Alert:
        alert = (
            self.db.query(Alert)
            .filter(Alert.id == alert_id, Alert.user_id == user_id)
            .first()
        )
        if alert is None:
            raise HTTPException(status_code=404, detail="Alerta no encontrada para el usuario")
        return alert

    def _get_notification_for_alert_or_404(self, alert_id: int, notification_id: int) -> Notification:
        notification = (
            self.db.query(Notification)
            .filter(Notification.id == notification_id, Notification.alert_id == alert_id)
            .first()
        )
        if notification is None:
            raise HTTPException(status_code=404, detail="Notificación no encontrada para la alerta")
        return notification

    def _replace_metrics(self, notification_id: int, metrics: List[dict]) -> None:
        (
            self.db.query(CrossMetricNotification)
            .filter(CrossMetricNotification.notification_id == notification_id)
            .delete(synchronize_session=False)
        )

        for metric_item in metrics:
            metric = Metric(name=metric_item.name, value=metric_item.value)
            self.db.add(metric)
            self.db.flush()
            self.db.add(
                CrossMetricNotification(
                    metric_id=metric.id,
                    notification_id=notification_id,
                )
            )

    def _to_response(self, notification: Notification) -> NotificationResponse:
        metrics = [
            {"name": name, "value": value}
            for name, value in (
                self.db.query(Metric.name, Metric.value)
                .join(
                    CrossMetricNotification,
                    CrossMetricNotification.metric_id == Metric.id,
                )
                .filter(CrossMetricNotification.notification_id == notification.id)
                .all()
            )
        ]
        return NotificationResponse(
            id=notification.id,
            alert_id=notification.alert_id,
            timestamp=notification.timestamp,
            metrics=metrics,
        )
