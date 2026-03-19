from fastapi import HTTPException
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, EmailStr, HttpUrl
from datetime import datetime
from ..core.shared_schemas import *
from ..features.alerts.schemas import *
from ..features.auth.schemas import *
from ..features.categories.schemas import *
from ..features.information_sources.schemas import *
from ..features.notifications.schemas import *
from ..features.roles.schemas import *
from ..features.rss_channels.schemas import *
from ..features.stats.schemas import *
from ..features.users.schemas import *


class CommonDictRepository:
    def __init__(self) -> None:
        self.store: Dict[int, object] = {}
        self.counter = 1

    def next_id(self) -> int:
        value = self.counter
        self.counter += 1
        return value

    def ensure_key_exists(self, key: int, error_message: str) -> None:
        if key not in self.store:
            raise HTTPException(status_code=404, detail=error_message)

    def insert_key(self, key: int, value: object) -> None:
        self.store[key] = value

    def update_key(self, key: int, value: object) -> None:
        self.store[key] = value

    def delete_key(self, key: int) -> None:
        self.store.pop(key, None)

    def delete_multiple_keys(self, keys: List[int]) -> None:
        for key in keys:
            self.delete_key(key)


class RolesDictRepository(CommonDictRepository):
    def __init__(self):
        super().__init__()
        self.store: Dict[int, RoleResponse] = {}


class UsersDictRepository(CommonDictRepository):
    def __init__(self):
        super().__init__()
        self.users_store: Dict[int, UserInDB] = {}
        self.counter = 1

    def ensure_user_exists(self, user_id: int) -> None:
        self.ensure_key_exists(user_id, "Usuario no encontrado")


class AlertsDictRepository(CommonDictRepository):
    def __init__(self):
        super().__init__()
        self.alerts_store: Dict[int, AlertResponse] = {}

    def select_all_alerts_by_user_id(self, user_id: int) -> List[AlertResponse]:
        return [
            alert for alert in self.alerts_store.values() if alert.user_id == user_id
        ]

    def ensure_alert_for_user(self, user_id: int, alert_id: int) -> AlertResponse:
        alert = self.alerts_store.get(alert_id)
        if not alert or alert.user_id != user_id:
            raise HTTPException(
                status_code=404, detail="Alerta no encontrada para el usuario"
            )
        return alert


class CategoriesDictRepository(CommonDictRepository):
    def __init__(self):
        super().__init__()
        self.categories_store: Dict[int, CategoryResponse] = {}


class NotificationsDictRepository(CommonDictRepository):
    def __init__(self):
        super().__init__()
        self.notifications_store: Dict[int, NotificationResponse] = {}

    def select_all_notifications_ids_by_alert_id(self, alert_id: int) -> List[int]:
        notification_ids = [
            n.id for n in self.notifications_store.values() if n.alert_id == alert_id
        ]
        return notification_ids


class InformationSourcesDictRepository(CommonDictRepository):
    def __init__(self):
        super().__init__()
        self.information_sources_store: Dict[int, InformationSourceResponse] = {}


class RSSChannelsDictRepository(CommonDictRepository):
    def __init__(self):
        super().__init__()
        self.rss_channels_store: Dict[int, RSSChannelResponse] = {}


class StatsDictRepository(CommonDictRepository):
    def __init__(self):
        super().__init__()
        self.stats_store: Dict[int, StatsResponse] = {}


class ActiveTokensDictRepository(CommonDictRepository):
    def __init__(self):
        super().__init__()
        self.active_tokens: Dict[str, int] = {}


# class AlertsServiceDict:
#     def __init__(self):
#         self.alert_repository = AlertsDictRepository()
#         self.user_repository = UsersDictRepository()
#         self.notification_repository = NotificationsDictRepository()

#     def list_user_alerts(self, user_id: int) -> List[AlertResponse]:
#         self.user_repository.ensure_user_exists(user_id)
#         all_alerts_from_user = self.alert_repository.select_all_alerts_by_user_id(
#             user_id
#         )
#         return all_alerts_from_user

#     def create_user_alert(self, user_id: int, payload: AlertCreate) -> AlertResponse:
#         self.user_repository.ensure_user_exists(user_id)
#         alert_id = self.alert_repository.next_id()
#         alert = AlertResponse(id=alert_id, user_id=user_id, **payload.model_dump())
#         return alert

#     def get_user_alert(self, user_id: int, alert_id: int) -> AlertResponse:
#         return self.alert_repository.ensure_alert_for_user(user_id, alert_id)

#     def update_user_alert(
#         self,
#         user_id: int,
#         alert_id: int,
#         payload: AlertUpdate,
#     ) -> AlertResponse:
#         alert = self.alert_repository.ensure_alert_for_user(user_id, alert_id)
#         updated = alert.model_copy(update=payload.model_dump(exclude_unset=True))
#         self.alert_repository.update_key(alert_id, updated)
#         return updated

#     def delete_user_alert(self, user_id, alert_id) -> None:
#         self.alert_repository.ensure_alert_for_user(user_id, alert_id)
#         notification_ids = (
#             self.notification_repository.select_all_notifications_ids_by_alert_id(
#                 alert_id
#             )
#         )
#         self.notification_repository.delete_multiple_keys(notification_ids)
#         self.alert_repository.delete_key(alert_id)
