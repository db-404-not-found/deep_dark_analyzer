from pydantic import BaseModel


class StatusResponseSchema(BaseModel):
    status_code: int
    message: str
