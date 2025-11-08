from logging import getLogger

from incident_tracker.api.v1.schemas.requests import NewServiceRequestSchema
from incident_tracker.api.v1.schemas.responses import ServiceResponseSchema
from incident_tracker.common.exceptions.base import BaseAppException, BaseInfraException
from incident_tracker.dto.service import NewServiceDTO
from incident_tracker.interfaces.repositories import (
    IServiceRepository,
    ITransactionManager,
)

from ..exceptions import NewServiceException

logger = getLogger(__name__)


class CreateNewServiceInteractor:
    def __init__(
        self,
        service_repository: IServiceRepository,
        tm: ITransactionManager,
    ):
        self._service_repository = service_repository
        self._tm = tm

    async def __call__(
        self, request_data: NewServiceRequestSchema
    ) -> ServiceResponseSchema:
        logger.info("Новый запрос на добавление нового сервиса")
        try:
            async with self._tm as tm:
                service = await self._service_repository.create_service(
                    NewServiceDTO(
                        name=request_data.name,
                        scopes=[scope.value for scope in request_data.scopes],
                    )
                )
                await tm.commit()
        except (BaseAppException, BaseInfraException) as e:
            raise NewServiceException(
                status_code=e.status_code,
                message="Ошибка добавления нового сервиса",
                detail=str(e.message),
            ) from e

        logger.info(
            "Успешный запрос на добавление нового сервиса. ServiceId: %s", service.id
        )
        return ServiceResponseSchema(
            id=service.id,
            name=service.name,
            created_at=service.created_at.strftime("%d.%m.%Y %H:%M:%S"),
            scopes=service.scopes,
        )
