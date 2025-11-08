from typing import Annotated

from fastapi import APIRouter, Depends

from incident_tracker.api.v1.schemas.requests import NewServiceRequestSchema
from incident_tracker.api.v1.schemas.responses import ServiceResponseSchema
from incident_tracker.common.stub import Stub
from incident_tracker.interactors.service import CreateNewServiceInteractor

new_service_router = APIRouter()


@new_service_router.post("/", response_model=ServiceResponseSchema)
async def new_service(
    request_data: NewServiceRequestSchema,
    interactor: Annotated[
        CreateNewServiceInteractor, Depends(Stub(CreateNewServiceInteractor))
    ],
):
    return await interactor(request_data)
