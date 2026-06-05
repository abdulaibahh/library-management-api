from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_db
from app.dependencies.permissions import require_roles
from app.services.dashboard_service import DashboardService

router = APIRouter()

dashboard_service = DashboardService()


@router.get("/summary", summary="Get dashboard summary")
async def get_dashboard_summary(db: AsyncSession = Depends(get_db), _=Depends(require_roles("admin", "librarian"))):
    return await dashboard_service.summary(db)
