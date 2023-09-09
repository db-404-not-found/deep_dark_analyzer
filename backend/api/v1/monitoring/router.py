from fastapi import APIRouter

from backend.api.v1.monitoring.schemas import MonitoringSchema

router = APIRouter(tags=["monitoring"], prefix="/monitoring")


@router.get("/ping")
async def ping() -> MonitoringSchema:
    return MonitoringSchema(status="ok")
