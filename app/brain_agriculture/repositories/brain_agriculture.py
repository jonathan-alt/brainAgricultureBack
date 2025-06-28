import os
import time
from typing import List
from venv import logger

from clickhouse_driver import Client # type: ignore
from sqlmodel import Session, select

from app.core.repositories import BaseRepository
from app.brain_agriculture.models.brain_agriculture import  Movement, Fazenda
from app.brain_agriculture.schemas.brain_agriculture import consolidatedbrain_agricultureMovement

ENVIRONMENT = os.environ.get("ENVIRONMENT")
SECRETS = os.environ



class brain_agricultureRepository(BaseRepository):
    def __init__(self, db):
        self.db = db
        super().__init__(db)

    def get_all_fazendas(self) -> List[Fazenda]:
        with Session(self.db) as session:
            statement = select(Fazenda)
            results = session.exec(statement).all()
            return results


 