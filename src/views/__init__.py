from fastapi import APIRouter

from core.config import settings
from .api import router as api_router

router = APIRouter(
    prefix=settings.api.prefix,
)
router.include_router(api_router)
