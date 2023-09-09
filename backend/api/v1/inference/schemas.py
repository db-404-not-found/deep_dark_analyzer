from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from backend.db.models import Status


class QuestionQuerySchema(BaseModel):
    press_release: str


class QuestionResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: Status
    result: dict = Field(default_factory=dict)
