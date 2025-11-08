from logging import getLogger

from incident_tracker.api.v1.schemas.requests import NewIncidentStatusRequestSchema
from incident_tracker.api.v1.schemas.responses import IncidentResponseSchema
from incident_tracker.common.exceptions.base import BaseAppException, BaseInfraException
from incident_tracker.interactors.exceptions import ChangeIncidentStatusException
from incident_tracker.interfaces.services import IIncidentService

from ...interfaces.repositories import ITransactionManager

logger = getLogger(__name__)


class ChangeIncidentStatusInteractor:
    def __init__(
        self,
        incident_service: IIncidentService,
        tm: ITransactionManager,
    ):
        self._incident_service = incident_service
        self._tm = tm

    async def __call__(
        self, incident_id: str, request_data: NewIncidentStatusRequestSchema
    ) -> IncidentResponseSchema:
        logger.info("Новый запрос на изменение статуса инцидента")
        try:
            async with self._tm as tm:
                incident = await self._incident_service.change_incident_status(
                    incident_id, request_data
                )
                await tm.commit()
        except (BaseAppException, BaseInfraException) as e:
            raise ChangeIncidentStatusException(
                status_code=e.status_code,
                message="Ошибка изменения статуса инцидента",
                detail=str(e.message),
            ) from e

        logger.info(
            "Успешный запрос на изменение статуса инцидента. IncidentId: %s",
            incident.id,
        )
        return IncidentResponseSchema(
            id=incident.id,
            status=incident.status,
            source=incident.source,
            description=incident.description,
            created_at=incident.created_at.strftime("%d.%m.%Y %H:%M:%S"),
        )
