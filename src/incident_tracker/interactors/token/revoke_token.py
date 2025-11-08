from incident_tracker.api.v1.schemas.requests import RevokeTokenRequestSchema
from incident_tracker.api.v1.schemas.responses import RevokeTokenResponseSchema
from incident_tracker.common.exceptions.base import BaseAppException, BaseInfraException
from incident_tracker.interfaces.services import ITokenService
from incident_tracker.services.exceptions import TokenRevocationException


class RevokeTokenInteractor:
    def __init__(self, token_service: ITokenService):
        self._token_service = token_service

    async def __call__(
        self, request_data: RevokeTokenRequestSchema
    ) -> RevokeTokenResponseSchema:
        try:
            await self._token_service.revoke_token(request_data.refresh_token)
        except (BaseAppException, BaseInfraException) as e:
            raise TokenRevocationException(
                status_code=e.status_code,
                message="Ошибка отзыва токена",
                detail=str(e.message),
            ) from e

        return RevokeTokenResponseSchema(message="Токен отозван")
