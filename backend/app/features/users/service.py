import re
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from .schemas import UserUpdate
from ...core.shared_schemas import UserCreate, UserResponse
from ...core.common_service import CommonService
from ...db.models import User, Role, CrossRoleUser, Alert, Notification

_HTML_TAG_RE = re.compile(r"<[^>]+>")


class UsersService(CommonService):
    def __init__(self, db: Session):
        super().__init__(db)

    def list_users(self) -> List[UserResponse]:
        users = self.db.query(User).all()
        return [self._to_response(user) for user in users]

    def create_user(
        self,
        payload: UserCreate,
    ) -> UserResponse:
        self._ensure_unique_email(payload.email)
        self._reject_html(payload.first_name, "first_name")
        self._reject_html(payload.last_name, "last_name")
        self._reject_html(payload.organization, "organization")

        role_ids = list(payload.role_ids)
        if len(role_ids) > 1:
            raise HTTPException(status_code=422, detail="Un usuario solo puede tener un rol")

        if not role_ids:
            gestor = self._find_gestor_role()
            if gestor is not None:
                role_ids = [gestor.id]
        else:
            self._ensure_roles_exist(role_ids)

        user = User(
            email=payload.email,
            password=payload.password,
            first_name=payload.first_name,
            last_name=payload.last_name,
            organization=payload.organization,
        )
        self.db.add(user)
        self.db.flush()

        for role_id in role_ids:
            self.db.add(CrossRoleUser(user_id=user.id, role_id=role_id))

        self.db.commit()
        self.db.refresh(user)
        return self._to_response(user)

    def get_user(
        self,
        user_id: int,
    ) -> UserResponse:
        user = self._get_user_or_404(user_id)
        return self._to_response(user)

    def update_user(
        self,
        user_id: int,
        payload: UserUpdate,
    ) -> UserResponse:
        user = self._get_user_or_404(user_id)
        data = payload.model_dump(exclude_unset=True)

        if "email" in data:
            self._ensure_unique_email(data["email"], user_id)

        if "role_ids" in data:
            self._ensure_roles_exist(data["role_ids"])

        for field in ["email", "first_name", "last_name", "organization", "password"]:
            if field in data:
                setattr(user, field, data[field])

        if "role_ids" in data:
            (
                self.db.query(CrossRoleUser)
                .filter(CrossRoleUser.user_id == user_id)
                .delete(synchronize_session=False)
            )
            for role_id in data["role_ids"]:
                self.db.add(CrossRoleUser(user_id=user_id, role_id=role_id))

        self.db.commit()
        self.db.refresh(user)
        return self._to_response(user)

    def delete_user(
        self,
        user_id: int,
    ) -> None:
        user = self._get_user_or_404(user_id)

        alert_ids = [alert_id for (alert_id,) in self.db.query(Alert.id).filter(Alert.user_id == user_id).all()]

        if alert_ids:
            (
                self.db.query(Notification)
                .filter(Notification.alert_id.in_(alert_ids))
                .delete(synchronize_session=False)
            )
            (
                self.db.query(Alert)
                .filter(Alert.id.in_(alert_ids))
                .delete(synchronize_session=False)
            )

        (
            self.db.query(CrossRoleUser)
            .filter(CrossRoleUser.user_id == user_id)
            .delete(synchronize_session=False)
        )
        self.db.delete(user)
        self.db.commit()

    def _get_user_or_404(self, user_id: int) -> User:
        user = self.db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user

    def _ensure_unique_email(self, email: str, exclude_user_id: int | None = None) -> None:
        users = self.db.query(User)
        if exclude_user_id is not None:
            users = users.filter(User.id != exclude_user_id)
        for user in users.all():
            if user.email.lower() == email.lower():
                raise HTTPException(status_code=409, detail="El email ya está registrado")

    def _ensure_roles_exist(self, role_ids: List[int]) -> None:
        if not role_ids:
            return
        found = self.db.query(Role.id).filter(Role.id.in_(role_ids)).all()
        found_ids = {role_id for (role_id,) in found}
        missing = [role_id for role_id in role_ids if role_id not in found_ids]
        if missing:
            raise HTTPException(status_code=400, detail=f"Roles no encontrados: {missing}")

    def _find_gestor_role(self) -> Role | None:
        roles = self.db.query(Role).all()
        for role in roles:
            if role.name.strip().lower() == "gestor":
                return role
        return None

    def _reject_html(self, value: str, field: str) -> None:
        if _HTML_TAG_RE.search(value):
            raise HTTPException(status_code=422, detail=f"El campo {field} contiene HTML no permitido")

    def _to_response(self, user: User) -> UserResponse:
        role_ids = [role_id for (role_id,) in self.db.query(CrossRoleUser.role_id).filter(CrossRoleUser.user_id == user.id).all()]
        return UserResponse(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            organization=user.organization,
            role_ids=role_ids,
        )
