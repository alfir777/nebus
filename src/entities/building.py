from entities.base import BaseEntity


class BuildingEntity(BaseEntity):
    address: str
    latitude: float
    longitude: float
