import os

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from pydantic_core import ValidationError

from app.api.main import api_router
from app.core.config import settings
from app.exceptions import CustomHTTPException
from app.utils.response import create_response

if not os.path.exists(settings.DATA_DIRECTORY):
    os.makedirs(settings.DATA_DIRECTORY)

if not os.path.exists(settings.IMAGES_DIRECTORY):
    os.makedirs(settings.IMAGES_DIRECTORY)


async def route_not_found(request: Request, exc: HTTPException):
    return create_response(
        status_code=exc.status_code,
        success=False,
        message=exc.detail,
    )


async def internal_server_error(request: Request, exc: HTTPException):
    return create_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        success=False,
        message="Internal Server Error",
    )


app = FastAPI(
    default_response_class=ORJSONResponse,
    exception_handlers={
        404: route_not_found,
        500: internal_server_error,
    },
)


@app.exception_handler(CustomHTTPException)
async def custom_http_exception_handler(request: Request, exc: CustomHTTPException):
    return create_response(
        status_code=exc.status_code, success=exc.success, message=exc.message
    )


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: ValidationError):
    return create_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        success=False,
        message="Request Validation Failed",
        errors=exc.errors(),
    )


app.include_router(api_router)
