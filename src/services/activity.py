from core.exceptions import EntityNotFound, DepthLimitExceeded
from entities.activity import ActivityEntity
from repositories.activity import ActivityRepository


class ActivityService:
    def __init__(self, activity_repo: ActivityRepository):
        self.activity_repo = activity_repo

    async def create(self, activity: ActivityEntity) -> ActivityEntity:
        """Создаёт деятельность, ограничивая уровень вложенности 3 уровнями"""
        if activity.parent_id:
            parent = await self.activity_repo.get_by_key(activity.parent_id)
            if not parent:
                raise EntityNotFound("Родительская деятельность не найдена")

            if parent.parent_id:
                grandparent = await self.activity_repo.get_by_key(parent.parent_id)
                if grandparent and grandparent.parent_id:
                    raise DepthLimitExceeded("Достигнут максимальный уровень вложенности (3)")

        activity_db = await self.activity_repo.create(activity)
        return ActivityEntity.model_validate(activity_db)
