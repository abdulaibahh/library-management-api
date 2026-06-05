from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class ReservationStatus(str, PyEnum):
    active = "active"
    cancelled = "cancelled"
    fulfilled = "fulfilled"


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)
    reservation_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    status: Mapped[ReservationStatus] = mapped_column(
        SAEnum(ReservationStatus, native_enum=False),
        default=ReservationStatus.active,
        nullable=False,
    )

    user: Mapped["User"] = relationship("User", back_populates="reservations")
    book: Mapped["Book"] = relationship("Book", back_populates="reservations")
