#!/bin/bash
set -e

# Setup Python backend
cd backend
poetry install
cd ..

# Ensure database and cache are running and apply migrations
docker compose up -d db redis
docker compose run --rm backend poetry run python manage.py migrate

# Setup Node frontend
cd frontend
npm install
cd ..

echo "Bootstrap complete."
