from pydantic import BaseModel


class ActivityResponseSchema(BaseModel):
    name: str
