from incident_tracker.common.exceptions.base import (
    BaseAppException,
    BaseAuthException,
    BaseDetailException,
)


class ServiceNotFoundException(BaseAppException):
    status_code: int = 404


class IncidentNotFoundException(BaseAppException):
    status_code: int = 404


class TokenExpiredException(BaseAuthException):
    pass


class InvalidTokenException(BaseAuthException):
    pass


class TokenIsRevokedException(BaseAuthException):
    pass


class InvalidTokenJTIException(BaseAuthException):
    pass


class InvalidTokenTypeException(BaseAuthException):
    pass


class InvalidTokenIssuerException(BaseAuthException):
    pass


class MakeTokenException(BaseAppException):
    status_code: int = 503


class RSAKeyNotFoundException(BaseAppException):
    status_code: int = 503


class TokenRevocationException(BaseDetailException):
    pass


class TokenRefreshException(BaseDetailException):
    pass


class TokenCreationException(BaseDetailException):
    pass
