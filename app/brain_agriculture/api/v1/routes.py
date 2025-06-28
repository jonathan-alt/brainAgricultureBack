import logging
import time
from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request

from app.core.container import Container
from app.brain_agriculture.models.brain_agriculture import ReturnSucess
from app.brain_agriculture.schemas.brain_agriculture import Brain_Agriculture
from app.brain_agriculture.services.brain_agriculture import Brain_AgricultureService

logger = logging.getLogger(__name__)

brain_agriculture_router = r = APIRouter()


@r.post("/brain_agricultures/receive/", response_model=ReturnSucess)
@inject
async def receive_brain_agriculture(
    request: Request,
    brain_agricultures: Brain_Agriculture,
    brain_agriculture_service: Brain_AgricultureService = Depends(Provide[Container.brain_agriculture_service]),
):
    try:
       
        response = await brain_agriculture_service.add_steps(brain_agricultures)

        return response
    except Exception as e:
        return f"Erro ao tratar dados ou coletar no banco: {e}"




