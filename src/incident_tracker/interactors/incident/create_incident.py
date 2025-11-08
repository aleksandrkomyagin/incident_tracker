from logging import getLogger

from incident_tracker.api.v1.schemas.requests import NewIncidentRequestSchema
from incident_tracker.api.v1.schemas.responses import IncidentResponseSchema
from incident_tracker.common.exceptions.base import BaseAppException, BaseInfraException
from incident_tracker.interfaces.repositories import ITransactionManager
from incident_tracker.interfaces.services import IIncidentService

from ..exceptions import NewIncidentException

logger = getLogger(__name__)


class CreateNewIncidentInteractor:
    def __init__(
        self,
        incident_service: IIncidentService,
        tm: ITransactionManager,
    ):
        self._incident_service = incident_service
        self._tm = tm

    async def __call__(
        self, request_data: NewIncidentRequestSchema
    ) -> IncidentResponseSchema:
        logger.info("Новый запрос на добавление нового инцидента")
        try:
            async with self._tm as tm:
                incident = await self._incident_service.new_incident(request_data)
                await tm.commit()
        except (BaseAppException, BaseInfraException) as e:
            raise NewIncidentException(
                status_code=e.status_code,
                message="Ошибка добавления нового инцидента",
                detail=str(e.message),
            ) from e

        logger.info(
            "Успешный запрос на добавление нового инцидента. IncidentId: %s",
            incident.id,
        )
        return IncidentResponseSchema(
            id=incident.id,
            status=incident.status,
            source=incident.source,
            description=incident.description,
            created_at=incident.created_at.strftime("%d.%m.%Y %H:%M:%S"),
        )
