#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

# Configurar PYTHONPATH
export PYTHONPATH=.

echo "Verificando tabelas existentes no banco de dados..."
python scripts/check_tables.py

echo "Verificando se é necessário criar tabelas..."
python scripts/setup_db.py

#echo "Limpando as tabelas..."
#python scripts/clear_data.py

#echo "Populando banco com dados mockados..."
#python scripts/seed_data.py

exec "$@"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
