from typing import Literal

from pydantic import BaseModel


class MonitoringSchema(BaseModel):
    status: Literal["ok"]
