from fastapi import APIRouter

from .v1.organization import router as organization_router
from .v1.common import router as common_router
from .v1.building import router as building_router


router = APIRouter()

router.include_router(common_router)
router.include_router(organization_router)
router.include_router(building_router)
