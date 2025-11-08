from fastapi import APIRouter

from .add_service import new_service_router

service_router = APIRouter(prefix="/services", tags=["services"])

service_router.include_router(new_service_router)
