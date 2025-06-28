import os
import sys
import asyncio
import logging

# Adicionar o diretório raiz ao PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncpg
from app.core.config import config

logger = logging.getLogger(__name__)

async def setup_database():
    """Configura o banco de dados criando as tabelas necessárias usando asyncpg"""
    try:
        # Conectar ao banco usando asyncpg
        conn = await asyncpg.connect(
            user=config.AGRICULTURE_DB_USER,
            password=config.AGRICULTURE_DB_PASSWORD,
            database=config.AGRICULTURE_DB_DATABASE,
            host=config.AGRICULTURE_DB_HOST,
            port=config.AGRICULTURE_DB_PORT,
            ssl='require'
        )
        
        try:
            # Criar tabela de produtores
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS produtor (
                    id SERIAL PRIMARY KEY,
                    cpf VARCHAR(20) UNIQUE NOT NULL,
                    nomeprodutor VARCHAR(100) NOT NULL
                )
            """)
            
            # Criar tabela de fazendas
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS fazenda (
                    id SERIAL PRIMARY KEY,
                    nomefazenda VARCHAR(100) NOT NULL,
                    cidade VARCHAR(100) NOT NULL,
                    estado VARCHAR(100) NOT NULL,
                    areatotalfazenda FLOAT NOT NULL,
                    areaagricutavel FLOAT NOT NULL,
                    idprodutor INTEGER REFERENCES produtor(id)
                )
            """)
            
            # Criar tabela de safras
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS safra (
                    id SERIAL PRIMARY KEY,
                    ano INTEGER NOT NULL,
                    cultura VARCHAR(100) NOT NULL,
                    idfazenda INTEGER REFERENCES fazenda(id)
                )
            """)
            
            logger.info("Tabelas criadas com sucesso!")
            
        finally:
            await conn.close()
        
    except Exception as e:
        logger.error(f"Erro ao configurar banco de dados: {e}")
        raise e

if __name__ == "__main__":
    asyncio.run(setup_database())

        
