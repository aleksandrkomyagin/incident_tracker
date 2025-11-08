from typing import Annotated

from fastapi import APIRouter, Depends

from incident_tracker.api.auth import authorize
from incident_tracker.api.v1.schemas.requests import NewIncidentRequestSchema
from incident_tracker.api.v1.schemas.responses import IncidentResponseSchema
from incident_tracker.common.stub import Stub
from incident_tracker.interactors.incident import CreateNewIncidentInteractor

new_incident_router = APIRouter()


@new_incident_router.post(
    "/",
    dependencies=[Depends(authorize({"write"}))],
    response_model=IncidentResponseSchema,
)
async def new_incident(
    request_data: NewIncidentRequestSchema,
    interactor: Annotated[
        CreateNewIncidentInteractor, Depends(Stub(CreateNewIncidentInteractor))
    ],
):
    return await interactor(request_data)
