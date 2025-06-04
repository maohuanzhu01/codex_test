# Legal AI

This repository contains a Django backend and a Vite frontend.

## Local setup


```bash
./bootstrap.sh
# then
docker compose up --build
```

This will start the backend, frontend, and the Celery worker for background tasks.

The backend OpenAPI schema is available at `/schema/` and Swagger UI at `/docs/`.
