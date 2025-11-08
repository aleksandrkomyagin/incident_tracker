from functools import lru_cache
from typing import Annotated, AsyncIterable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from incident_tracker.cache.redis import RedisCache, get_redis
from incident_tracker.common.stub import Stub
from incident_tracker.crypto.rsa_key_manager import RSAKeyManager, get_rsa_key_generator
from incident_tracker.database.sqlalchemy.db_helper import (
    create_async_session_factory,
    create_engine,
)
from incident_tracker.database.sqlalchemy.repositories import (
    SQLAlchemyIncidentRepository,
    SQLAlchemyServiceRepository,
)
from incident_tracker.database.sqlalchemy.transaction_manager import (
    SqlalchemyTransactionManager,
)
from incident_tracker.interactors.incident import (
    ChangeIncidentStatusInteractor,
    CreateNewIncidentInteractor,
    ListIncidentInteractor,
)
from incident_tracker.interactors.service import CreateNewServiceInteractor
from incident_tracker.interactors.token import (
    CreateTokenInteractor,
    RefreshTokenInteractor,
    RevokeTokenInteractor,
)
from incident_tracker.interfaces.crypto import IRSAKeyManager
from incident_tracker.interfaces.repositories import (
    IIncidentRepository,
    IServiceRepository,
    ITransactionManager,
)
from incident_tracker.interfaces.services import (
    ICacheService,
    IIncidentService,
    ITokenService,
)
from incident_tracker.security import AuthenticateService, AuthorizationService
from incident_tracker.services import (
    IncidentService,
    TokenService,
)


def new_engine():
    return create_engine()


@lru_cache
def new_async_session_maker(
    engine: Annotated[AsyncEngine, Depends(Stub(AsyncEngine))],
) -> async_sessionmaker[AsyncSession]:
    return create_async_session_factory(engine)


async def new_session(
    session_maker: Annotated[
        async_sessionmaker[AsyncSession],
        Depends(Stub(async_sessionmaker[AsyncSession])),
    ],
) -> AsyncIterable[AsyncSession]:
    async with session_maker() as session:
        yield session


def new_transaction_manager(
    session: Annotated[AsyncSession, Depends(Stub(AsyncSession))],
) -> SqlalchemyTransactionManager:
    return SqlalchemyTransactionManager(session)


def new_incident_repository(
    session: Annotated[AsyncSession, Depends(Stub(AsyncSession))],
) -> SQLAlchemyIncidentRepository:
    return SQLAlchemyIncidentRepository(session)


def new_service_repository(
    session: Annotated[AsyncSession, Depends(Stub(AsyncSession))],
) -> SQLAlchemyServiceRepository:
    return SQLAlchemyServiceRepository(session)


def new_cache_service() -> RedisCache:
    return get_redis()


def new_rsa_key_generator() -> RSAKeyManager:
    return get_rsa_key_generator()


def new_incident_service(
    incident_repository: Annotated[IIncidentRepository, Depends()],
) -> IncidentService:
    return IncidentService(incident_repository)


def new_token_service(
    cache_service: Annotated[ICacheService, Depends()],
    rsa_key_manager: Annotated[IRSAKeyManager, Depends()],
    service_repository: Annotated[IServiceRepository, Depends()],
) -> TokenService:
    return TokenService(cache_service, rsa_key_manager, service_repository)


def new_create_new_service_interactor(
    service_repository: Annotated[IServiceRepository, Depends()],
    tm: Annotated[ITransactionManager, Depends()],
) -> CreateNewServiceInteractor:
    return CreateNewServiceInteractor(service_repository, tm)


def new_create_new_incident_interactor(
    incident_service: Annotated[IIncidentService, Depends()],
    tm: Annotated[ITransactionManager, Depends()],
) -> CreateNewIncidentInteractor:
    return CreateNewIncidentInteractor(incident_service, tm)


def new_change_incident_status_interactor(
    incident_service: Annotated[IIncidentService, Depends()],
    tm: Annotated[ITransactionManager, Depends()],
) -> ChangeIncidentStatusInteractor:
    return ChangeIncidentStatusInteractor(incident_service, tm)


def new_list_incident_interactor(
    incident_service: Annotated[IIncidentService, Depends()],
) -> ListIncidentInteractor:
    return ListIncidentInteractor(incident_service)


def new_create_token_interactor(
    token_service: Annotated[ITokenService, Depends()],
) -> CreateTokenInteractor:
    return CreateTokenInteractor(token_service)


def new_refresh_token_interactor(
    token_service: Annotated[ITokenService, Depends()],
) -> RefreshTokenInteractor:
    return RefreshTokenInteractor(token_service)


def new_revoke_token_interactor(
    token_service: Annotated[ITokenService, Depends()],
) -> RevokeTokenInteractor:
    return RevokeTokenInteractor(token_service)


def new_authentication_provider(
    token_service: Annotated[ITokenService, Depends()],
) -> AuthenticateService:
    return AuthenticateService(token_service)


def new_authorization_provider() -> AuthorizationService:
    return AuthorizationService()
