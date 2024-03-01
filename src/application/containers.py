from dependency_injector import containers, providers

from application.config import Settings
from application.database import Database
from application.repositories import EventRepository, UserRepository
from application.services import EventService, UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["application.routers.user_router"])

    config = providers.Configuration()

    db = providers.Singleton(
        Database,
        db_url=config.postgres.url,
    )

    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session,
    )

    event_repository = providers.Factory(
        EventRepository,
        session_factory=db.provided.session,
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )

    event_service = providers.Factory(
        EventService,
        event_repository=event_repository
    )



def create_container() -> Container:
    container = Container()
    settings = Settings()
    container.config.from_dict(settings.model_dump())

    return container
