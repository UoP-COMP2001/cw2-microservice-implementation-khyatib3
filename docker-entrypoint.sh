#!/bin/bash
set -e

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}

echo "Starting ProfileService API on ${HOST}:${PORT}..."
echo "Swagger UI will be available at http://localhost:${PORT}/profileservice-api/ui/"

exec uvicorn app:connex_app --host "${HOST}" --port "${PORT}" --no-access-log
