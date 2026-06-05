from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None = None
    is_active: bool = True


class UserCreate(UserBase):
    password: str
    role_id: int


class UserRead(UserBase):
    id: int
    role_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
