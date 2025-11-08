from fastapi import APIRouter

from .incident import incident_router
from .monitoring import monitoring_router
from .services import service_router
from .token import token_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(incident_router)
v1_router.include_router(monitoring_router)
v1_router.include_router(service_router)
v1_router.include_router(token_router)
