import uuid

from datetime import datetime, timedelta, timezone
from logging import getLogger
from typing import Any

import jwt

from incident_tracker.dto.token import TokenDTO
from incident_tracker.interfaces.crypto import IRSAKeyManager
from incident_tracker.interfaces.repositories import IServiceRepository
from incident_tracker.interfaces.services import ICacheService, ITokenService
from incident_tracker.services.exceptions import (
    InvalidTokenException,
    InvalidTokenIssuerException,
    InvalidTokenJTIException,
    InvalidTokenTypeException,
    MakeTokenException,
    ServiceNotFoundException,
    TokenExpiredException,
    TokenIsRevokedException,
)
from incident_tracker.setup.config import settings

logger = getLogger(__name__)


class TokenService(ITokenService):
    def __init__(
        self,
        cache_service: ICacheService,
        rsa_key_manager: IRSAKeyManager,
        service_repository: IServiceRepository,
    ) -> None:
        self._cache = cache_service
        self._rsa_key_manager = rsa_key_manager
        self._service_repository = service_repository

    async def _get_current_rsa_key(self) -> str:
        return await self._cache.get("current_rsa_key")

    @staticmethod
    def _make_payload(
        service_id: str,
        expire: datetime,
        token_type: str,
        scopes: list[str] | None = None,
    ) -> dict:
        payload = {
            "service_id": service_id,
            "exp": expire,
            "jti": str(uuid.uuid4()),
            "iss": settings.token_config.issuer,
            "type": token_type,
        }
        if token_type == "access":
            payload["scopes"] = scopes

        return payload

    async def _validate_token_payload(self, payload: dict[str, Any]) -> str:
        jti = payload.get("jti", None)
        if not jti:
            raise InvalidTokenJTIException(message="Некорректный токен")

        token = await self._cache.get(f"revoked:{jti}")
        if token:
            raise TokenIsRevokedException(message="Токен отозван")

        token_type = payload.get("type", None)
        if not token_type or token_type != "refresh":
            raise InvalidTokenTypeException(message="Неверный тип токена")

        issuer = payload.get("iss", None)
        if not issuer or issuer != settings.token_config.issuer:
            raise InvalidTokenIssuerException(message="Неверный издатель токена")

        return payload["service_id"]

    async def _decode_token(self, token: str) -> dict[str, Any]:
        private_pem = await self._get_current_rsa_key()
        try:
            public_key = self._rsa_key_manager.get_public_key(private_pem)
            payload = jwt.decode(
                jwt=token,
                key=public_key,
                algorithms=settings.token_config.algorithm,
                issuer=settings.token_config.issuer,
            )
        except jwt.ExpiredSignatureError as e:
            raise TokenExpiredException(message="Срок действия токена истек") from e
        except jwt.InvalidTokenError as e:
            raise InvalidTokenException(message="Некорректный токен") from e
        except jwt.PyJWTError as e:
            raise InvalidTokenException(message="Некорректный токен") from e

        return payload

    async def _make_token(
        self, service_id: str, scopes: list[str] | None = None
    ) -> dict[str, str]:
        private_pem = await self._get_current_rsa_key()
        if not private_pem:
            private_pem = self._rsa_key_manager.generate_key()
            await self._cache.set("current_rsa_key", private_pem)
        try:
            access_token_expire = datetime.now(timezone.utc) + timedelta(minutes=10)
            refresh_token_expire = datetime.now(timezone.utc) + timedelta(days=1)
            access_token = jwt.encode(
                payload=self._make_payload(
                    service_id, access_token_expire, "access", scopes
                ),
                key=private_pem,
                algorithm=settings.token_config.algorithm,
            )
            refresh_token = jwt.encode(
                payload=self._make_payload(service_id, refresh_token_expire, "refresh"),
                key=private_pem,
                algorithm=settings.token_config.algorithm,
            )
        except jwt.PyJWTError as e:
            raise MakeTokenException(message="Ошибка создания токена") from e
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    async def create_token(self, service_id: str) -> TokenDTO:
        service = await self._service_repository.get_service_by_id(service_id)
        if not service:
            raise ServiceNotFoundException(message="Сервис не найден")
        token = await self._make_token(str(service.id), service.scopes)
        return TokenDTO(
            access_token=token["access_token"], refresh_token=token["refresh_token"]
        )

    async def decode_token(self, token: str) -> dict[str, Any]:
        return await self._decode_token(token)

    async def revoke_token(self, refresh_token: str) -> None:
        payload = await self._decode_token(refresh_token)
        exp_dt = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        await self._cache.set(
            f"revoked:{payload['jti']}",
            "1",
            expire=int((exp_dt - datetime.now(timezone.utc)).total_seconds()),
        )

    async def refresh_token(self, refresh_token: str) -> TokenDTO:
        payload = await self._decode_token(refresh_token)
        service_id = await self._validate_token_payload(payload)
        service = await self._service_repository.get_service_by_id(service_id)
        if not service:
            raise ServiceNotFoundException(message="Сервис не найден")
        token = await self._make_token(service_id, service.scopes)
        exp_dt = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        await self._cache.set(
            f"revoked:{payload['jti']}",
            "1",
            expire=int((exp_dt - datetime.now(timezone.utc)).total_seconds()),
        )
        return TokenDTO(
            access_token=token["access_token"], refresh_token=token["refresh_token"]
        )
