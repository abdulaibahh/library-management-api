from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.permissions import require_roles
from app.schemas.user import UserRead
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=list[UserRead], summary="List users")
async def list_users(db: AsyncSession = Depends(get_db), current_user: User = Depends(require_roles("admin", "librarian"))):
    stmt = select(User)
    result = await db.execute(stmt)
    users = result.scalars().all()
    return users


@router.get("/me", response_model=UserRead, summary="Get current user")
async def get_me(current_user: User = Depends(get_current_user)) -> UserRead:
    return current_user
