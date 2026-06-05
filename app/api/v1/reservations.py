from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.permissions import require_roles
from app.schemas.reservation import ReservationRead, ReservationCreate
from app.services.reservation_service import ReservationService
from app.models.user import User

router = APIRouter()

reservation_service = ReservationService()


@router.get("/", response_model=list[ReservationRead], summary="List reservations (admin/librarian)")
async def list_reservations(db: AsyncSession = Depends(get_db), current_user: User = Depends(require_roles("admin", "librarian"))):
    return await reservation_service.list(db)


@router.get("/me", response_model=list[ReservationRead], summary="List my reservations")
async def list_my_reservations(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await reservation_service.list_by_user(db, current_user.id)


@router.post("/", response_model=ReservationRead, status_code=201, summary="Create reservation")
async def create_reservation(payload: ReservationCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        res = await reservation_service.create(db, user_id=current_user.id, book_id=payload.book_id)
        return res
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{reservation_id}/cancel", response_model=ReservationRead, summary="Cancel reservation")
async def cancel_reservation(reservation_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    reservation = await reservation_service.get(db, reservation_id)
    if not reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    if reservation.user_id != current_user.id and current_user.role.name not in ("admin", "librarian"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not permitted to cancel this reservation")
    updated = await reservation_service.cancel(db, reservation)
    return updated


@router.get("/{reservation_id}", response_model=ReservationRead, summary="Get reservation by id")
async def get_reservation(reservation_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    reservation = await reservation_service.get(db, reservation_id)
    if not reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    if reservation.user_id != current_user.id and current_user.role.name not in ("admin", "librarian"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not permitted to view this reservation")
    return reservation
