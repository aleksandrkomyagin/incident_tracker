from typing import Annotated

from fastapi import APIRouter, Depends

from incident_tracker.api.v1.schemas.requests import RevokeTokenRequestSchema
from incident_tracker.api.v1.schemas.responses import RevokeTokenResponseSchema
from incident_tracker.common.stub import Stub
from incident_tracker.interactors.token import RevokeTokenInteractor

revoke_router = APIRouter()


@revoke_router.post("/revoke", response_model=RevokeTokenResponseSchema)
async def revoke_token(
    request_data: RevokeTokenRequestSchema,
    interactor: Annotated[RevokeTokenInteractor, Depends(Stub(RevokeTokenInteractor))],
):
    return await interactor(request_data)
