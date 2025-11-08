from logging import getLogger

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from incident_tracker.common.exceptions.base import (
    BaseAppException,
    BaseAuthException,
    BaseDetailException,
    BaseInfraException,
    BasePermissionException,
)

logger = getLogger(__name__)


def register_exception_handler(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        return JSONResponse(
            content={"detail": exc.errors()},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    @app.exception_handler(BaseAuthException)
    async def auth_exception_handler(request: Request, exc: BaseAuthException):
        return JSONResponse(
            {"message": exc.message},
            status_code=exc.status_code,
        )

    @app.exception_handler(BasePermissionException)
    async def permission_exception_handler(
        request: Request, exc: BasePermissionException
    ):
        return JSONResponse(
            {"message": exc.message},
            status_code=exc.status_code,
        )

    @app.exception_handler(BaseAppException)
    async def app_exception_handler(request: Request, exc: BaseDetailException):
        if isinstance(exc.__cause__, BaseInfraException):
            exc.response_data["detail"]["text"] = "Внутренняя ошибка сервера"
            return JSONResponse(exc.response_data, status_code=exc.status_code)
        return JSONResponse(exc.response_data, status_code=exc.status_code)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            {"message": "Внутренняя ошибка сервера"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
