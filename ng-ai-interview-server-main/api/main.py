from api.conf.config import Config
from api.infra.mongo.connection import init_mongodb
# from api.infra.mongo.connection import init_mongodb, MongoConnection

# Load configuration
config = Config.load_config()

# Initialize MongoDB
init_mongodb()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from loguru import logger
import uvicorn

from api.middleware.logging import LoggingMiddleware
from api.middleware.error_handler import (
    api_error_handler,
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler
)
from api.router import health, test, user, job, question, chat, test_result
from api.router import interview_graph_router
from api.exceptions.api_error import APIError


# Configure logging
logger.add(
    config.logging.file,
    level=config.logging.level,
    format=config.logging.format,
    rotation=config.logging.rotation
)

app = FastAPI(
    title=config.app.name,
    openapi_url=f"{config.app.api_v1_str}/openapi.yaml",
    docs_url=f"{config.app.api_v1_str}/doc",
)

# Add middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors.allow_origins,
    allow_credentials=config.cors.allow_credentials,
    allow_methods=config.cors.allow_methods,
    allow_headers=config.cors.allow_headers,
)
print("CORS config applied:", config.cors.allow_origins)


# Register exception handlers
app.add_exception_handler(APIError, api_error_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Register routers
app.include_router(health.router, prefix=config.app.api_v1_str)
app.include_router(test.router, prefix=config.app.api_v1_str)
app.include_router(user.router, prefix=config.app.api_v1_str)
app.include_router(job.router, prefix=config.app.api_v1_str)
app.include_router(question.router, prefix=config.app.api_v1_str)
app.include_router(chat.router, prefix=config.app.api_v1_str)
app.include_router(test_result.router, prefix=config.app.api_v1_str)
app.include_router(interview_graph_router.router, prefix="/api/v1/interview-graph")

# def shutdown_event():
#     MongoConnection.close_client()

# 在 FastAPI 应用中注册 shutdown 事件
# @app.on_event("shutdown")
# def shutdown():
#     shutdown_event()

# Run the API server
# source venv/bin/activate
# uvicorn api.main:app --reload
# http://127.0.0.1:8000/api/v1/doc


if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host=config.server.host,
        port=config.server.port,
        reload=config.server.reload
    ) 