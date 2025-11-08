from logging import getLogger

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from incident_tracker.database.sqlalchemy.decorators import db_operation
from incident_tracker.database.sqlalchemy.models import Incident, Service
from incident_tracker.dto.incident import IncidentDTO
from incident_tracker.dto.service import NewServiceDTO, ServiceDTO
from incident_tracker.interfaces.repositories import (
    IIncidentRepository,
    IServiceRepository,
)
from incident_tracker.interfaces.repositories.types import NewIncident

logger = getLogger(__name__)


class SQLAlchemyIncidentRepository(IIncidentRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @db_operation
    async def create_incident(self, new_incident: NewIncident) -> IncidentDTO:
        stmt = insert(Incident).values(**new_incident).returning(Incident)
        result = await self.session.execute(stmt)
        incident = result.scalar_one()

        return IncidentDTO(
            id=str(incident.id),
            status=incident.status,
            source=incident.source,
            description=incident.description,
            created_at=incident.created_at,
        )

    @db_operation
    async def get_incident_by_id(self, incident_id: str) -> IncidentDTO | None:
        stmt = select(Incident).where(Incident.id == incident_id)
        result = await self.session.execute(stmt)
        incident = result.scalar_one_or_none()
        if not incident:
            return None

        return IncidentDTO(
            id=str(incident.id),
            status=incident.status,
            source=incident.source,
            description=incident.description,
            created_at=incident.created_at,
        )

    @db_operation
    async def list_incidents_by_status(
        self, status: str, page: int, page_size: int
    ) -> list[IncidentDTO]:
        stmt = select(Incident)
        if status:
            stmt = stmt.where(Incident.status == status)
        stmt = (
            stmt.offset((page - 1) * page_size)
            .limit(page_size)
            .order_by(Incident.created_at)
        )
        result = await self.session.execute(stmt)
        incidents = result.scalars().all()

        return [
            IncidentDTO(
                id=str(incident.id),
                status=incident.status,
                source=incident.source,
                description=incident.description,
                created_at=incident.created_at,
            )
            for incident in incidents
        ]

    @db_operation
    async def update_incident_status(
        self, incident_id: str, new_incident_status: str
    ) -> IncidentDTO | None:
        stmt = (
            update(Incident)
            .values({"status": new_incident_status})
            .where(Incident.id == incident_id)
            .returning(Incident)
        )
        result = await self.session.execute(stmt)
        incident = result.scalar_one_or_none()
        if not incident:
            return None
        return IncidentDTO(
            id=str(incident.id),
            status=incident.status,
            source=incident.source,
            description=incident.description,
            created_at=incident.created_at,
        )


class SQLAlchemyServiceRepository(IServiceRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @db_operation
    async def create_service(self, new_service: NewServiceDTO) -> ServiceDTO:
        stmt = (
            insert(Service)
            .values({"name": new_service.name, "scopes": new_service.scopes})
            .returning(Service)
        )
        result = await self.session.execute(stmt)
        service = result.scalar_one()

        return ServiceDTO(
            id=str(service.id),
            name=service.name,
            created_at=service.created_at,
            scopes=[str(scope.value).lower() for scope in service.scopes],
        )

    @db_operation
    async def get_service_by_id(self, service_id: str) -> ServiceDTO | None:
        stmt = select(Service).where(Service.id == service_id)
        result = await self.session.execute(stmt)
        service = result.scalar_one_or_none()
        if not service:
            return None

        return ServiceDTO(
            id=str(service.id),
            name=service.name,
            created_at=service.created_at,
            scopes=[str(scope.value).lower() for scope in service.scopes],
        )
