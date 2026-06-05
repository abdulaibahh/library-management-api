from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_db
from app.dependencies.permissions import require_roles
from app.schemas.category import CategoryRead
from app.models.category import Category

router = APIRouter()


@router.get("/", response_model=list[CategoryRead], summary="List categories")
async def list_categories(db: AsyncSession = Depends(get_db)):
    stmt = select(Category)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("/", response_model=CategoryRead, summary="Create category")
async def create_category(payload: CategoryRead, db: AsyncSession = Depends(get_db), current_user=Depends(require_roles("admin", "librarian"))):
    category = Category(name=payload.name, description=payload.description)
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category
