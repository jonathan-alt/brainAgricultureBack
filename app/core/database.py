import logging

import asyncpg

from app.core.config import Config

logger = logging.getLogger()

async def get_db(config: Config):
    try:
        pool = await asyncpg.create_pool(
            user=config.AGRICULTURE_DB_USER,
            password=config.AGRICULTURE_DB_PASSWORD,
            database=config.AGRICULTURE_DB_DATABASE,
            host=config.AGRICULTURE_DB_HOST,
            port=config.AGRICULTURE_DB_PORT,
            min_size=1,
            max_size=5,
            ssl='require',
            command_timeout=60,
            server_settings={
                'application_name': 'brain_agriculture_app'
            }
        )
        yield pool
        await pool.close()
    except Exception as e:
        logger.warning(f"Não foi possível conectar ao banco de dados: {e}")
        logger.warning("Aplicação funcionando sem banco de dados")
        yield None
