from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from .schemas import RoleResponse, RoleCreate, RoleUpdate
from ...core.common_service import CommonService
from ...db.models import Role, CrossRoleUser


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
