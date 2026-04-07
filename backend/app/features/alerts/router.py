from typing import List
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from .schemas import AlertResponse, AlertCreate, AlertUpdate, KeywordSuggestionRequest, KeywordSuggestionResponse
from .service import AlertsService
from ...db.database import get_db
from ...core.security import get_current_user
from ...core.shared_schemas import UserInDB

router = APIRouter(prefix="/users", tags=["alerts"])


def get_alerts_service(db: Session = Depends(get_db)):
    return AlertsService(db)


@router.get(
    "/{user_id}/alerts",
    response_model=List[AlertResponse],
    tags=["alerts"],
)
def list_user_alerts(
    user_id: int,
    _: UserInDB = Depends(get_current_user),
    service: AlertsService = Depends(get_alerts_service),
) -> List[AlertResponse]:
    return service.list_user_alerts(user_id)


@router.post(
    "/{user_id}/alerts",
    response_model=AlertResponse,
    status_code=201,
    tags=["alerts"],
)
def create_user_alert(
    user_id: int,
    payload: AlertCreate,
    _: UserInDB = Depends(get_current_user),
    service: AlertsService = Depends(get_alerts_service),
) -> AlertResponse:
    return service.create_user_alert(user_id, payload)


@router.get(
    "/{user_id}/alerts/{alert_id}",
    response_model=AlertResponse,
    tags=["alerts"],
)
def get_user_alert(
    user_id: int,
    alert_id: int,
    _: UserInDB = Depends(get_current_user),
    service: AlertsService = Depends(get_alerts_service),
) -> AlertResponse:
    return service.get_user_alert(user_id, alert_id)


@router.put(
    "/{user_id}/alerts/{alert_id}",
    response_model=AlertResponse,
    tags=["alerts"],
)
def update_user_alert(
    user_id: int,
    alert_id: int,
    payload: AlertUpdate,
    _: UserInDB = Depends(get_current_user),
    service: AlertsService = Depends(get_alerts_service),
) -> AlertResponse:
    return service.update_user_alert(user_id, alert_id, payload)


@router.delete(
    "/{user_id}/alerts/{alert_id}",
    status_code=204,
    response_model=None,
    response_class=Response,
    tags=["alerts"],
)
def delete_user_alert(
    user_id: int,
    alert_id: int,
    _: UserInDB = Depends(get_current_user),
    service: AlertsService = Depends(get_alerts_service),
) -> None:
    service.delete_user_alert(user_id, alert_id)

@router.post(
    "/suggest-keywords",
    response_model=KeywordSuggestionResponse,
    tags=["alerts", "ai"],
    summary="Sugiere entre 3 y 10 palabras relacionadas usando IA"
)
def suggest_alert_keywords(
    payload: KeywordSuggestionRequest,
    _: UserInDB = Depends(get_current_user),
    service: AlertsService = Depends(get_alerts_service),
) -> KeywordSuggestionResponse:
    suggestions = service.suggest_keywords_with_ai(payload.keyword)
    return KeywordSuggestionResponse(suggestions=suggestions)
