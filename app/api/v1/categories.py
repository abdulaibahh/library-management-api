from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_db
from app.dependencies.permissions import require_roles
from app.schemas.category import CategoryRead, CategoryBase
from app.services.category_service import CategoryService

router = APIRouter()

category_service = CategoryService()


@router.get("/", response_model=list[CategoryRead], summary="List categories")
async def list_categories(db: AsyncSession = Depends(get_db)):
    return await category_service.list(db)


@router.post("/", response_model=CategoryRead, summary="Create category")
async def create_category(payload: CategoryBase, db: AsyncSession = Depends(get_db), current_user=Depends(require_roles("admin", "librarian"))):
    return await category_service.create(db, payload.name, payload.description)


@router.get("/{category_id}", response_model=CategoryRead, summary="Get category")
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    category = await category_service.get(db, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


@router.put("/{category_id}", response_model=CategoryRead, summary="Update category")
async def update_category(category_id: int, payload: CategoryBase, db: AsyncSession = Depends(get_db), current_user=Depends(require_roles("admin", "librarian"))):
    category = await category_service.get(db, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return await category_service.update(db, category, name=payload.name, description=payload.description)


@router.delete("/{category_id}", status_code=204, summary="Delete category")
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(require_roles("admin", "librarian"))):
    category = await category_service.get(db, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    await category_service.delete(db, category)
    return None
