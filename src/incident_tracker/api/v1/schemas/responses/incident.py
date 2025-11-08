from pydantic import BaseModel


class IncidentResponseSchema(BaseModel):
    id: str
    status: str
    source: str
    description: str
    created_at: str


class ListIncidentResponseSchema(BaseModel):
    items: list[IncidentResponseSchema]
    page: int
    page_size: int
