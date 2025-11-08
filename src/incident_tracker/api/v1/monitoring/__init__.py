from fastapi import APIRouter

from .health import health_router

monitoring_router = APIRouter(prefix="/monitoring", tags=["monitoring"])

monitoring_router.include_router(health_router)
