import os
import sys
import logging
import asyncpg
from app.core.config import config

# Adicionar o diretório raiz ao PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = logging.getLogger(__name__)

async def check_existing_tables():
    """Verifica quais tabelas já existem no banco de dados"""
    try:
        # Conectar ao banco
        conn = await asyncpg.connect(
            user=config.AGRICULTURE_DB_USER,
            password=config.AGRICULTURE_DB_PASSWORD,
            database=config.AGRICULTURE_DB_DATABASE,
            host=config.AGRICULTURE_DB_HOST,
            port=config.AGRICULTURE_DB_PORT,
        )
        
        logger.info("Conectado ao banco de dados!")
        
        # Verificar tabelas existentes
        tables_query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE'
        ORDER BY table_name;
        """
        
        tables = await conn.fetch(tables_query)
        
        logger.info("Tabelas existentes no banco:")
        for table in tables:
            logger.info(f"  - {table['table_name']}")
        
        # Verificar se nossas tabelas principais existem
        expected_tables = ['produtor', 'fazenda', 'safra']
        existing_table_names = [table['table_name'] for table in tables]
        
        logger.info("\nVerificação das tabelas necessárias:")
        for table in expected_tables:
            if table in existing_table_names:
                logger.info(f"  {table} - EXISTE")
            else:
                logger.info(f"  {table} - NÃO EXISTE")
        
        await conn.close()
        
    except Exception as e:
        logger.error(f"Erro ao verificar tabelas: {e}")
        raise e

if __name__ == "__main__":
    import asyncio
    asyncio.run(check_existing_tables()) 