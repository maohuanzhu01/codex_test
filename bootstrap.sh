#!/bin/bash
set -e

# Setup Python backend
cd backend
poetry install
poetry run python manage.py migrate
cd ..

# Setup Node frontend
cd frontend
npm install
cd ..

echo "Bootstrap complete."
