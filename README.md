# Legal AI

This repository contains a Django backend and a Vite frontend.

## Prerequisites

Install the following tools:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Poetry](https://python-poetry.org/)
- [Node.js and npm](https://nodejs.org/)

## Local setup

1. Copy `backend/.env.example` to `backend/.env` and edit values such as
   `DJANGO_SECRET_KEY`.
2. Start PostgreSQL (for example with `docker compose up -d db`) or use your
   local installation.
3. Run the bootstrap script to install dependencies and apply migrations:

   ```bash
   ./bootstrap.sh
   ```
4. Finally, launch all services:

   ```bash
   docker compose up --build
   ```

The backend OpenAPI schema is available at `/schema/` and Swagger UI at `/docs/`.
