from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_db
from app.dependencies.permissions import require_roles
from app.schemas.book import BookRead, BookBase
from app.services.book_service import BookService
from app.models.book import Book

router = APIRouter()

book_service = BookService()


@router.get("/", response_model=list[BookRead], summary="List books")
async def list_books(db: AsyncSession = Depends(get_db)):
    return await book_service.list(db)


@router.post("/", response_model=BookRead, summary="Create book")
async def create_book(payload: BookBase, db: AsyncSession = Depends(get_db), current_user=Depends(require_roles("admin", "librarian"))):
    data = payload.dict()
    book = await book_service.create(db, data)
    return book


@router.get("/{book_id}", response_model=BookRead, summary="Get book by id")
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await book_service.get(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=BookRead, summary="Update book")
async def update_book(book_id: int, payload: BookBase, db: AsyncSession = Depends(get_db), current_user=Depends(require_roles("admin", "librarian"))):
    book = await book_service.get(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    updated = await book_service.update(db, book, **payload.dict())
    return updated


@router.delete("/{book_id}", status_code=204, summary="Delete book")
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(require_roles("admin", "librarian"))):
    book = await book_service.get(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    await book_service.delete(db, book)
    return None
