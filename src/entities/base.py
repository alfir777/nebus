from typing import Optional

from pydantic import BaseModel, Field


class BaseEntity(BaseModel):
    key: Optional[int] = Field(default=None, alias="id")

    def convert_to_db_dict(self) -> dict:
        return self.model_dump(exclude_none=True, by_alias=True)
