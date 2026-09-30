# Task Tracker

A small task tracker run with Docker Compose. The React frontend talks to a FastAPI backend, and tasks are stored in PostgreSQL.

## Run it

Requires Docker.

```bash
git clone https://github.com/chrisleipoldnh-prog/task-tracker.git
cd task-tracker
cp .env.example .env
docker compose up --build
```

- App: http://localhost:5173
- API: http://localhost:8050
- Interactive docs: http://localhost:8050/docs

Copy `.env.example` to `.env` before starting Compose. That file supplies `DB_NAME`, `DB_USER`, and `DB_PASSWORD`. `.env` is gitignored.

From the app you can add a task, mark it complete or incomplete, and delete it. Tasks stay in the `task-db` volume across container restarts.

## API

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/health` | API status and a `SELECT 1` database check |
| `GET` | `/tasks` | List tasks |
| `GET` | `/tasks/{id}` | Get one task |
| `POST` | `/tasks` | Create a task. Body: `{"title": "Buy milk"}` |
| `PATCH` | `/tasks/{id}` | Update `title` and/or `completed` |
| `DELETE` | `/tasks/{id}` | Delete a task |

A task looks like:

```json
{
  "id": 1,
  "title": "Buy milk",
  "completed": false
}
```

An unknown id returns **404**. The backend allows browser requests from `http://localhost:5173`.

## Layout

```text
frontend/            React app (Vite) and its Dockerfile
backend/app.py       FastAPI routes
backend/database.py  SQLAlchemy engine and session
backend/models.py    Task table
backend/schemas.py   Request bodies
compose.yaml         Frontend, backend, and PostgreSQL
```

Startup creates the `tasks` table if it does not exist. The table has `id`, `title`, and `completed`.
