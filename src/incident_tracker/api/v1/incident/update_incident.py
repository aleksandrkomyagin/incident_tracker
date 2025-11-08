from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path

from incident_tracker.api.auth import authorize
from incident_tracker.api.v1.schemas.requests import NewIncidentStatusRequestSchema
from incident_tracker.api.v1.schemas.responses import IncidentResponseSchema
from incident_tracker.common.stub import Stub
from incident_tracker.interactors.incident import ChangeIncidentStatusInteractor

update_incident_router = APIRouter()


@update_incident_router.patch(
    "/{incident_id}",
    dependencies=[Depends(authorize({"write"}))],
    response_model=IncidentResponseSchema,
)
async def change_incident_status(
    incident_id: Annotated[UUID, Path()],
    request_data: NewIncidentStatusRequestSchema,
    interactor: Annotated[
        ChangeIncidentStatusInteractor, Depends(Stub(ChangeIncidentStatusInteractor))
    ],
):
    return await interactor(str(incident_id), request_data)
