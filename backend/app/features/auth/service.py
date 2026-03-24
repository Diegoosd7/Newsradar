from uuid import uuid4
from fastapi import HTTPException
from sqlalchemy.orm import Session
from .schemas import TokenResponse, LoginRequest
from ...core.common_service import CommonService
from ...core.shared_schemas import UserCreate, UserResponse
from ...db.models import User, Role, CrossRoleUser


active_tokens: dict[str, int] = {}


class AuthService(CommonService):
    def __init__(self, db: Session):
        super().__init__(db)

    def login(self, payload: LoginRequest) -> TokenResponse:
        user = self.db.query(User).filter(User.email == payload.email).first()
        if user is None or user.password != payload.password:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        token = str(uuid4())
        active_tokens[token] = user.id
        return TokenResponse(access_token=token)

    def register(self, payload: UserCreate) -> UserResponse:
        existing = self.db.query(User).filter(User.email == payload.email).first()
        if existing is not None:
            raise HTTPException(status_code=409, detail="El email ya está registrado")

        self._ensure_roles_exist(payload.role_ids)

        user = User(
            email=payload.email,
            password=payload.password,
            first_name=payload.first_name,
            last_name=payload.last_name,
            organization=payload.organization,
        )
        self.db.add(user)
        self.db.flush()

        for role_id in payload.role_ids:
            self.db.add(CrossRoleUser(user_id=user.id, role_id=role_id))

        self.db.commit()
        self.db.refresh(user)

        return UserResponse(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            organization=user.organization,
            role_ids=payload.role_ids,
        )

    def _ensure_roles_exist(self, role_ids: list[int]) -> None:
        if not role_ids:
            return
        found = self.db.query(Role.id).filter(Role.id.in_(role_ids)).all()
        found_ids = {role_id for (role_id,) in found}
        missing = [role_id for role_id in role_ids if role_id not in found_ids]
        if missing:
            raise HTTPException(status_code=400, detail=f"Roles no encontrados: {missing}")
