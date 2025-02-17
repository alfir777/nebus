from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from repositories.building import BuildingRepository
from services.building import BuildingService


def get_building_service(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    repo = BuildingRepository(session=session)
    return BuildingService(building_repo=repo)
