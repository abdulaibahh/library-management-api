from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.book import Book
from app.models.category import Category
from app.models.borrowing import Borrowing, BorrowingStatus
from app.models.reservation import Reservation, ReservationStatus
from app.utils.time import utc_now


class DashboardService:
    async def summary(self, db: AsyncSession) -> dict:
        total_users = (await db.execute(select(func.count()).select_from(User))).scalar_one()
        total_books = (await db.execute(select(func.count()).select_from(Book))).scalar_one()
        total_categories = (await db.execute(select(func.count()).select_from(Category))).scalar_one()

        total_borrowed = (await db.execute(
            select(func.count()).select_from(Borrowing).where(Borrowing.status == BorrowingStatus.borrowed)
        )).scalar_one()

        total_overdue = (await db.execute(
            select(func.count()).select_from(Borrowing).where(
                Borrowing.status == BorrowingStatus.borrowed,
                Borrowing.due_date < utc_now(),
            )
        )).scalar_one()

        total_active_reservations = (await db.execute(
            select(func.count()).select_from(Reservation).where(Reservation.status == ReservationStatus.active)
        )).scalar_one()

        available_books = (await db.execute(select(func.coalesce(func.sum(Book.available_quantity), 0)))).scalar_one()

        return {
            "total_users": int(total_users),
            "total_books": int(total_books),
            "total_categories": int(total_categories),
            "total_borrowed": int(total_borrowed),
            "total_overdue": int(total_overdue),
            "total_active_reservations": int(total_active_reservations),
            "available_books": int(available_books or 0),
        }
