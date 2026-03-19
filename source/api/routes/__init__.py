from fastapi import APIRouter

from routes.health import router as health_router
from routes.user import router as user_router
from routes.report import router as report_router
from routes.occurrence import router as occurrence_router

router = APIRouter()

router.include_router(health_router)
router.include_router(user_router)
router.include_router(report_router)
router.include_router(occurrence_router)

__all__ = ["router"]
