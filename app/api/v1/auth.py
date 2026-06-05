from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.dependencies.database import get_db
from app.schemas.auth import UserRegister, UserLogin, TokenResponse
from app.schemas.user import UserRead
from app.models.user import User
from app.models.role import Role
from app.core.roles import UserRole
from app.services.user_service import UserService
from app.services.auth_service import AuthService

router = APIRouter()

user_service = UserService()
auth_service = AuthService()


@router.post("/register", response_model=UserRead, status_code=201, summary="Register a new user")
async def register(payload: UserRegister, db: AsyncSession = Depends(get_db)) -> UserRead:
    existing = await user_service.get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # try to find student role; fallback to first role id
    role_stmt = select(Role).where(Role.name == UserRole.student.value)
    role_result = await db.execute(role_stmt)
    role = role_result.scalar_one_or_none()
    role_id = role.id if role else 1

    hashed = await auth_service.hash_password(payload.password)
    user_dict = {
        "first_name": payload.first_name,
        "last_name": payload.last_name,
        "email": payload.email,
        "phone": payload.phone,
        "password_hash": hashed,
        "role_id": role_id,
    }

    user = await user_service.create_user(db, user_dict)
    return user


@router.post("/login", response_model=TokenResponse, summary="Authenticate a user")
async def login(payload: UserLogin, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    user = await user_service.get_user_by_email(db, payload.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not await auth_service.verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = await auth_service.create_token(user)
    return TokenResponse(access_token=access_token)
