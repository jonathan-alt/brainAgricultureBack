import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from app.core.config import Config

logger = logging.getLogger()

def get_db(config: Config):
    try:
        logger.info("Iniciando conexão com o banco de dados...")
        
        # Configuração SSL baseada no ambiente
        ssl_mode = 'require' if config.ENVIRONMENT != 'test' else 'disable'
        logger.info(f"Modo SSL configurado: {ssl_mode}")
        
        # Criar URL de conexão PostgreSQL usando psycopg2
        database_url = f"postgresql://{config.AGRICULTURE_DB_USER}:{config.AGRICULTURE_DB_PASSWORD}@{config.AGRICULTURE_DB_HOST}:{config.AGRICULTURE_DB_PORT}/{config.AGRICULTURE_DB_DATABASE}"
        logger.info(f"URL de conexão: postgresql://{config.AGRICULTURE_DB_USER}:***@{config.AGRICULTURE_DB_HOST}:{config.AGRICULTURE_DB_PORT}/{config.AGRICULTURE_DB_DATABASE}")
        
        # Configurar parâmetros SSL
        connect_args = {}
        if ssl_mode == 'require':
            connect_args['sslmode'] = 'require'
        
        logger.info("Criando engine do SQLAlchemy...")
        
        # Criar engine do SQLAlchemy
        engine = create_engine(
            database_url,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            pool_recycle=3600,
            connect_args=connect_args,
            echo=False  # Set to True for SQL debugging
        )
        
        logger.info("Engine do SQLAlchemy criado com sucesso")
        
        # Criar session factory
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        yield engine
        logger.info("Fechando conexão com o banco de dados...")
        engine.dispose()
    except Exception as e:
        logger.error(f"Erro ao conectar com o banco de dados: {e}")
        logger.warning("Aplicação funcionando sem banco de dados")
        yield None
