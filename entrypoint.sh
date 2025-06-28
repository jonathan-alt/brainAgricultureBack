#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

echo "🔍 Verificando tabelas existentes no banco de dados..."
python scripts/check_tables.py

echo "📋 Verificando se é necessário criar tabelas..."
python scripts/setup_db.py

export PYTHONPATH=.
exec "$@"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
