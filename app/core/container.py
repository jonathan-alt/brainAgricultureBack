from dependency_injector import containers, providers



from app.core.config import config
from app.core.database import get_db
from app.brain_agriculture.repositories.brain_agriculture import Brain_AgricultureRepository
from app.brain_agriculture.services.brain_agriculture import Brain_AgricultureService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["app.brain_agriculture.api.v1.routes"])

    db = providers.Resource(get_db, config=config)


    brain_agriculture_repository = providers.Factory(Brain_AgricultureRepository, db=db)


    brain_agriculture_service = providers.Factory(Brain_AgricultureService, brain_agriculture_repository=brain_agriculture_repository)

