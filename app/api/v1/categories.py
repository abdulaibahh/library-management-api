from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="List categories")
async def list_categories():
    return {"message": "List categories endpoint placeholder"}
