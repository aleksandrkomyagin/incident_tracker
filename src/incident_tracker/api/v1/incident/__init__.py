from fastapi import APIRouter

from .list_incidents import list_incidents_router
from .new_incident import new_incident_router
from .update_incident import update_incident_router

incident_router = APIRouter(prefix="/incidents", tags=["incidents"])

incident_router.include_router(list_incidents_router)
incident_router.include_router(new_incident_router)
incident_router.include_router(update_incident_router)
