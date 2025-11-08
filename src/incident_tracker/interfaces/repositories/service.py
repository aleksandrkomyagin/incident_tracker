from abc import abstractmethod
from typing import Protocol

from incident_tracker.dto.service import NewServiceDTO, ServiceDTO


class IServiceRepository(Protocol):
    @abstractmethod
    async def create_service(self, service: NewServiceDTO) -> ServiceDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_service_by_id(self, service_id: str) -> ServiceDTO | None:
        raise NotImplementedError
