from logging import getLogger

from incident_tracker.api.v1.schemas.responses import (
    IncidentResponseSchema,
    ListIncidentResponseSchema,
)
from incident_tracker.common.exceptions.base import BaseAppException, BaseInfraException
from incident_tracker.interactors.exceptions import ListIncidentException
from incident_tracker.interfaces.services import IIncidentService

logger = getLogger(__name__)


class ListIncidentInteractor:
    def __init__(
        self,
        incident_service: IIncidentService,
    ):
        self._incident_service = incident_service

    async def __call__(
        self, status: str, page: int, page_size: int
    ) -> ListIncidentResponseSchema:
        logger.info(
            "Новый запрос на получение списка инцидентов, отфильтрованных по статусу %s",
            status,
        )
        try:
            incidents = await self._incident_service.get_incidents_by_status(
                status, page, page_size
            )
        except (BaseAppException, BaseInfraException) as e:
            raise ListIncidentException(
                status_code=e.status_code,
                message="Ошибка получения списка инцидентов",
                detail=str(e.message),
            ) from e

        logger.info(
            "Успешный запрос на получение списка инцидентов, отфильтрованных по статусу: %s",
            status,
        )
        return ListIncidentResponseSchema(
            items=[
                IncidentResponseSchema(
                    id=incident.id,
                    status=incident.status,
                    source=incident.source,
                    description=incident.description,
                    created_at=incident.created_at.strftime("%d.%m.%Y %H:%M:%S"),
                )
                for incident in incidents
            ],
            page=page,
            page_size=page_size,
        )
