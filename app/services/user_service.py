from typing import Any

from app.models.user import User


class UserService:
    async def create_user(self, user_data: dict[str, Any]) -> User:
        raise NotImplementedError()

    async def get_user_by_email(self, email: str) -> User | None:
        raise NotImplementedError()
