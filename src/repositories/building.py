from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from entities.building import BuildingEntity
from models import Building
from models import (
    Building as BuildingModel,
)
from repositories.base import BuildingRepositoryProtocol
from utils import haversine


class BuildingRepository(BuildingRepositoryProtocol):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, building: BuildingEntity) -> BuildingEntity:
        building_db = Building(**building.convert_to_db_dict())
        self.session.add(building_db)
        await self.session.commit()
        await self.session.refresh(building_db)
        return building.model_copy(update={"key": building_db.id})

    async def get_by_radius(self, lat: float, lon: float, radius: float) -> List[Optional[BuildingEntity]]:
        query = select(BuildingModel).options(
            selectinload(BuildingModel.organizations),
        )
        result = await self.session.scalars(query)

        buildings = [
            building
            for building in result.all()
            if haversine(lat, lon, building.latitude, building.longitude) <= radius
        ]

        return [BuildingEntity.model_validate(building, from_attributes=True) for building in buildings]

    async def get_by_bbox(
        self, lat_min: float, lat_max: float, lon_min: float, lon_max: float
    ) -> List[Optional[BuildingEntity]]:
        query = (
            select(BuildingModel)
            .options(
                selectinload(BuildingModel.organizations),
            )
            .where(BuildingModel.latitude.between(lat_min, lat_max), BuildingModel.longitude.between(lon_min, lon_max))
        )
        result = await self.session.scalars(query)
        return [BuildingEntity.model_validate(building, from_attributes=True) for building in result.all()]
