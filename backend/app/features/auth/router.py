from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .schemas import TokenResponse, LoginRequest, VerifyEmailResponse
from .service import AuthService
from ...db.database import get_db
from ...core.shared_schemas import UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_service(db: Session = Depends(get_db)):
    return AuthService(db)


@router.post("/login", response_model=TokenResponse, tags=["auth"])
def login(
    payload: LoginRequest, service: AuthService = Depends(get_auth_service)
) -> TokenResponse:
    return service.login(payload)


@router.post("/register", response_model=UserResponse, tags=["auth"])
def register(
    payload: UserCreate, service: AuthService = Depends(get_auth_service)
) -> UserResponse:
    return service.register(payload)


@router.get("/verify-email", response_model=VerifyEmailResponse, tags=["auth"])
def verify_email(
    token: str,
    service: AuthService = Depends(get_auth_service),
) -> VerifyEmailResponse:
    return service.verify_email(token)
