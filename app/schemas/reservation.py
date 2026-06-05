from datetime import datetime
from pydantic import BaseModel


class ReservationBase(BaseModel):
    user_id: int
    book_id: int
    reservation_date: datetime | None = None
    status: str | None = None


class ReservationRead(ReservationBase):
    id: int

    class Config:
        orm_mode = True


class ReservationCreate(BaseModel):
    book_id: int


class ReservationUpdate(BaseModel):
    status: str | None = None
