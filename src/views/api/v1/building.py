from typing import List

from fastapi import APIRouter, Depends, Query, HTTPException

from dependencies.building import get_building_service
from dependencies.security import verify_api_key
from schemas.building import BuildingResponseSchema
from services.building import BuildingService

router = APIRouter(tags=["Buildings"])


@router.get(
    "/buildings/by-radius",
    description="список организаций, которые находятся в заданном радиусе относительно указанной точки на карте",
    response_model=List[BuildingResponseSchema],
)
async def get_buildings_by_radius(
    lat: float = Query(..., example="51.4711"),
    lon: float = Query(..., example="-0.2290"),
    radius: float = Query(..., example="3"),
    service: BuildingService = Depends(get_building_service),
    _: bool = Depends(verify_api_key),
):
    buildings = await service.get_by_radius(lat, lon, radius)
    if not buildings:
        raise HTTPException(status_code=404, detail="No buildings found")
    return [BuildingResponseSchema.from_entity(building) for building in buildings]


@router.get(
    "/buildings/by-bbox",
    description="список организаций, которые находятся в заданной прямоугольной области "
    "относительно указанной точки на карте",
    response_model=List[BuildingResponseSchema],
)
async def get_buildings_by_bbox(
    lat_min: float = Query(..., example="51.4711"),
    lat_max: float = Query(..., example="51.4986"),
    lon_min: float = Query(..., example="-0.2290"),
    lon_max: float = Query(..., example="-0.0979"),
    service: BuildingService = Depends(get_building_service),
    _: bool = Depends(verify_api_key),
):
    buildings = await service.get_by_bbox(lat_min=lat_min, lat_max=lat_max, lon_min=lon_min, lon_max=lon_max)
    if not buildings:
        raise HTTPException(status_code=404, detail="No buildings found")
    return [BuildingResponseSchema.from_entity(building) for building in buildings]
