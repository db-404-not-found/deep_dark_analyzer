from fastapi import APIRouter

from backend.api.v1.inference.router import router as inference_router
from backend.api.v1.monitoring.router import router as monitoring_router

router = APIRouter(prefix="/v1")
router.include_router(monitoring_router)
router.include_router(inference_router)
