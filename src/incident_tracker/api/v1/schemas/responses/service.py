from pydantic import BaseModel


class ServiceResponseSchema(BaseModel):
    id: str
    name: str
    created_at: str
    scopes: list[str]
