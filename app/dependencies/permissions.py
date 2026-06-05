from typing import Callable

from fastapi import Depends, HTTPException, status

from app.dependencies.auth import get_current_user
from app.models.user import User


def require_roles(*allowed_roles: str) -> Callable:
    async def _require(current_user: User = Depends(get_current_user)) -> User:
        role_name = getattr(current_user.role, "name", None)
        if role_name not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
        return current_user

    return _require
