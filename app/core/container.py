from dependency_injector import containers, providers

from app.accounts.repositories.client import ClientRepository
from app.accounts.services.client import ClientService
from app.core.config import config
from app.core.database import get_db
from app.report.repositories.report import ReportRepository
from app.report.services.report import ReportService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["app.report.api.v1.routes", "app.core.auth"])

    db = providers.Resource(get_db, config=config)

    client_repository = providers.Factory(ClientRepository, db=db)
    report_repository = providers.Factory(ReportRepository, db=db)

    client_service = providers.Factory(ClientService, client_repository=client_repository)
    report_service = providers.Factory(ReportService, report_repository=report_repository)

