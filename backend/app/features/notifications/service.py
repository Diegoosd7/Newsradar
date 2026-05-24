import zoneinfo

from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from .schemas import NotificationResponse, NotificationCreate, NotificationUpdate
from ...core.common_service import CommonService
from ...core.email_service import EmailService
from ...db.models import (
    Alert,
    Notification,
    Metric,
    CrossMetricNotification,
    NewsItem,
    RSSChannel,
    InformationSource,
    User,
)


class NotificationsService(CommonService):
    def __init__(self, db: Session):
        super().__init__(db)
        self.email_service = EmailService()

    def list_user_notifications(self, user_id: int) -> List[NotificationResponse]:
        notifications = (
            self.db.query(Notification)
            .join(Alert, Alert.id == Notification.alert_id)
            .filter(Alert.user_id == user_id)
            .order_by(Notification.timestamp.desc())
            .all()
        )
        return [self._to_response(notification) for notification in notifications]

    def list_alert_notifications(
        self,
        user_id: int,
        alert_id: int,
    ) -> List[NotificationResponse]:
        self._get_alert_for_user_or_404(user_id, alert_id)
        notifications = (
            self.db.query(Notification)
            .filter(Notification.alert_id == alert_id)
            .order_by(Notification.timestamp.desc())
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

    def create_and_dispatch_notification(
        self,
        alert: Alert,
        user: User,
        news_item: NewsItem,
        matched_descriptor: str | None,
        timestamp,
    ) -> bool:
        existing = (
            self.db.query(Notification)
            .filter(
                Notification.alert_id == alert.id,
                Notification.news_item_id == news_item.id,
            )
            .first()
        )
        if existing is not None:
            return False

        notification = Notification(
            alert_id=alert.id,
            news_item_id=news_item.id,
            timestamp=timestamp,
            matched_descriptor=matched_descriptor,
            is_read=False,
        )
        self.db.add(notification)
        self.db.flush()

        self.db.commit()
        self.db.refresh(notification)

        published_or_timestamp = notification.timestamp
        source_name = self._get_source_name(news_item)
        zona = zoneinfo.ZoneInfo("Europe/Madrid")
        published_local = published_or_timestamp.astimezone(zona)
        news_datetime_text = published_local.strftime("%d/%m/%Y %H:%M")

        try:
            self.email_service.send_alert_notification_email(
                recipient_email=user.email,
                alert_name=alert.name,
                source_name=source_name,
                news_datetime_text=news_datetime_text,
                title=news_item.title,
                summary=news_item.summary,
            )
        except Exception as exc:
            print(
                f"Warning: no se pudo enviar el email de la notificación "
                f"{notification.id} para la alerta {alert.id}: {exc}"
            )

        return True

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

    def mark_notification_as_read(
        self,
        user_id: int,
        notification_id: int,
    ) -> NotificationResponse:
        self._ensure_user_exists(user_id)
        notification = self._get_user_notification_or_404(user_id, notification_id)
        notification.is_read = True
        self.db.commit()
        self.db.refresh(notification)
        return self._to_response(notification)

    def _ensure_user_exists(self, user_id: int) -> User:
        user = self.db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user

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

    def _get_user_notification_or_404(self, user_id: int, notification_id: int) -> Notification:
        notification = (
            self.db.query(Notification)
            .join(Alert, Alert.id == Notification.alert_id)
            .filter(Notification.id == notification_id, Alert.user_id == user_id)
            .first()
        )
        if notification is None:
            raise HTTPException(status_code=404, detail="Notificación no encontrada para el usuario")
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

    def _get_source_name(self, news_item: NewsItem) -> str:
        if news_item.channel_id is None:
            return "Origen desconocido"

        source_name = (
            self.db.query(InformationSource.name)
            .join(RSSChannel, RSSChannel.information_source_id == InformationSource.id)
            .filter(RSSChannel.id == news_item.channel_id)
            .scalar()
        )
        return source_name or "Origen desconocido"

    def _to_response(self, notification: Notification) -> NotificationResponse:
        news_item = None
        source_name = None
        if notification.news_item_id is not None:
            news_item = self.db.query(NewsItem).filter(NewsItem.id == notification.news_item_id).first()
            if news_item is not None:
                source_name = self._get_source_name(news_item)

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
            news_item_id=notification.news_item_id,
            matched_descriptor=notification.matched_descriptor,
            is_read=notification.is_read,
            news_title=news_item.title if news_item is not None else None,
            news_summary=news_item.summary if news_item is not None else None,
            news_url=news_item.url if news_item is not None else None,
            news_published=news_item.published if news_item is not None else None,
            source_name=source_name,
        )