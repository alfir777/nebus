from typing import List, Optional

from entities.building import BuildingEntity
from repositories.base import BuildingRepositoryProtocol


class BuildingService:
    def __init__(self, building_repo: BuildingRepositoryProtocol):
        self.building_repo = building_repo

    async def get(self, building_key: int) -> BuildingEntity:
        return await self.building_repo.get_by_key(building_key)

    async def create(self, building: BuildingEntity) -> BuildingEntity:
        return await self.building_repo.create(building)

    async def get_by_bbox(
        self, lat_min: float, lat_max: float, lon_min: float, lon_max: float
    ) -> List[Optional[BuildingEntity]]:
        return await self.building_repo.get_by_bbox(lat_min=lat_min, lat_max=lat_max, lon_min=lon_min, lon_max=lon_max)

    async def get_by_radius(self, lat: float, lon: float, radius: float) -> List[Optional[BuildingEntity]]:
        return await self.building_repo.get_by_radius(lat, lon, radius)
