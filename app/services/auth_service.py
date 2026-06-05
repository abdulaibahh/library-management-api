from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User


class AuthService:
    @staticmethod
    async def verify_password(plain_password: str, hashed_password: str) -> bool:
        return verify_password(plain_password, hashed_password)

    @staticmethod
    async def hash_password(password: str) -> str:
        return hash_password(password)

    @staticmethod
    async def create_token(user: User) -> str:
        return create_access_token({"sub": user.email, "user_id": str(user.id)})
