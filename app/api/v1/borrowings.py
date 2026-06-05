from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="List borrowings")
async def list_borrowings():
    return {"message": "List borrowings endpoint placeholder"}
