from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.permissions import require_roles
from app.schemas.user import UserRead
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.user_service import UserService
from app.services.auth_service import AuthService

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


@router.get("/{user_id}", response_model=UserRead, summary="Get user by id")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_roles("admin", "librarian"))):
    user = await UserService().get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserRead, summary="Update user")
async def update_user(user_id: int, payload: UserCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_roles("admin", "librarian"))):
    service = UserService()
    user = await service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    data = payload.model_dump()
    if "password" in data:
        data["password_hash"] = await AuthService.hash_password(data.pop("password"))
    updated = await service.update_user(db, user, **data)
    return updated


@router.delete("/{user_id}", status_code=204, summary="Delete user")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_roles("admin"))):
    service = UserService()
    user = await service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    await service.delete_user(db, user)
    return None
