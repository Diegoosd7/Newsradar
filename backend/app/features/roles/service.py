from typing import List
from sqlalchemy.orm import Session
from .schemas import RoleResponse, RoleCreate, RoleUpdate
from ...core.common_service import CommonService


class RolesService(CommonService):
    def __init__(self, db: Session):
        super().__init__(db)

    def list_roles(self) -> List[RoleResponse]:
        pass

    def create_role(
        self,
        payload: RoleCreate,
    ) -> RoleResponse:
        pass

    def get_role(
        self,
        role_id: int,
    ) -> RoleResponse:
        pass

    def update_role(
        self,
        role_id: int,
        payload: RoleUpdate,
    ) -> RoleResponse:
        pass

    def delete_role(
        self,
        role_id: int,
    ) -> None:
        pass
