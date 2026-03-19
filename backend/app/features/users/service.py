from typing import List
from sqlalchemy.orm import Session
from .schemas import UserUpdate
from ...core.shared_schemas import UserCreate, UserResponse
from ...core.common_service import CommonService


class UsersService(CommonService):
    def __init__(self, db: Session):
        super().__init__(db)

    def list_users(self) -> List[UserResponse]:
        pass

    def create_user(
        self,
        payload: UserCreate,
    ) -> UserResponse:
        pass

    def get_user(
        self,
        user_id: int,
    ) -> UserResponse:
        pass

    def update_user(
        self,
        user_id: int,
        payload: UserUpdate,
    ) -> UserResponse:
        pass

    def delete_user(
        self,
        user_id: int,
    ) -> None:
        pass
