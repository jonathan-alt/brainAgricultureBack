import datetime as dt
import logging
import time
import uuid
from typing import Dict, Optional

from app.core.services import BaseService
from app.brain_agriculture.repositories.brain_agriculture import Brain_AgricultureRepository
from app.brain_agriculture.schemas.brain_agriculture import (
    FinalMovement,
    QuantifyMovement,
    ReturnSucess,
    Brain_Agriculture,
    StepsAnalyticalView,
    consolidatedBrain_AgricultureMovement,
    Movement,
)

logger = logging.getLogger(__name__)


class Brain_AgricultureService(BaseService):
    def __init__(self, brain_agriculture_repository: Brain_AgricultureRepository):
        self.brain_agriculture_repository = brain_agriculture_repository
        super().__init__(brain_agriculture_repository)

    async def get_teste(self, fazenda: str) -> StepsAnalyticalView:
        return await self.brain_agriculture_repository.get_teste(fazenda)

    
