from abc import abstractmethod
from typing import Protocol

from incident_tracker.dto.incident import IncidentDTO
from incident_tracker.interfaces.repositories.types import NewIncident


class IIncidentRepository(Protocol):
    @abstractmethod
    async def create_incident(self, new_incident: NewIncident) -> IncidentDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_incident_by_id(self, user_id: str) -> IncidentDTO | None:
        raise NotImplementedError

    @abstractmethod
    async def list_incidents_by_status(
        self, status: str, page: int, page_size: int
    ) -> list[IncidentDTO]:
        raise NotImplementedError

    @abstractmethod
    async def update_incident_status(
        self, incident_id: str, new_incident_status: str
    ) -> IncidentDTO | None:
        raise NotImplementedError
