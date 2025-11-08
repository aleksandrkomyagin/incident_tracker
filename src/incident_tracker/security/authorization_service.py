from logging import getLogger

from incident_tracker.interfaces.services import IAuthorizationService
from incident_tracker.security.exceptions import PermissionDeniedException

logger = getLogger(__name__)


class AuthorizationService(IAuthorizationService):
    async def authorize(self, token_payload: dict, required_roles: set[str]) -> None:
        scopes: list[str] = token_payload.get("scopes", [])
        if not required_roles & set(scopes):
            raise PermissionDeniedException(message="Недостаточно прав")
