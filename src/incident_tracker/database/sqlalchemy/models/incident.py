import uuid

from datetime import datetime
from enum import StrEnum

from sqlalchemy import UUID, DateTime, Text, func
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class IncidentStatus(StrEnum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class IncidentSource(StrEnum):
    OPERATOR = "operator"
    MONITORING = "monitoring"
    PARTNER = "partner"


class Incident(BaseModel):
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    status: Mapped[IncidentStatus] = mapped_column(
        SQLAlchemyEnum(IncidentStatus, name="incident_status_enum"),
        default=IncidentStatus.NEW,
        nullable=False,
    )
    source: Mapped[IncidentSource] = mapped_column(
        SQLAlchemyEnum(IncidentSource, name="incident_source_enum"),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        Text(),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
