#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

python scripts/setup_db.py
export PYTHONPATH=.
exec "$@"
