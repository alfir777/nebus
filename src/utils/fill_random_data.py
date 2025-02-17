import os
import random
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import DepthLimitExceeded
from core.models import db_helper
from entities.activity import ActivityEntity
from entities.building import BuildingEntity
from entities.organization import OrganizationEntity
from repositories.activity import ActivityRepository
from repositories.building import BuildingRepository
from repositories.organization import OrganizationRepository
from services.activity import ActivityService
from services.building import BuildingService
from services.organization import OrganizationService

FILL_TEST_DATA = os.getenv("FILL_TEST_DATA", "False").lower() == "true"


async def fill_test_data(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    organization_service = OrganizationService(organization_repo=OrganizationRepository(session))
    organization = await organization_service.get_by_key(organization_id=1)
    if organization:
        raise ValueError("Test data already exists")
    activity_service = ActivityService(activity_repo=ActivityRepository(session))
    building_service = BuildingService(building_repo=BuildingRepository(session))
    food = await activity_service.create(ActivityEntity(name="Еда"))
    meat = await activity_service.create(ActivityEntity(name="Мясная продукция", parent_id=food.key))
    dairy = await activity_service.create(ActivityEntity(name="Молочная продукция", parent_id=food.key))
    bakery = await activity_service.create(ActivityEntity(name="Хлебобулочные изделия", parent_id=food.key))

    it = await activity_service.create(ActivityEntity(name="IT"))
    software = await activity_service.create(ActivityEntity(name="Разработка ПО", parent_id=it.key))
    cybersecurity = await activity_service.create(ActivityEntity(name="Кибербезопасность", parent_id=it.key))

    auto = await activity_service.create(ActivityEntity(name="Авто"))
    car_service = await activity_service.create(ActivityEntity(name="Автосервис", parent_id=auto.key))
    car_rental = await activity_service.create(ActivityEntity(name="Прокат авто", parent_id=auto.key))

    bread = await activity_service.create(ActivityEntity(name="Хлеб", parent_id=bakery.key))
    try:
        _ = await activity_service.create(ActivityEntity(name="Белый хлеб", parent_id=bread.key))
    except DepthLimitExceeded:
        pass
    else:
        raise AssertionError("DepthLimitExceeded not raised")

    activities = [
        food,
        meat,
        dairy,
        bakery,
        it,
        software,
        cybersecurity,
        auto,
        car_service,
        car_rental,
    ]
    buildings = [
        await building_service.create(
            BuildingEntity(
                address=f"Улица {i}, Дом {random.randint(1, 50)}",
                latitude=51.515663419306904 + random.uniform(-0.05, 0.05),
                longitude=-0.20893541598101087 + random.uniform(-0.05, 0.05),
            )
        )
        for i in range(1, 11)
    ]

    _ = [
        await organization_service.create(
            OrganizationEntity(
                name=f"Компания {i}",
                phones=[
                    f"+7707{random.randint(1000000, 9999999)}",
                    f"+7707{random.randint(1000000, 9999999)}",
                ],
                building=random.choice(buildings),
                activities=[random.choice(activities) for _ in range(random.randint(1, 3))],
            )
        )
        for i in range(1, 21)
    ]
