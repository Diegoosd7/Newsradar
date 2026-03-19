from typing import List
from sqlalchemy.orm import Session
from .schemas import NotificationResponse, NotificationCreate, NotificationUpdate
from ...core.common_service import CommonService


class NotificationsService(CommonService):
    def __init__(self, db: Session):
        super().__init__(db)

    def list_alert_notifications(
        self,
        user_id: int,
        alert_id: int,
    ) -> List[NotificationResponse]:
        pass

    def create_alert_notification(
        self,
        user_id: int,
        alert_id: int,
        payload: NotificationCreate,
    ) -> NotificationResponse:
        pass

    def get_alert_notification(
        self,
        user_id: int,
        alert_id: int,
        notification_id: int,
    ) -> NotificationResponse:
        pass

    def update_alert_notification(
        self,
        user_id: int,
        alert_id: int,
        notification_id: int,
        payload: NotificationUpdate,
    ) -> NotificationResponse:
        pass

    def delete_alert_notification(
        self,
        user_id: int,
        alert_id: int,
        notification_id: int,
    ) -> None:
        pass
