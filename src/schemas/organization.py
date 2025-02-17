from pydantic import BaseModel
from typing import List

from entities.organization import OrganizationEntity


class OrganizationResponseSchema(BaseModel):
    name: str
    phones: List[str]
    address: str
    activities: List[str]

    @staticmethod
    def from_entity(organization: OrganizationEntity) -> "OrganizationResponseSchema":
        return OrganizationResponseSchema(
            name=organization.name,
            phones=organization.phones,
            address=organization.building.address,
            activities=[activity.name for activity in organization.activities],
        )
