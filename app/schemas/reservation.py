from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ReservationBase(BaseModel):
    user_id: int
    book_id: int
    reservation_date: datetime | None = None
    status: str | None = None


class ReservationRead(ReservationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ReservationCreate(BaseModel):
    book_id: int


class ReservationUpdate(BaseModel):
    status: str | None = None
