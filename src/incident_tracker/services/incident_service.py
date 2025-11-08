from logging import getLogger

from incident_tracker.api.v1.schemas.requests import (
    NewIncidentRequestSchema,
    NewIncidentStatusRequestSchema,
)
from incident_tracker.dto.incident import IncidentDTO
from incident_tracker.interfaces.repositories import IIncidentRepository
from incident_tracker.interfaces.repositories.types import NewIncident
from incident_tracker.interfaces.services import IIncidentService
from incident_tracker.services.exceptions import IncidentNotFoundException

logger = getLogger(__name__)


class IncidentService(IIncidentService):
    def __init__(self, incident_repository: IIncidentRepository) -> None:
        self._incident_repository = incident_repository

    async def new_incident(self, new_incident: NewIncidentRequestSchema) -> IncidentDTO:
        return await self._incident_repository.create_incident(
            NewIncident(
                source=new_incident.source,
                description=new_incident.description,
            )
        )

    async def get_incidents_by_status(
        self, status: str, page: int, page_size: int
    ) -> list[IncidentDTO]:
        return await self._incident_repository.list_incidents_by_status(
            status, page, page_size
        )

    async def change_incident_status(
        self, incident_id: str, new_incident_status: NewIncidentStatusRequestSchema
    ) -> IncidentDTO:
        incident = await self._incident_repository.update_incident_status(
            incident_id, new_incident_status.status
        )
        if not incident:
            raise IncidentNotFoundException(message="Инцидент не найден")
        return incident
