from typing import List
from sqlalchemy.orm import Session
from .schemas import AlertResponse, AlertCreate, AlertUpdate
from ...core.common_service import CommonService


class AlertsService(CommonService):
    def __init__(self, db: Session):
        super().__init__(db)

    def list_user_alerts(self, user_id: int) -> List[AlertResponse]:
        pass

    def create_user_alert(self, user_id: int, payload: AlertCreate) -> AlertResponse:
        pass

    def get_user_alert(self, user_id: int, alert_id: int) -> AlertResponse:
        pass

    def update_user_alert(
        self,
        user_id: int,
        alert_id: int,
        payload: AlertUpdate,
    ) -> AlertResponse:
        pass

    def delete_user_alert(self, user_id, alert_id) -> None:
        pass
