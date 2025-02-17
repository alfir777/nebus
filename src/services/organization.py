from typing import List, Optional

from entities.organization import OrganizationEntity
from repositories.base import OrganizationRepositoryProtocol


class OrganizationService:
    def __init__(self, organization_repo: OrganizationRepositoryProtocol):
        self.organization_repo = organization_repo

    async def create(self, organization: OrganizationEntity):
        return await self.organization_repo.create(organization)

    async def get_by_key(self, organization_id: int) -> Optional[OrganizationEntity]:
        return await self.organization_repo.get_by_key(key=organization_id)

    async def get_by_building_key(self, building_key: int) -> Optional[List[OrganizationEntity]]:
        organizations = await self.organization_repo.get_by_building_key(building_key)
        return [OrganizationEntity.model_validate(org) for org in organizations]

    async def get_organizations_by_activity_key(self, activity_key: int) -> Optional[List[OrganizationEntity]]:
        return await self.organization_repo.get_by_activity_key(activity_key)

    async def get_by_activity_tree(self, activity_id: int) -> List[OrganizationEntity]:
        return await self.organization_repo.get_by_activity_tree(activity_id)

    async def get_by_bbox(
        self, lat_min: float, lat_max: float, lon_min: float, lon_max: float
    ) -> List[Optional[OrganizationEntity]]:
        return await self.organization_repo.get_by_bbox(
            lat_min=lat_min, lat_max=lat_max, lon_min=lon_min, lon_max=lon_max
        )

    async def get_by_radius(self, lat: float, lon: float, radius: float) -> List[Optional[OrganizationEntity]]:
        return await self.organization_repo.get_by_radius(lat, lon, radius)

    async def get_organization(self, org_id: int):
        return await self.organization_repo.get_by_key(org_id)

    async def get_by_name(self, name: str) -> List[Optional[OrganizationEntity]]:
        return await self.organization_repo.get_by_name(name)
