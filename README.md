# Legal AI

This repository contains a Django backend and a Vite frontend.

## Prerequisites

Install the following tools:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Poetry](https://python-poetry.org/)
- [Node.js and npm](https://nodejs.org/)

## Local setup


This will start the backend, frontend, and the Celery worker for background tasks.

The backend OpenAPI schema is available at `/schema/` and Swagger UI at `/docs/`.

### Default admin user

After running the migrations you can create a default superuser named `admin`
with password `12345678`:

```bash
docker compose run --rm backend poetry run python manage.py create_default_admin
```
