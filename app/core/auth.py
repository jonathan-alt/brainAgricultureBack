from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from app.accounts.services.client import ClientService
from app.core.container import Container
from app.core.exceptions import UnauthorizedError
from app.core.security import ApiToken


@inject
async def get_current_client(
    credentials: str = Depends(ApiToken()),
    client_service: ClientService = Depends(Provide[Container.client_service]),
) -> None:
    client = await client_service.get_client_by_api_key(credentials.credentials)

    if not client:
        raise UnauthorizedError(detail="Invalid or expired ApiKey.")

    return client
