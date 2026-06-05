from __future__ import annotations

from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.reservation import Reservation, ReservationStatus
from app.models.book import Book


class ReservationService:
    async def create(self, db: AsyncSession, user_id: int, book_id: int) -> Reservation:
        # check book exists
        stmt = select(Book).where(Book.id == book_id)
        result = await db.execute(stmt)
        book = result.scalar_one_or_none()
        if not book:
            raise ValueError("Book not found")

        reservation = Reservation(user_id=user_id, book_id=book_id, reservation_date=datetime.utcnow(), status=ReservationStatus.active)
        db.add(reservation)
        await db.commit()
        await db.refresh(reservation)
        return reservation

    async def list(self, db: AsyncSession) -> list[Reservation]:
        stmt = select(Reservation)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def list_by_user(self, db: AsyncSession, user_id: int) -> list[Reservation]:
        stmt = select(Reservation).where(Reservation.user_id == user_id)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get(self, db: AsyncSession, reservation_id: int) -> Reservation | None:
        stmt = select(Reservation).where(Reservation.id == reservation_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def cancel(self, db: AsyncSession, reservation: Reservation) -> Reservation:
        reservation.status = ReservationStatus.cancelled
        db.add(reservation)
        await db.commit()
        await db.refresh(reservation)
        return reservation
