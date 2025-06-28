import logging

import asyncpg

from app.core.config import Config

logger = logging.getLogger()

async def get_db(config: Config):
    pool = await asyncpg.create_pool(
        user=config.SENSOR_DB_USER,
        password=config.SENSOR_DB_PASSWORD,
        database=config.SENSOR_DB_DATABASE,
        host=config.SENSOR_DB_HOST,
        port=config.SENSOR_DB_PORT,
        min_size=5,
        max_size=10,
    )

    yield pool
    await pool.close()
