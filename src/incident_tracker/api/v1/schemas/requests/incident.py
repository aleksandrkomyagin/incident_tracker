from enum import StrEnum

from pydantic import BaseModel


class IncidentSource(StrEnum):
    OPERATOR = "operator"
    MONITORING = "monitoring"
    PARTNER = "partner"


class IncidentStatus(StrEnum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class NewIncidentRequestSchema(BaseModel):
    source: IncidentSource
    description: str


class NewIncidentStatusRequestSchema(BaseModel):
    status: IncidentStatus
