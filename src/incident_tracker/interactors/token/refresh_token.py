from incident_tracker.api.v1.schemas.requests import RefreshTokenRequestSchema
from incident_tracker.api.v1.schemas.responses import RefreshTokenResponseSchema
from incident_tracker.common.exceptions.base import BaseAppException, BaseInfraException
from incident_tracker.interfaces.services import ITokenService
from incident_tracker.services.exceptions import TokenRefreshException


class RefreshTokenInteractor:
    def __init__(self, token_service: ITokenService):
        self._token_service = token_service

    async def __call__(
        self, request_data: RefreshTokenRequestSchema
    ) -> RefreshTokenResponseSchema:
        try:
            token = await self._token_service.refresh_token(request_data.refresh_token)
        except (BaseAppException, BaseInfraException) as e:
            raise TokenRefreshException(
                status_code=e.status_code,
                message="Ошибка обновления токена",
                detail=str(e.message),
            ) from e

        return RefreshTokenResponseSchema(
            access_token=token.access_token, refresh_token=token.refresh_token
        )
