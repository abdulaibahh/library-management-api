from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.book import Book


class BookService:
    async def create(self, db: AsyncSession, data: dict) -> Book:
        book = Book(**data)
        db.add(book)
        await db.commit()
        await db.refresh(book)
        return book

    async def list(self, db: AsyncSession) -> list[Book]:
        stmt = select(Book)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get(self, db: AsyncSession, book_id: int) -> Book | None:
        stmt = select(Book).where(Book.id == book_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, db: AsyncSession, book: Book, **data) -> Book:
        for k, v in data.items():
            setattr(book, k, v)
        db.add(book)
        await db.commit()
        await db.refresh(book)
        return book

    async def delete(self, db: AsyncSession, book: Book) -> None:
        await db.delete(book)
        await db.commit()
class BookService:
    async def list_books(self) -> list[dict]:
        raise NotImplementedError()
