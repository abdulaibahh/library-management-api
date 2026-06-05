from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.permissions import require_roles
from app.schemas.borrowing import BorrowingRead, BorrowingCreate, BorrowingUpdate
from app.services.borrowing_service import BorrowingService
from app.services.user_service import UserService
from app.models.user import User

router = APIRouter()

borrowing_service = BorrowingService()


@router.get("/", response_model=list[BorrowingRead], summary="List borrowings (admin/librarian)")
async def list_borrowings(db: AsyncSession = Depends(get_db), current_user: User = Depends(require_roles("admin", "librarian"))):
    return await borrowing_service.list(db)


@router.get("/me", response_model=list[BorrowingRead], summary="List my borrowings")
async def list_my_borrowings(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await borrowing_service.list_by_user(db, current_user.id)


@router.post("/", response_model=BorrowingRead, status_code=201, summary="Borrow a book")
async def borrow_book(payload: BorrowingCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        borrowing = await borrowing_service.create(db, user_id=current_user.id, book_id=payload.book_id, due_date=payload.due_date)
        return borrowing
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{borrowing_id}/return", response_model=BorrowingRead, summary="Return a borrowed book")
async def return_book(borrowing_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    borrowing = await borrowing_service.get(db, borrowing_id)
    if not borrowing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Borrowing not found")
    if borrowing.user_id != current_user.id and current_user.role.name != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not permitted to return this borrowing")

    returned = await borrowing_service.return_book(db, borrowing, return_date=datetime.utcnow())
    return returned


@router.get("/{borrowing_id}", response_model=BorrowingRead, summary="Get borrowing by id")
async def get_borrowing(borrowing_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    borrowing = await borrowing_service.get(db, borrowing_id)
    if not borrowing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Borrowing not found")
    # allow owner or admin/librarian
    if borrowing.user_id != current_user.id and current_user.role.name not in ("admin", "librarian"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not permitted to view this borrowing")
    return borrowing
