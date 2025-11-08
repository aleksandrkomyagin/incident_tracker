import uuid

from datetime import datetime
from enum import StrEnum

from sqlalchemy import ARRAY, UUID, DateTime, String, func
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Scope(StrEnum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"


class Service(BaseModel):
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    scopes: Mapped[list[Scope]] = mapped_column(
        ARRAY(SQLAlchemyEnum(Scope, name="scope_enum")),
        nullable=False,
    )
