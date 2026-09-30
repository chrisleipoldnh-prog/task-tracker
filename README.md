# Task Tracker

A small full-stack task app used to show a Docker CI/CD pipeline. GitHub Actions builds the images, tests the backend inside the image that ships, and publishes commit-tagged images to GitHub Container Registry when code lands on `main`.

## CI/CD

Workflow: [`.github/workflows/ci.yml`](.github/workflows/ci.yml)

- **Every change is validated.** The workflow runs on pull requests and pushes to `main`.
- **The shipped image is what gets tested.** Pytest runs inside the built backend container.
- **Publish is gated.** Images are pushed to GHCR only after a push to `main`.
- **Builds are traceable.** Each image is tagged `latest` and with the commit SHA.
- **Registry auth is short-lived.** Login uses `GITHUB_TOKEN` through `docker/login-action`.
- **Permissions stay narrow.** The workflow requests `contents: read` and `packages: write`.

## App

React UI, FastAPI API, PostgreSQL. Create a task, mark it complete, or delete it. Nginx in the frontend image proxies `/api` to the backend over the Compose network.

## Docker

- **Frontend:** multi-stage image. Node compiles the app; nginx serves the static build.
- **Backend:** slim Python image, dependencies installed before application code, process runs as a non-root user.
- **Compose:** health checks control startup order, Postgres data lives in a named volume, and credentials come from `.env`.

## Run locally

```bash
cp .env.example .env
docker compose up --build
```

Open [http://localhost:5173](http://localhost:5173).

After a push to `main`, images are available as `ghcr.io/<owner>/task-tracker-backend` and `ghcr.io/<owner>/task-tracker-frontend`.
