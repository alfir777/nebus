from typing import List

from entities.activity import ActivityEntity
from entities.base import BaseEntity
from entities.building import BuildingEntity


class OrganizationEntity(BaseEntity):
    name: str
    phones: list[str]
    building: BuildingEntity
    activities: List[ActivityEntity]

    class Config:
        from_attributes = True

    @property
    def activity_ids(self):
        return [activity.key for activity in self.activities]
