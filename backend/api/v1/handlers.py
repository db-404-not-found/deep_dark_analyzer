from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from loguru import logger

from backend.api.v1.schemas import StatusResponseSchema


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    logger.info("Got exception {exc}", exc=exc)
    return JSONResponse(
        status_code=exc.status_code,
        content=StatusResponseSchema(
            message=exc.detail,
            status_code=exc.status_code,
        ).model_dump(),
    )
