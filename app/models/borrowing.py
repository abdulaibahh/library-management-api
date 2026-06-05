from datetime import datetime
from sqlalchemy import DateTime, Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class BorrowingStatus(str, Enum):
    pending = "pending"
    borrowed = "borrowed"
    returned = "returned"
    overdue = "overdue"


class Borrowing(Base):
    __tablename__ = "borrowings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)
    borrow_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    return_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(Enum(BorrowingStatus), default=BorrowingStatus.borrowed, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="borrowings")
    book: Mapped["Book"] = relationship("Book", back_populates="borrowings")
