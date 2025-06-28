import logging

from app.celery_app import celery_app

logger = logging.getLogger(__name__)

import json

from asgiref.sync import async_to_sync

from app.brain_agriculture.schemas.brain_agriculture import ReceiveBrain_AgricultureSchema


async def get_container():
    from app.core.container import Container

    container = Container()
    await container.init_resources()
    return container


async def create_brain_agriculture(brain_agriculture, client_id: int):
    container = await get_container()
    brain_agriculture_service = await container.brain_agriculture_service()
    brain_agriculture = ReceiveBrain_AgricultureSchema.parse_obj(json.loads(brain_agriculture))
    await brain_agriculture_service.insert_brain_agriculture(brain_agriculture, client_id)


@celery_app.task(acks_late=True)
def handle_new_brain_agriculture(brain_agriculture: dict, client_id: int) -> str:
    async_to_sync(create_brain_agriculture)(brain_agriculture, client_id)


@celery_app.task(acks_late=True)
def update_brain_agriculture_status(brain_agriculture: dict) -> str:

    pass


@celery_app.task(acks_late=True)
def update_brain_agriculture_status_in_batch(brain_agriculture: dict) -> str:

    pass
