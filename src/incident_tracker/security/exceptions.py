from incident_tracker.common.exceptions.base import (
    BaseAuthException,
    BasePermissionException,
)


class TokenRequiredException(BaseAuthException):
    pass


class BearerSchemaRequiredException(BaseAuthException):
    pass


class InvalidTokenException(BaseAuthException):
    pass


class TokenExpiredException(BaseAuthException):
    pass


class PermissionDeniedException(BasePermissionException):
    status_code = 403
