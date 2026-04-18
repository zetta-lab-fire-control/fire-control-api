from fastapi import APIRouter

from routes.health import router as health_router
from routes.auth import router as auth_router
from routes.user import router as user_router
from routes.firefighter import router as firefighter_router
from routes.report import router as report_router
from routes.occurrence import router as occurrence_router
from routes.media import router as media_router


router = APIRouter()

router.include_router(health_router, tags=["status"])
router.include_router(auth_router, tags=["auth"])
router.include_router(user_router, tags=["users"])
router.include_router(firefighter_router, tags=["firefighters"])
router.include_router(report_router, tags=["reports"])
router.include_router(occurrence_router, tags=["occurrences"])
router.include_router(media_router, tags=["media"])


__all__ = ["router"]
