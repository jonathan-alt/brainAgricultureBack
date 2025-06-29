import os
import time
import logging
from typing import List, Optional


from sqlmodel import Session, select

from app.core.repositories import BaseRepository
from app.brain_agriculture.models.brain_agriculture import Fazenda, Produtor, Safra
from app.brain_agriculture.schemas.brain_agriculture import DadosFazenda


ENVIRONMENT = os.environ.get("ENVIRONMENT")
SECRETS = os.environ

logger = logging.getLogger(__name__)


class Brain_AgricultureRepository(BaseRepository):
    def __init__(self, db):
        self.db = db
        super().__init__(db)

    def get_all_fazendas(self) -> List[Fazenda]:
        if self.db is None:
            logger.warning("Banco de dados não disponível, retornando lista vazia")
            return []
        
        with Session(self.db) as session:
            statement = select(Fazenda)
            results = session.exec(statement).all()
            return results

    async def get_teste(self, fazenda: str) -> DadosFazenda:
        # Implementação temporária - você pode ajustar conforme necessário
        logger.info(f"Buscando dados de teste para fazenda: {fazenda}")
        # Aqui você implementaria a lógica real de busca no banco de dados
        return DadosFazenda(fazenda=fazenda)  # Retorna um objeto com a fazenda

    # Métodos CRUD para Produtores
    def get_all_produtores(self) -> List[Produtor]:
        """Busca todos os produtores"""
        if self.db is None:
            logger.warning("Banco de dados não disponível, retornando lista vazia")
            return []
        
        with Session(self.db) as session:
            statement = select(Produtor)
            results = session.exec(statement).all()
            return results

    def get_produtor_by_id(self, produtor_id: int) -> Optional[Produtor]:
        """Busca um produtor pelo ID"""
        if self.db is None:
            logger.warning("Banco de dados não disponível")
            return None
        
        with Session(self.db) as session:
            statement = select(Produtor).where(Produtor.id == produtor_id)
            result = session.exec(statement).first()
            return result

    def get_produtor_by_cpf(self, cpf: str) -> Optional[Produtor]:
        """Busca um produtor pelo CPF"""
        if self.db is None:
            logger.warning("Banco de dados não disponível")
            return None
        
        with Session(self.db) as session:
            statement = select(Produtor).where(Produtor.cpf == cpf)
            result = session.exec(statement).first()
            return result

    def create_produtor(self, produtor: Produtor) -> Produtor:
        """Cria um novo produtor"""
        if self.db is None:
            logger.error("Banco de dados não disponível")
            raise Exception("Banco de dados não disponível")
        
        with Session(self.db) as session:
            session.add(produtor)
            session.commit()
            session.refresh(produtor)
            return produtor

    def update_produtor(self, produtor_id: int, produtor_data: dict) -> Optional[Produtor]:
        """Atualiza um produtor existente"""
        if self.db is None:
            logger.error("Banco de dados não disponível")
            raise Exception("Banco de dados não disponível")
        
        with Session(self.db) as session:
            statement = select(Produtor).where(Produtor.id == produtor_id)
            produtor = session.exec(statement).first()
            
            if not produtor:
                return None
            
            for key, value in produtor_data.items():
                if hasattr(produtor, key):
                    setattr(produtor, key, value)
            
            session.add(produtor)
            session.commit()
            session.refresh(produtor)
            return produtor

    def delete_produtor(self, produtor_id: int) -> bool:
        """Exclui um produtor"""
        if self.db is None:
            logger.error("Banco de dados não disponível")
            raise Exception("Banco de dados não disponível")
        
        with Session(self.db) as session:
            statement = select(Produtor).where(Produtor.id == produtor_id)
            produtor = session.exec(statement).first()
            
            if not produtor:
                return False
            
            session.delete(produtor)
            session.commit()
            return True

    # Métodos CRUD para Fazendas
    def get_fazenda_by_id(self, fazenda_id: int) -> Optional[Fazenda]:
        """Busca uma fazenda pelo ID"""
        if self.db is None:
            logger.warning("Banco de dados não disponível")
            return None
        
        with Session(self.db) as session:
            statement = select(Fazenda).where(Fazenda.id == fazenda_id)
            result = session.exec(statement).first()
            return result

    def get_fazendas_by_produtor(self, produtor_id: int) -> List[Fazenda]:
        """Busca fazendas de um produtor específico"""
        if self.db is None:
            logger.warning("Banco de dados não disponível, retornando lista vazia")
            return []
        
        with Session(self.db) as session:
            statement = select(Fazenda).where(Fazenda.idprodutor == produtor_id)
            results = session.exec(statement).all()
            return results

    def get_fazenda_by_nome_and_produtor(self, nomefazenda: str, produtor_id: int) -> Optional[Fazenda]:
        """Busca uma fazenda pelo nome e produtor"""
        if self.db is None:
            logger.warning("Banco de dados não disponível")
            return None
        
        with Session(self.db) as session:
            statement = select(Fazenda).where(
                Fazenda.nomefazenda == nomefazenda,
                Fazenda.idprodutor == produtor_id
            )
            result = session.exec(statement).first()
            return result

    def create_fazenda(self, fazenda: Fazenda) -> Fazenda:
        """Cria uma nova fazenda"""
        if self.db is None:
            logger.error("Banco de dados não disponível")
            raise Exception("Banco de dados não disponível")
        
        with Session(self.db) as session:
            session.add(fazenda)
            session.commit()
            session.refresh(fazenda)
            return fazenda

    def update_fazenda(self, fazenda_id: int, fazenda_data: dict) -> Optional[Fazenda]:
        """Atualiza uma fazenda existente"""
        if self.db is None:
            logger.error("Banco de dados não disponível")
            raise Exception("Banco de dados não disponível")
        
        with Session(self.db) as session:
            statement = select(Fazenda).where(Fazenda.id == fazenda_id)
            fazenda = session.exec(statement).first()
            
            if not fazenda:
                return None
            
            for key, value in fazenda_data.items():
                if hasattr(fazenda, key):
                    setattr(fazenda, key, value)
            
            session.add(fazenda)
            session.commit()
            session.refresh(fazenda)
            return fazenda

    def delete_fazenda(self, fazenda_id: int) -> bool:
        """Exclui uma fazenda"""
        if self.db is None:
            logger.error("Banco de dados não disponível")
            raise Exception("Banco de dados não disponível")
        
        with Session(self.db) as session:
            statement = select(Fazenda).where(Fazenda.id == fazenda_id)
            fazenda = session.exec(statement).first()
            
            if not fazenda:
                return False
            
            session.delete(fazenda)
            session.commit()
            return True

    # Métodos CRUD para Safras
    def get_all_safras(self) -> List[Safra]:
        """Busca todas as safras"""
        if self.db is None:
            logger.warning("Banco de dados não disponível, retornando lista vazia")
            return []
        
        with Session(self.db) as session:
            statement = select(Safra)
            results = session.exec(statement).all()
            return results

    def get_safra_by_id(self, safra_id: int) -> Optional[Safra]:
        """Busca uma safra pelo ID"""
        if self.db is None:
            logger.warning("Banco de dados não disponível")
            return None
        
        with Session(self.db) as session:
            statement = select(Safra).where(Safra.id == safra_id)
            result = session.exec(statement).first()
            return result

    def get_safras_by_fazenda(self, fazenda_id: int) -> List[Safra]:
        """Busca safras de uma fazenda específica"""
        if self.db is None:
            logger.warning("Banco de dados não disponível, retornando lista vazia")
            return []
        
        with Session(self.db) as session:
            statement = select(Safra).where(Safra.idfazenda == fazenda_id)
            results = session.exec(statement).all()
            return results

    def get_safras_by_ano(self, ano: int) -> List[Safra]:
        """Busca safras por ano"""
        if self.db is None:
            logger.warning("Banco de dados não disponível, retornando lista vazia")
            return []
        
        with Session(self.db) as session:
            statement = select(Safra).where(Safra.ano == ano)
            results = session.exec(statement).all()
            return results

    def create_safra(self, safra: Safra) -> Safra:
        """Cria uma nova safra"""
        if self.db is None:
            logger.error("Banco de dados não disponível")
            raise Exception("Banco de dados não disponível")
        
        with Session(self.db) as session:
            session.add(safra)
            session.commit()
            session.refresh(safra)
            return safra

    def update_safra(self, safra_id: int, safra_data: dict) -> Optional[Safra]:
        """Atualiza uma safra existente"""
        if self.db is None:
            logger.error("Banco de dados não disponível")
            raise Exception("Banco de dados não disponível")
        
        with Session(self.db) as session:
            statement = select(Safra).where(Safra.id == safra_id)
            safra = session.exec(statement).first()
            
            if not safra:
                return None
            
            for key, value in safra_data.items():
                if hasattr(safra, key):
                    setattr(safra, key, value)
            
            session.add(safra)
            session.commit()
            session.refresh(safra)
            return safra

    def delete_safra(self, safra_id: int) -> bool:
        """Exclui uma safra"""
        if self.db is None:
            logger.error("Banco de dados não disponível")
            raise Exception("Banco de dados não disponível")
        
        with Session(self.db) as session:
            statement = select(Safra).where(Safra.id == safra_id)
            safra = session.exec(statement).first()
            
            if not safra:
                return False
            
            session.delete(safra)
            session.commit()
            return True

    def get_fazendas_por_estado(self) -> List[dict]:
        """Busca estatísticas de fazendas por estado"""
        if self.db is None:
            logger.warning("Banco de dados não disponível, retornando lista vazia")
            return []
        
        with Session(self.db) as session:
            from sqlalchemy import func
            
            # Usar SQLAlchemy ORM em vez de query raw
            result = session.exec(
                select(
                    Fazenda.estado,
                    func.count(Fazenda.id).label("quantidade")
                ).group_by(Fazenda.estado).order_by(func.count(Fazenda.id).desc())
            ).all()
            
            return [{"estado": row.estado, "quantidade": row.quantidade} for row in result]

    def get_total_fazendas(self) -> int:
        """Retorna o total de fazendas"""
        if self.db is None:
            logger.warning("Banco de dados não disponível")
            return 0
        
        with Session(self.db) as session:
            from sqlalchemy import func
            result = session.exec(select(func.count(Fazenda.id))).first()
            return result or 0

    def get_total_culturas(self) -> int:
        """Retorna o total de culturas plantadas (total de registros de safras)"""
        if self.db is None:
            logger.warning("Banco de dados não disponível")
            return 0
        
        with Session(self.db) as session:
            from sqlalchemy import func
            result = session.exec(select(func.count(Safra.id))).first()
            return result or 0

    def get_culturas_agrupadas(self) -> list:
        """Retorna o total de cada cultura plantada (agrupado por nome da cultura)"""
        if self.db is None:
            logger.warning("Banco de dados não disponível, retornando lista vazia")
            return []
        
        with Session(self.db) as session:
            from sqlalchemy import func
            statement = select(Safra.cultura, func.count(Safra.id).label("quantidade")).group_by(Safra.cultura).order_by(func.count(Safra.id).desc())
            result = session.exec(statement).all()
            return [{"cultura": row.cultura, "quantidade": row.quantidade} for row in result]

    def get_safras_por_ano(self) -> List[dict]:
        """Retorna o total de safras agrupadas por ano"""
        if self.db is None:
            logger.warning("Banco de dados não disponível, retornando lista vazia")
            return []
        
        with Session(self.db) as session:
            from sqlalchemy import func
            result = session.exec(
                select(
                    Safra.ano,
                    func.count(Safra.id).label("quantidade")
                ).group_by(Safra.ano).order_by(Safra.ano.desc())
            ).all()
            
            return [{"ano": row.ano, "quantidade": row.quantidade} for row in result]

    def get_estatisticas_areas(self) -> dict:
        """Retorna estatísticas de áreas das fazendas (total, agricultável e vegetação)"""
        if self.db is None:
            logger.warning("Banco de dados não disponível")
            return {"area_total": 0, "area_agricultavel": 0, "area_vegetacao": 0}
        
        with Session(self.db) as session:
            from sqlalchemy import func
            # Calcular soma das áreas totais e agricultáveis
            result = session.exec(
                select(
                    func.sum(Fazenda.areatotalfazenda).label("area_total"),
                    func.sum(Fazenda.areaagricutavel).label("area_agricultavel")
                )
            ).first()
            
            area_total = result.area_total or 0
            area_agricultavel = result.area_agricultavel or 0
            area_vegetacao = area_total - area_agricultavel
            
            return {
                "area_total": area_total,
                "area_agricultavel": area_agricultavel,
                "area_vegetacao": area_vegetacao
            }


 