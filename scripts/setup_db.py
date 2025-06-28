import os
import logging
from psycopg2 import connect, OperationalError

ENVIRONMENT = os.environ.get("ENVIRONMENT")
SECRETS = os.environ

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
print(SECRETS)
try:
    logging.info(f"Tentando conectar ao banco com usuário={SECRETS['USER']}, host={SECRETS['HOST']}, database={SECRETS['DATABASE']}")
    with connect(
        user=SECRETS["USER"],
        host=SECRETS["HOST"],
        password=SECRETS["PASSWORD"],
        database=SECRETS['DATABASE']
    ) as conn:
        logging.info("Conexão com o banco de dados estabelecida com sucesso!")
        print(conn)
except OperationalError as e:
    logging.error(f"Erro de conexão com o banco de dados: {e}")
except Exception as e:
    logging.error(f"Erro inesperado: {e}")

        
