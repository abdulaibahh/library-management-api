from datetime import datetime
from pydantic import BaseModel


class BorrowingBase(BaseModel):
    user_id: int
    book_id: int
    borrow_date: datetime | None = None
    due_date: datetime
    return_date: datetime | None = None
    status: str | None = None


class BorrowingRead(BorrowingBase):
    id: int

    class Config:
        orm_mode = True


class BorrowingCreate(BaseModel):
    book_id: int
    due_date: datetime


class BorrowingUpdate(BaseModel):
    return_date: datetime | None = None
    status: str | None = None
