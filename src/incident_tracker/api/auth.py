from typing import Annotated

from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from incident_tracker.common.stub import Stub
from incident_tracker.interfaces.services import (
    IAuthenticateService,
    IAuthorizationService,
)

security = HTTPBearer(auto_error=False)


async def authenticate(
    authentication_service: Annotated[
        IAuthenticateService, Depends(Stub(IAuthenticateService))
    ],
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    authorization_data = (
        f"{credentials.scheme} {credentials.credentials}" if credentials else None
    )
    return await authentication_service.authenticate(authorization_data)


def authorize(required_roles: set[str]):
    async def dependency(
        token_payload: Annotated[dict, Depends(authenticate)],
        authorization_service: Annotated[
            IAuthorizationService, Depends(Stub(IAuthorizationService))
        ],
    ) -> None:
        await authorization_service.authorize(token_payload, required_roles)

    return dependency
