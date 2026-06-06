from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.utils.time import utc_now


class BorrowingStatus(str, PyEnum):
    pending = "pending"
    borrowed = "borrowed"
    returned = "returned"
    overdue = "overdue"


class Borrowing(Base):
    __tablename__ = "borrowings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)
    borrow_date: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    return_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    status: Mapped[BorrowingStatus] = mapped_column(
        SAEnum(BorrowingStatus, native_enum=False),
        default=BorrowingStatus.borrowed,
        nullable=False,
    )

    user: Mapped["User"] = relationship("User", back_populates="borrowings")
    book: Mapped["Book"] = relationship("Book", back_populates="borrowings")
