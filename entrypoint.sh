#!/bin/sh

set -o errexit
set -o pipefail
set -o nounset

echo "Running migrations..."
alembic -c incident_tracker/setup/alembic.ini upgrade head
echo "Migrations successful"

echo "Running server..."
python incident_tracker/main.py
