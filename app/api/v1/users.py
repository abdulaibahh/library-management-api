from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="List users")
async def list_users():
    return {"message": "List users endpoint placeholder"}
