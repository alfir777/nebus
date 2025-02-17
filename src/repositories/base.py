from typing import Protocol, Optional, List

from entities.activity import ActivityEntity
from entities.building import BuildingEntity
from entities.organization import OrganizationEntity


class ActivityRepositoryProtocol(Protocol):
    async def get_by_key(self, key: int) -> ActivityEntity:
        pass

    async def create(self, activity: ActivityEntity) -> ActivityEntity:
        pass


class BuildingRepositoryProtocol(Protocol):
    async def get_by_key(self, key: int) -> Optional[BuildingEntity]:
        pass

    async def create(self, building: BuildingEntity) -> BuildingEntity:
        pass

    async def get_by_bbox(
        self, lat_min: float, lat_max: float, lon_min: float, lon_max: float
    ) -> List[Optional[BuildingEntity]]:
        pass

    async def get_by_radius(self, lat: float, lon: float, radius: float) -> List[Optional[BuildingEntity]]:
        pass


class OrganizationRepositoryProtocol(Protocol):
    async def get_by_key(self, key: int) -> Optional[OrganizationEntity]:
        pass

    async def create(self, organization: OrganizationEntity) -> OrganizationEntity:
        pass

    async def get_by_building_key(self, building_key: int) -> Optional[List[OrganizationEntity]]:
        pass

    async def get_by_activity_key(self, activity_key: int) -> Optional[List[OrganizationEntity]]:
        pass

    async def get_by_activity_tree(self, activity_key: int) -> List[Optional[OrganizationEntity]]:
        pass

    async def get_by_bbox(
        self, lat_min: float, lat_max: float, lon_min: float, lon_max: float
    ) -> List[Optional[OrganizationEntity]]:
        pass

    async def get_by_radius(self, lat: float, lon: float, radius: float) -> List[Optional[OrganizationEntity]]:
        pass

    async def get_by_name(self, name: str) -> List[Optional[OrganizationEntity]]:
        pass
