# Task Tracker

A small task tracker being containerized with Docker. The FastAPI backend connects to PostgreSQL and creates a `tasks` table on startup.

## Run it

Requires Docker.

```bash
cp .env.example .env
docker compose up --build
```

The API is published on port **8050**.

- Home: http://localhost:8050/
- Health: http://localhost:8050/health
- Interactive docs: http://localhost:8050/docs

`GET /health` returns the API status and the result of `SELECT 1` against PostgreSQL.

## Layout

```text
backend/app.py       FastAPI app
backend/database.py  SQLAlchemy engine and connection check
backend/model.py     Task table
frontend/            Frontend image (not built yet)
compose.yaml         Backend and PostgreSQL services
```

Copy `.env.example` to `.env` before starting Compose. That file supplies `DB_NAME`, `DB_USER`, and `DB_PASSWORD`. `.env` is gitignored.

## Status

- The backend connects to PostgreSQL with the `DB_*` environment variables. Compose passes `DB_PASSWORD` through to the backend.
- Startup creates the `tasks` table (`id`, `title`, `completed`). Data is stored in the `task-db` volume.
- Task create, update, and delete routes are not wired up yet.
- The frontend Dockerfile is still empty.
