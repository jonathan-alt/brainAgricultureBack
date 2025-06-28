import logging
import asyncpg
from app.core.config import config

logger = logging.getLogger(__name__)

async def test_database_connection():
    """Testa a conexão com o banco de dados"""
    try:
        # Tentar conectar ao banco
        conn = await asyncpg.connect(
            user=config.AGRICULTURE_DB_USER,
            password=config.AGRICULTURE_DB_PASSWORD,
            database=config.AGRICULTURE_DB_DATABASE,
            host=config.AGRICULTURE_DB_HOST,
            port=config.AGRICULTURE_DB_PORT,
        )
        
        logger.info("Conexão com banco de dados estabelecida com sucesso!")
        
        # Testar uma query simples
        result = await conn.fetchval('SELECT 1')
        logger.info(f"Query de teste executada: {result}")
        
        await conn.close()
        
    except Exception as e:
        logger.error(f"Erro ao conectar com banco de dados: {e}")
        raise e

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_database_connection()) 