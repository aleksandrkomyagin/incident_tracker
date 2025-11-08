from pydantic import BaseModel


class CreateTokenRequestSchema(BaseModel):
    service_id: str


class RefreshTokenRequestSchema(BaseModel):
    refresh_token: str


class RevokeTokenRequestSchema(BaseModel):
    refresh_token: str
