from sqlalchemy.orm import Session
from .schemas import TokenResponse, LoginRequest
from ...core.common_service import CommonService
from ...core.shared_schemas import UserCreate, UserResponse


class AuthService(CommonService):
    def __init__(self, db: Session):
        super().__init__(db)

    def login(self, payload: LoginRequest) -> TokenResponse:
        pass

    def register(self, payload: UserCreate) -> UserResponse:
        pass
