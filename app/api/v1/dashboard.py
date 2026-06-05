from fastapi import APIRouter

router = APIRouter()


@router.get("/summary", summary="Get dashboard summary")
async def get_dashboard_summary():
    return {"message": "Dashboard summary endpoint placeholder"}
