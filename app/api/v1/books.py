from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="List books")
async def list_books():
    return {"message": "List books endpoint placeholder"}
