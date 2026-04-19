from typing import List
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from .schemas import NotificationResponse, NotificationCreate, NotificationUpdate
from .service import NotificationsService
from ...db.database import get_db
from ...core.security import get_current_user
from ...core.shared_schemas import UserInDB

router = APIRouter(prefix="/users", tags=["notifications"])


def get_notifications_service(db: Session = Depends(get_db)):
    return NotificationsService(db)


@router.get(
    "/{user_id}/notifications",
    response_model=List[NotificationResponse],
    tags=["notifications"],
)
def list_user_notifications(
    user_id: int,
    _: UserInDB = Depends(get_current_user),
    service: NotificationsService = Depends(get_notifications_service),
) -> List[NotificationResponse]:
    return service.list_user_notifications(user_id)


@router.patch(
    "/{user_id}/notifications/{notification_id}/read",
    response_model=NotificationResponse,
    tags=["notifications"],
)
def mark_notification_as_read(
    user_id: int,
    notification_id: int,
    _: UserInDB = Depends(get_current_user),
    service: NotificationsService = Depends(get_notifications_service),
) -> NotificationResponse:
    return service.mark_notification_as_read(user_id, notification_id)


@router.get(
    "/{user_id}/alerts/{alert_id}/notifications",
    response_model=List[NotificationResponse],
    tags=["notifications"],
)
def list_alert_notifications(
    user_id: int,
    alert_id: int,
    _: UserInDB = Depends(get_current_user),
    service: NotificationsService = Depends(get_notifications_service),
) -> List[NotificationResponse]:
    return service.list_alert_notifications(user_id, alert_id)


@router.post(
    "/{user_id}/alerts/{alert_id}/notifications",
    response_model=NotificationResponse,
    status_code=201,
    tags=["notifications"],
)
def create_alert_notification(
    user_id: int,
    alert_id: int,
    payload: NotificationCreate,
    _: UserInDB = Depends(get_current_user),
    service: NotificationsService = Depends(get_notifications_service),
) -> NotificationResponse:
    return service.create_alert_notification(user_id, alert_id, payload)


@router.get(
    "/{user_id}/alerts/{alert_id}/notifications/{notification_id}",
    response_model=NotificationResponse,
    tags=["notifications"],
)
def get_alert_notification(
    user_id: int,
    alert_id: int,
    notification_id: int,
    _: UserInDB = Depends(get_current_user),
    service: NotificationsService = Depends(get_notifications_service),
) -> NotificationResponse:
    return service.get_alert_notification(user_id, alert_id, notification_id)


@router.put(
    "/{user_id}/alerts/{alert_id}/notifications/{notification_id}",
    response_model=NotificationResponse,
    tags=["notifications"],
)
def update_alert_notification(
    user_id: int,
    alert_id: int,
    notification_id: int,
    payload: NotificationUpdate,
    _: UserInDB = Depends(get_current_user),
    service: NotificationsService = Depends(get_notifications_service),
) -> NotificationResponse:
    return service.update_alert_notification(
        user_id, alert_id, notification_id, payload
    )


@router.delete(
    "/{user_id}/alerts/{alert_id}/notifications/{notification_id}",
    status_code=204,
    response_model=None,
    response_class=Response,
    tags=["notifications"],
)
def delete_alert_notification(
    user_id: int,
    alert_id: int,
    notification_id: int,
    _: UserInDB = Depends(get_current_user),
    service: NotificationsService = Depends(get_notifications_service),
) -> None:
    return service.delete_alert_notification(user_id, alert_id, notification_id)
