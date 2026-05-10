from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from .schemas import RoleResponse, RoleCreate, RoleUpdate
from ...core.common_service import CommonService
from ...db.models import Role, CrossRoleUser

# Service para manejar roles de usuario. Permite listar, crear, obtener, actualizar y eliminar roles.
class RolesService(CommonService):
    def __init__(self, db: Session):
        super().__init__(db)

    def list_roles(self) -> List[RoleResponse]:
        roles = self.db.query(Role).all()
        return [RoleResponse(id=role.id, name=role.name) for role in roles]

    def create_role(
        self,
        payload: RoleCreate,
    ) -> RoleResponse:
        self._ensure_unique_role_name(payload.name)
        role = Role(name=payload.name)
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return RoleResponse(id=role.id, name=role.name)

    def get_role(
        self,
        role_id: int,
    ) -> RoleResponse:
        role = self._get_role_or_404(role_id)
        return RoleResponse(id=role.id, name=role.name)

    def update_role(
        self,
        role_id: int,
        payload: RoleUpdate,
    ) -> RoleResponse:
        role = self._get_role_or_404(role_id)
        data = payload.model_dump(exclude_unset=True)
        if "name" in data:
            self._ensure_unique_role_name(data["name"], exclude_role_id=role_id)
            role.name = data["name"]
        self.db.commit()
        self.db.refresh(role)
        return RoleResponse(id=role.id, name=role.name)

    def delete_role(
        self,
        role_id: int,
    ) -> None:
        role = self._get_role_or_404(role_id)

        assigned = (
            self.db.query(CrossRoleUser)
            .filter(CrossRoleUser.role_id == role_id)
            .first()
        )
        if assigned is not None:
            raise HTTPException(
                status_code=409,
                detail="No se puede eliminar un rol asignado a usuarios",
            )

        self.db.delete(role)
        self.db.commit()

    def _get_role_or_404(self, role_id: int) -> Role:
        role = self.db.query(Role).filter(Role.id == role_id).first()
        if role is None:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        return role

    def _ensure_unique_role_name(self, name: str, exclude_role_id: int | None = None) -> None:
        normalized = name.strip().lower()
        roles = self.db.query(Role).all()
        for role in roles:
            if exclude_role_id is not None and role.id == exclude_role_id:
                continue
            if role.name.strip().lower() == normalized:
                raise HTTPException(status_code=409, detail="Ya existe un rol con ese nombre")
