import asyncio
import logging
from sqlmodel import SQLModel, create_engine
from app.core.config import config
from app.brain_agriculture.models.brain_agriculture import Produtor, Fazenda, Safra

logger = logging.getLogger(__name__)

async def setup_database():
    """Configura o banco de dados criando as tabelas necessárias"""
    try:
        # Criar string de conexão
        database_url = f"postgresql://{config.AGRICULTURE_DB_USER}:{config.AGRICULTURE_DB_PASSWORD}@{config.AGRICULTURE_DB_HOST}:{config.AGRICULTURE_DB_PORT}/{config.AGRICULTURE_DB_DATABASE}"
        
        # Criar engine
        engine = create_engine(database_url, echo=True)
        
        # Criar todas as tabelas
        SQLModel.metadata.create_all(engine)
        
        logger.info("Tabelas criadas com sucesso!")
        
        # Fechar conexão
        engine.dispose()
        
    except Exception as e:
        logger.error(f"Erro ao configurar banco de dados: {e}")
        raise e

if __name__ == "__main__":
    asyncio.run(setup_database())

        
