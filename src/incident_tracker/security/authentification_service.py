from typing import Any

from incident_tracker.interfaces.services import IAuthenticateService, ITokenService
from incident_tracker.security.exceptions import (
    BearerSchemaRequiredException,
    TokenRequiredException,
)


def get_authorization_scheme_param(
    authorization_header_value: str | None,
) -> tuple[str, str]:
    scheme, param = authorization_header_value.split(" ")
    return scheme, param


class AuthenticateService(IAuthenticateService):
    def __init__(self, token_service: ITokenService) -> None:
        self._token_service = token_service

    async def authenticate(self, authorization_header: str | None) -> dict[str, Any]:
        if authorization_header is None:
            raise TokenRequiredException(message="Не передан токен доступа")
        scheme, token = get_authorization_scheme_param(authorization_header)
        if scheme.lower() != "bearer":
            raise BearerSchemaRequiredException(message="Некорректная схема токена")
        if not token:
            raise TokenRequiredException(message="Не передан токен доступа")
        return await self._token_service.decode_token(token)
