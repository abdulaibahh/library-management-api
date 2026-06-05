from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="List reservations")
async def list_reservations():
    return {"message": "List reservations endpoint placeholder"}
