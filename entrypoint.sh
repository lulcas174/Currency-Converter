#!/bin/bash
set -e

echo "🔄 Esperando banco de dados ficar disponível..."

until pg_isready -h db -p 5432; do
  sleep 1
done

echo "✅ Banco disponível, rodando migrations..."
alembic upgrade head

echo "🚀 Subindo aplicação..."
exec uvicorn src.index:app --host 0.0.0.0 --port 8000 --reload
