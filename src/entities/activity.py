from typing import Optional

from entities.base import BaseEntity


class ActivityEntity(BaseEntity):
    name: str = None
    parent_id: Optional[int] = None
    parent: Optional["ActivityEntity"] = None
