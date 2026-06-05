from datetime import datetime
from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    description: str | None = None


class CategoryRead(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
