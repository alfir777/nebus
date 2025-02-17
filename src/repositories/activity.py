from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.constants import DEPTH_OF_ACTIVITY
from core.exceptions import EntityNotFound
from entities.activity import ActivityEntity
from models import Activity as ActivityModel
from repositories.base import ActivityRepositoryProtocol


class ActivityRepository(ActivityRepositoryProtocol):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _map_to_entity(self, activity: ActivityModel | None, depth: int) -> ActivityEntity | None:
        if not activity:
            return None
        if depth == 0:
            parent_model = await activity.awaitable_attrs.parent
            parent_entity = await self._map_to_entity(parent_model, DEPTH_OF_ACTIVITY - 1)
        else:
            parent_entity = await self._map_to_entity(activity.parent, depth - 1)
        return ActivityEntity(id=activity.id, name=activity.name, parent_id=activity.parent_id, parent=parent_entity)

    async def create(self, activity: ActivityEntity) -> ActivityEntity:
        activity_db = ActivityModel(**activity.convert_to_db_dict())
        self.session.add(activity_db)
        await self.session.commit()
        await self.session.refresh(activity_db)
        return activity.model_copy(update={"key": activity_db.id})

    async def get_by_key(self, activity_key: int) -> ActivityEntity:
        stmt = select(ActivityModel).options(joinedload(ActivityModel.parent)).filter_by(id=activity_key)
        result = await self.session.execute(stmt)
        activity_db = result.scalars().first()

        if not activity_db:
            raise EntityNotFound

        return await self._map_to_entity(activity=activity_db, depth=DEPTH_OF_ACTIVITY)
