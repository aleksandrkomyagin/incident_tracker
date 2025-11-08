from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

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
    IAuthenticateService,
    IAuthorizationService,
    ICacheService,
    IIncidentService,
    ITokenService,
)
from incident_tracker.setup.di import dependencies

dependency_container = dict()

dependency_container[AsyncEngine] = dependencies.new_engine
dependency_container[
    async_sessionmaker[AsyncSession]
] = dependencies.new_async_session_maker
dependency_container[AsyncSession] = dependencies.new_session
dependency_container[IIncidentRepository] = dependencies.new_incident_repository
dependency_container[IServiceRepository] = dependencies.new_service_repository
dependency_container[ITransactionManager] = dependencies.new_transaction_manager
dependency_container[ICacheService] = dependencies.new_cache_service
dependency_container[IRSAKeyManager] = dependencies.new_rsa_key_generator
dependency_container[IIncidentService] = dependencies.new_incident_service
dependency_container[ITokenService] = dependencies.new_token_service
dependency_container[
    CreateNewServiceInteractor
] = dependencies.new_create_new_service_interactor
dependency_container[
    ChangeIncidentStatusInteractor
] = dependencies.new_change_incident_status_interactor
dependency_container[
    CreateNewIncidentInteractor
] = dependencies.new_create_new_incident_interactor
dependency_container[ListIncidentInteractor] = dependencies.new_list_incident_interactor
dependency_container[CreateTokenInteractor] = dependencies.new_create_token_interactor
dependency_container[RefreshTokenInteractor] = dependencies.new_refresh_token_interactor
dependency_container[RevokeTokenInteractor] = dependencies.new_revoke_token_interactor
dependency_container[IAuthenticateService] = dependencies.new_authentication_provider
dependency_container[IAuthorizationService] = dependencies.new_authorization_provider
