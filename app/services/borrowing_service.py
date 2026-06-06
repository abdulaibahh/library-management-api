from __future__ import annotations

from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.models.borrowing import Borrowing, BorrowingStatus
from app.models.book import Book
from app.utils.time import utc_now


class BorrowingService:
    async def create(self, db: AsyncSession, user_id: int, book_id: int, due_date: datetime) -> Borrowing:
        # Fetch book
        stmt = select(Book).where(Book.id == book_id)
        result = await db.execute(stmt)
        book = result.scalar_one_or_none()
        if not book:
            raise ValueError("Book not found")
        if book.available_quantity <= 0:
            raise ValueError("Book not available")

        # decrement available
        book.available_quantity = max(0, book.available_quantity - 1)
        db.add(book)

        borrowing = Borrowing(user_id=user_id, book_id=book_id, due_date=due_date, status=BorrowingStatus.borrowed)
        db.add(borrowing)
        await db.commit()
        await db.refresh(borrowing)
        return borrowing

    async def list(self, db: AsyncSession) -> list[Borrowing]:
        stmt = select(Borrowing)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def list_by_user(self, db: AsyncSession, user_id: int) -> list[Borrowing]:
        stmt = select(Borrowing).where(Borrowing.user_id == user_id)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get(self, db: AsyncSession, borrowing_id: int) -> Borrowing | None:
        stmt = select(Borrowing).where(Borrowing.id == borrowing_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def return_book(self, db: AsyncSession, borrowing: Borrowing, return_date: datetime | None = None) -> Borrowing:
        if borrowing.return_date:
            return borrowing
        borrowing.return_date = return_date or utc_now()
        borrowing.status = BorrowingStatus.returned

        # increase book available quantity
        stmt = select(Book).where(Book.id == borrowing.book_id)
        result = await db.execute(stmt)
        book = result.scalar_one_or_none()
        if book:
            book.available_quantity = book.available_quantity + 1
            db.add(book)

        db.add(borrowing)
        await db.commit()
        await db.refresh(borrowing)
        return borrowing
