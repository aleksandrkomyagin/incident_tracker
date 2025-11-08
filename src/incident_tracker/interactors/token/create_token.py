from incident_tracker.api.v1.schemas.requests import CreateTokenRequestSchema
from incident_tracker.api.v1.schemas.responses import CreateTokenResponseSchema
from incident_tracker.common.exceptions.base import BaseAppException, BaseInfraException
from incident_tracker.interfaces.services import ITokenService
from incident_tracker.services.exceptions import TokenCreationException


class CreateTokenInteractor:
    def __init__(self, token_service: ITokenService):
        self._token_service = token_service

    async def __call__(
        self, request_data: CreateTokenRequestSchema
    ) -> CreateTokenResponseSchema:
        try:
            token = await self._token_service.create_token(request_data.service_id)
        except (BaseAppException, BaseInfraException) as e:
            raise TokenCreationException(
                status_code=e.status_code,
                message="Ошибка обновления токена",
                detail=str(e.message),
            ) from e

        return CreateTokenResponseSchema(
            access_token=token.access_token, refresh_token=token.refresh_token
        )
