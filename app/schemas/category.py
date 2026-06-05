from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    name: str
    description: str | None = None


class CategoryRead(CategoryBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
