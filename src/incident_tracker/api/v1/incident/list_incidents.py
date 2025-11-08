from enum import StrEnum
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from incident_tracker.api.auth import authorize
from incident_tracker.api.v1.schemas.responses import ListIncidentResponseSchema
from incident_tracker.common.stub import Stub
from incident_tracker.interactors.incident import ListIncidentInteractor

list_incidents_router = APIRouter()


class IncidentStatus(StrEnum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


@list_incidents_router.get(
    "/",
    dependencies=[Depends(authorize({"read"}))],
    response_model=ListIncidentResponseSchema,
)
async def list_incident(
    interactor: Annotated[
        ListIncidentInteractor, Depends(Stub(ListIncidentInteractor))
    ],
    status: Annotated[IncidentStatus | None, Query()] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=20, le=50)] = 50,
):
    return await interactor(status, page, page_size)
