#!/bin/sh

set -e

echo "=== INICIANDO JANJIA BOOTSTRAP ==="

# Aguarda dependências (Postgres, Redis, Ollama) e garante o modelo qwen3:8b
python /app/scripts/bootstrap.py

echo "=== EXECUTANDO MIGRAÇÕES DO BANCO DE DADOS ==="
alembic upgrade head

echo "=== INICIANDO API FASTAPI ==="
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
