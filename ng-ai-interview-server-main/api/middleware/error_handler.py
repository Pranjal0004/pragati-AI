from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from api.exceptions.api_error import APIError
from api.model.api.base import Response
from loguru import logger

async def api_error_handler(request: Request, exc: APIError) -> JSONResponse:
    """Handle API errors"""
    logger.error(f"API error: {exc.message}")
    return JSONResponse(
        status_code=int(exc.code),
        content=Response(
            code=exc.code,
            message=exc.message,
            data=None
        ).model_dump()
    )

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTP exceptions"""
    logger.error(f"HTTP error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content=Response(
            code=str(exc.status_code),
            message=exc.detail,
            data=None
        ).model_dump()
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle validation errors"""
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content=Response(
            code="422",
            message="Validation error",
            data={"errors": exc.errors()}
        ).model_dump()
    )

async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected errors"""
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content=Response(
            code="500",
            message="Internal server error",
            data=None
        ).model_dump()
    ) 