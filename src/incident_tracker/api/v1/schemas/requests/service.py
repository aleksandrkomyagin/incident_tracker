from enum import StrEnum

from pydantic import BaseModel


class Scope(StrEnum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"


class NewServiceRequestSchema(BaseModel):
    name: str
    scopes: list[Scope]
