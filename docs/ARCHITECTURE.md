# Architecture

This document follows the C4 model.

## Context

TODO: high level diagram.

## Container

- **Frontend**: Vite SPA served by Nginx.
- **Backend**: Django + DRF API.
- **Database**: Postgres with pgvector extension.
- **Redis**: message broker and cache.
