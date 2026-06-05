from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category


class CategoryService:
    async def create(self, db: AsyncSession, name: str, description: str | None = None) -> Category:
        category = Category(name=name, description=description)
        db.add(category)
        await db.commit()
        await db.refresh(category)
        return category

    async def list(self, db: AsyncSession) -> list[Category]:
        stmt = select(Category)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get(self, db: AsyncSession, category_id: int) -> Category | None:
        stmt = select(Category).where(Category.id == category_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, db: AsyncSession, category: Category, **data) -> Category:
        for k, v in data.items():
            setattr(category, k, v)
        db.add(category)
        await db.commit()
        await db.refresh(category)
        return category

    async def delete(self, db: AsyncSession, category: Category) -> None:
        await db.delete(category)
        await db.commit()
