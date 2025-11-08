from abc import abstractmethod
from typing import Any, Protocol

from incident_tracker.api.v1.schemas.requests import (
    NewIncidentRequestSchema,
    NewIncidentStatusRequestSchema,
)
from incident_tracker.dto.incident import IncidentDTO
from incident_tracker.dto.token import TokenDTO


class IIncidentService(Protocol):
    @abstractmethod
    async def new_incident(self, new_incident: NewIncidentRequestSchema) -> IncidentDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_incidents_by_status(
        self, status: str, page: int, page_size: int
    ) -> list[IncidentDTO]:
        raise NotImplementedError

    @abstractmethod
    async def change_incident_status(
        self, incident_id: str, new_incident_status: NewIncidentStatusRequestSchema
    ) -> IncidentDTO:
        raise NotImplementedError


class ITokenService(Protocol):
    @abstractmethod
    async def create_token(self, service_id: str) -> TokenDTO:
        raise NotImplementedError

    @abstractmethod
    async def decode_token(self, token: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def refresh_token(self, refresh_token: str) -> TokenDTO:
        raise NotImplementedError

    @abstractmethod
    async def revoke_token(self, refresh_token: str) -> None:
        raise NotImplementedError


class IAuthenticateService(Protocol):
    async def authenticate(self, authorization_header: str | None) -> dict[str, Any]:
        raise NotImplementedError


class IAuthorizationService(Protocol):
    async def authorize(self, token_payload: dict, required_roles: set[str]) -> None:
        raise NotImplementedError


class ICacheService(Protocol):
    @abstractmethod
    async def set(self, key: str, value: Any, expire: int | None = None) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, key: str) -> Any | None:
        raise NotImplementedError
