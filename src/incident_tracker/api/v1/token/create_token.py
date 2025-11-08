from typing import Annotated

from fastapi import APIRouter, Depends

from incident_tracker.api.v1.schemas.requests import CreateTokenRequestSchema
from incident_tracker.api.v1.schemas.responses import CreateTokenResponseSchema
from incident_tracker.common.stub import Stub
from incident_tracker.interactors.token import CreateTokenInteractor

create_token_router = APIRouter()


@create_token_router.post("/", response_model=CreateTokenResponseSchema)
async def create_token(
    request_data: CreateTokenRequestSchema,
    interactor: Annotated[CreateTokenInteractor, Depends(Stub(CreateTokenInteractor))],
):
    return await interactor(request_data)
