from typing import Annotated

from fastapi import APIRouter, Depends

from incident_tracker.api.v1.schemas.requests import RefreshTokenRequestSchema
from incident_tracker.api.v1.schemas.responses import RefreshTokenResponseSchema
from incident_tracker.common.stub import Stub
from incident_tracker.interactors.token import RefreshTokenInteractor

refresh_router = APIRouter()


@refresh_router.post("/refresh", response_model=RefreshTokenResponseSchema)
async def refresh_token(
    request_data: RefreshTokenRequestSchema,
    interactor: Annotated[
        RefreshTokenInteractor, Depends(Stub(RefreshTokenInteractor))
    ],
):
    return await interactor(request_data)
