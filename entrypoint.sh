#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

# Configurar PYTHONPATH
export PYTHONPATH=.

# Obter porta do ambiente ou usar 8000 como padrão
PORT=${PORT:-8000}

echo "Verificando tabelas existentes no banco de dados..."
python scripts/check_tables.py

echo "Verificando se é necessário criar tabelas..."
python scripts/setup_db.py

echo "verificando porta $PORT"

uvicorn app.main:app --host 0.0.0.0 --port $PORT
