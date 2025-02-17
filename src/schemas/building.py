from pydantic import BaseModel

from entities.building import BuildingEntity


class BuildingResponseSchema(BaseModel):
    address: str
    latitude: float
    longitude: float

    @staticmethod
    def from_entity(building: BuildingEntity) -> "BuildingResponseSchema":
        return BuildingResponseSchema(
            address=building.address, latitude=building.latitude, longitude=building.longitude
        )
