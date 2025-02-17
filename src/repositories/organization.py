from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import aliased, selectinload

from entities.organization import OrganizationEntity
from models import (
    Activity as ActivityModel,
    Building as BuildingModel,
    OrganizationActivity as OrganizationActivityModel,
)
from models.organization import Organization as OrganizationModel
from repositories.base import OrganizationRepositoryProtocol
from utils import haversine


class OrganizationRepository(OrganizationRepositoryProtocol):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_key(self, key: int) -> Optional[OrganizationEntity]:
        query = (
            select(OrganizationModel)
            .options(
                selectinload(OrganizationModel.activities),
                selectinload(OrganizationModel.building),
            )
            .where(OrganizationModel.id == key)
        )
        result = await self.session.scalar(query)
        if result:
            return OrganizationEntity.model_validate(result, from_attributes=True)
        return None

    async def get_by_name(self, name: str) -> List[Optional[OrganizationEntity]]:
        query = (
            select(OrganizationModel)
            .options(
                selectinload(OrganizationModel.activities),
                selectinload(OrganizationModel.building),
            )
            .where(OrganizationModel.name == name)
        )
        result = await self.session.scalars(query)
        return [OrganizationEntity.model_validate(org, from_attributes=True) for org in result.all()]

    async def get_by_building_key(self, building_key: int) -> List[Optional[OrganizationEntity]]:
        query = (
            select(OrganizationModel)
            .options(
                selectinload(OrganizationModel.activities),
                selectinload(OrganizationModel.building),
            )
            .where(OrganizationModel.building_id == building_key)
        )
        result = await self.session.scalars(query)
        return [OrganizationEntity.model_validate(org, from_attributes=True) for org in result.all()]

    async def get_by_activity_key(self, activity_key: int) -> List[Optional[OrganizationEntity]]:
        query = (
            select(OrganizationModel)
            .join(OrganizationActivityModel)
            .options(
                selectinload(OrganizationModel.activities),
                selectinload(OrganizationModel.building),
            )
            .where(OrganizationActivityModel.activity_id == activity_key)
        )
        result = await self.session.scalars(query)
        return [OrganizationEntity.model_validate(org, from_attributes=True) for org in result.all()]

    async def get_by_activity_tree(self, activity_key: int) -> List[Optional[OrganizationEntity]]:
        activity_alias = aliased(ActivityModel)

        activity_tree = (
            select(ActivityModel.id).where(ActivityModel.id == activity_key).cte(name="activity_tree", recursive=True)
        )

        recursive_part = select(activity_alias.id).join(activity_tree, activity_alias.parent_id == activity_tree.c.id)

        activity_tree = activity_tree.union_all(recursive_part)

        query = (
            select(OrganizationModel)
            .distinct()
            .options(
                selectinload(OrganizationModel.activities),
                selectinload(OrganizationModel.building),
            )
            .join(
                OrganizationActivityModel,
                OrganizationModel.id == OrganizationActivityModel.organization_id,
            )
            .where(OrganizationActivityModel.activity_id.in_(select(activity_tree.c.id)))
        )

        result = await self.session.scalars(query)
        return [OrganizationEntity.model_validate(org, from_attributes=True) for org in result.all()]

    async def get_by_bbox(
        self, lat_min: float, lat_max: float, lon_min: float, lon_max: float
    ) -> List[Optional[OrganizationEntity]]:
        query = (
            select(OrganizationModel)
            .join(BuildingModel, OrganizationModel.building_id == BuildingModel.id)
            .options(
                selectinload(OrganizationModel.activities),
                selectinload(OrganizationModel.building),
            )
            .where(BuildingModel.latitude.between(lat_min, lat_max), BuildingModel.longitude.between(lon_min, lon_max))
        )
        result = await self.session.scalars(query)
        return [OrganizationEntity.model_validate(org, from_attributes=True) for org in result.all()]

    async def get_by_radius(self, lat: float, lon: float, radius: float) -> List[Optional[OrganizationEntity]]:
        query = select(OrganizationModel).options(
            selectinload(OrganizationModel.activities),
            selectinload(OrganizationModel.building),
        )
        result = await self.session.scalars(query)

        organizations = [
            org for org in result.all() if haversine(lat, lon, org.building.latitude, org.building.longitude) <= radius
        ]

        return [OrganizationEntity.model_validate(org, from_attributes=True) for org in organizations]

    async def create(self, organization: OrganizationEntity) -> OrganizationEntity:
        if not organization.activity_ids:
            raise ValueError("activity_ids не должны быть пустыми!")

        activities = await self.session.scalars(
            select(ActivityModel).where(ActivityModel.id.in_(organization.activity_ids))
        )
        organization_db = OrganizationModel(
            name=organization.name,
            phones=organization.phones,
            building_id=organization.building.key,
            activities=list(activities),
        )
        self.session.add(organization_db)
        await self.session.commit()
        await self.session.refresh(organization_db)
        return organization.model_copy(update={"key": organization_db.id})
