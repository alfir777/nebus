from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from dependencies.organization import get_organization_service
from dependencies.security import verify_api_key
from schemas.organization import OrganizationResponseSchema
from services.organization import OrganizationService

router = APIRouter(tags=["Organizations"])


@router.get(
    "/organizations/by-building/{building_id}",
    description="список всех организаций находящихся в конкретном здании",
    response_model=List[OrganizationResponseSchema],
)
async def get_organizations_by_building(
    building_id: int,
    service: OrganizationService = Depends(get_organization_service),
    _: bool = Depends(verify_api_key),
):
    organizations = await service.get_by_building_key(building_id)
    if not organizations:
        raise HTTPException(status_code=404, detail="Organization not found")
    return [OrganizationResponseSchema.from_entity(organization) for organization in organizations]


@router.get(
    "/organizations/by-activity/{activity_id}",
    description="список всех организаций, которые относятся к указанному виду деятельности",
    response_model=List[OrganizationResponseSchema],
)
async def get_organizations_by_activity(
    activity_id: int,
    service: OrganizationService = Depends(get_organization_service),
    _: bool = Depends(verify_api_key),
):
    organizations = await service.get_organizations_by_activity_key(activity_id)
    if not organizations:
        raise HTTPException(status_code=404, detail="Organization not found")
    return [OrganizationResponseSchema.from_entity(organization) for organization in organizations]


@router.get("/organizations/by-activity-tree/{activity_id}", response_model=List[OrganizationResponseSchema])
async def get_organizations_by_activity_tree(
    activity_id: int,
    service: OrganizationService = Depends(get_organization_service),
    _: bool = Depends(verify_api_key),
):
    organizations = await service.get_by_activity_tree(activity_id)
    if not organizations:
        raise HTTPException(status_code=404, detail="Organization not found")
    return [OrganizationResponseSchema.from_entity(organization) for organization in organizations]


@router.get(
    "/organizations/by-radius",
    description="список организаций, которые находятся в заданном радиусе относительно указанной точки на карте",
    response_model=List[OrganizationResponseSchema],
)
async def get_organizations_by_radius(
    lat: float = Query(..., example="51.4711"),
    lon: float = Query(..., example="-0.2290"),
    radius: float = Query(..., example="3"),
    service: OrganizationService = Depends(get_organization_service),
    _: bool = Depends(verify_api_key),
):
    organizations = await service.get_by_radius(lat, lon, radius)
    if not organizations:
        raise HTTPException(status_code=404, detail="Organization not found")
    return [OrganizationResponseSchema.from_entity(organization) for organization in organizations]


@router.get(
    "/organizations/by-bbox",
    description="список организаций, которые находятся в заданной прямоугольной области "
    "относительно указанной точки на карте",
    response_model=List[OrganizationResponseSchema],
)
async def get_organizations_by_bbox(
    lat_min: float = Query(..., example="51.4711"),
    lat_max: float = Query(..., example="51.4986"),
    lon_min: float = Query(..., example="-0.2290"),
    lon_max: float = Query(..., example="-0.0979"),
    service: OrganizationService = Depends(get_organization_service),
    _: bool = Depends(verify_api_key),
):
    organizations = await service.get_by_bbox(lat_min=lat_min, lat_max=lat_max, lon_min=lon_min, lon_max=lon_max)
    if not organizations:
        raise HTTPException(status_code=404, detail="Organization not found")
    return [OrganizationResponseSchema.from_entity(organization) for organization in organizations]


@router.get(
    "/organizations/by-name",
    description="поиск организации по названию",
    response_model=List[OrganizationResponseSchema],
)
async def get_by_name(
    name: str, service: OrganizationService = Depends(get_organization_service), _: bool = Depends(verify_api_key)
):
    organizations = await service.get_by_name(name)
    if not organizations:
        raise HTTPException(status_code=404, detail="Organization not found")
    return [OrganizationResponseSchema.from_entity(organization) for organization in organizations]


@router.get(
    "/organizations/{organization_id}",
    description="вывод информации об организации по её идентификатору",
    response_model=OrganizationResponseSchema,
)
async def get_organization_by_id(
    organization_id: int,
    service: OrganizationService = Depends(get_organization_service),
    _: bool = Depends(verify_api_key),
) -> OrganizationResponseSchema:
    organization = await service.get_by_key(organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return OrganizationResponseSchema.from_entity(organization)
