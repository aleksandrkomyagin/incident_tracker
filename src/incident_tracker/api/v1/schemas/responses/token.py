from dataclasses import dataclass

from ..validator import ValidatedDataClass


@dataclass
class BaseMessageResponse(ValidatedDataClass):
    message: str


@dataclass
class BaseTokenResponseSchema(ValidatedDataClass):
    access_token: str
    refresh_token: str


class CreateTokenResponseSchema(BaseTokenResponseSchema):
    pass


class RefreshTokenResponseSchema(BaseTokenResponseSchema):
    pass


class RevokeTokenResponseSchema(BaseMessageResponse):
    pass
