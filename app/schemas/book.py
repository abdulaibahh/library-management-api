from datetime import datetime
from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    publisher: str | None = None
    publication_year: int | None = None
    description: str | None = None
    quantity: int
    available_quantity: int
    category_id: int


class BookRead(BookBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
