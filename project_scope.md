# Docker Task Tracker — Capstone Project

## Project Goal

Build and containerize a small full-stack Task Tracker application using Docker.

The finished project should demonstrate practical understanding of:

- Docker images and containers
- Dockerfiles
- Image layers and build caching
- Port publishing
- Bind mounts
- Named volumes
- Docker networking
- Docker Compose
- Environment variables
- Container debugging
- Production-oriented Docker practices
- Container registries
- Basic Docker CI/CD

The final developer experience should be:

```bash
git clone <repository>
cd docker-task-tracker
docker compose up --build
```

After that command, the application should be usable without manually starting the frontend, backend, or database.

---

# Architecture

The application will contain three main services:

```text
Browser
   │
   ▼
Frontend
   │
   │ HTTP
   ▼
Backend API
   │
   │ PostgreSQL connection
   ▼
PostgreSQL
   │
   ▼
Persistent Docker Volume
```

### Frontend

Provides the user interface for viewing and managing tasks.

### Backend

Provides a REST API and handles application logic.

### Database

PostgreSQL stores task data persistently.

---

# Suggested Technology Stack

## Frontend

Use a small frontend application.

Suggested:

```text
React
```

The frontend should communicate with the backend through HTTP.

## Backend

Use:

```text
Python
Flask
```

## Database

Use:

```text
PostgreSQL
```

## Infrastructure

Use:

```text
Docker
Docker Compose
GitHub
GitHub Actions
Container Registry
```

---

# Functional Requirements

Users should be able to:

- View tasks
- Create a task
- Mark a task complete
- Delete a task

A task should contain at least:

```text
id
title
completed
```

Optional additions:

```text
description
created_at
due_date
priority
```

Keep the application itself relatively simple. The primary goal of this project is demonstrating Docker skills.

---

# Backend Requirements

The backend must expose a REST API.

Suggested endpoints:

```text
GET    /health
GET    /tasks
POST   /tasks
PATCH  /tasks/<id>
DELETE /tasks/<id>
```

`/health` should return a simple health response.

Example:

```json
{
  "status": "healthy"
}
```

The backend must connect to PostgreSQL using configuration supplied through environment variables.

Database configuration must not be hard-coded into the application.

---

# Frontend Requirements

The frontend should provide a basic interface for interacting with tasks.

At minimum it should:

- Display existing tasks
- Allow creation of a task
- Allow tasks to be marked complete
- Allow tasks to be deleted
- Communicate with the backend API

Visual design is secondary to functionality.

---

# Docker Requirements

## Backend Image

Create a Dockerfile for the Flask backend.

It should demonstrate:

- An appropriate base image
- `WORKDIR`
- Efficient dependency installation
- Cache-friendly `COPY` ordering
- `.dockerignore`
- `EXPOSE`
- An appropriate runtime command

The Dockerfile should avoid reinstalling Python dependencies whenever only application source code changes.

---

## Frontend Image

Create a Dockerfile for the frontend.

The frontend must run inside its own container.

Consider production image size and whether a multi-stage build would be appropriate.

---

# Docker Compose Requirements

Create:

```text
compose.yaml
```

Compose must manage the application services.

At minimum:

```text
frontend
backend
db
```

Running:

```bash
docker compose up --build
```

should start the complete application.

---

# Networking Requirements

Services should communicate using Docker networking.

Containers should not rely on manually discovered container IP addresses.

Use Compose service names for service discovery.

For example, the backend should be able to locate the database through its service name rather than:

```text
localhost
```

Remember:

```text
localhost inside a container
=
that container itself
```

Only ports that need to be accessed from the host should be published.

---

# Database Requirements

Use the official PostgreSQL image.

Database configuration should be supplied through environment variables.

PostgreSQL data must survive container replacement.

Use a named Docker volume for database storage.

Conceptually:

```text
PostgreSQL container
        │
        ▼
Named Volume
        │
        ▼
Persistent Database Data
```

Deleting and recreating the database container should not automatically destroy the application's data.

---

# Environment Configuration

Configuration should be separated from application code.

Use environment variables for values such as:

```text
DATABASE_HOST
DATABASE_PORT
DATABASE_NAME
DATABASE_USER
DATABASE_PASSWORD
```

Provide:

```text
.env.example
```

with example values.

Do not commit real secrets.

The project should ignore the real `.env` file through `.gitignore`.

---

# Development Workflow

The project should support a convenient local development workflow.

Consider using bind mounts where appropriate so source-code changes can be tested without unnecessarily rebuilding images.

Understand the distinction between:

```text
Bind mount
→ development source code

Named volume
→ persistent application/database data
```

---

# Persistence Test

The project should pass the following test:

1. Start the application.
2. Create several tasks.
3. Stop the application.
4. Remove/recreate the containers.
5. Start the application again.
6. Confirm that the tasks still exist.

This demonstrates that database state is stored outside the disposable container.

---

# Networking Test

Verify that:

```text
frontend → backend
backend → database
```

works through Docker networking.

The backend should reach PostgreSQL using its Compose service name.

The application should not depend on hard-coded container IP addresses.

---

# Debugging Requirements

Be comfortable troubleshooting the project using commands such as:

```bash
docker ps
docker ps -a
docker logs <container>
docker exec -it <container> bash
docker inspect <container>

docker compose ps
docker compose logs
docker compose logs -f
docker compose exec <service> bash
```

You should be able to diagnose:

- A container that exits unexpectedly
- Application errors
- Incorrect environment variables
- Incorrect port mappings
- Database connection failures
- Docker networking problems
- Missing files or dependencies

---

# Production Improvements

After the basic application works, improve the containers for production.

Consider:

- Smaller base images
- Non-root container users
- Production application servers
- Dependency/version pinning
- Health checks
- Multi-stage builds
- Minimal image contents
- Runtime configuration
- Proper secret handling

The final production image should contain only what is required to run the application.

---

# Container Registry

Publish at least one application image to a container registry.

Suggested registry:

```text
GitHub Container Registry (GHCR)
```

Use meaningful image tags.

Examples:

```text
v1.0.0
latest
<git-commit-sha>
```

Understand that tags are references and that `latest` does not inherently mean "newest."

---

# CI/CD Requirement

Create a GitHub Actions workflow that automatically builds the Docker image.

Stretch goal:

```text
git push
   │
   ▼
GitHub
   │
   ▼
GitHub Actions
   │
   ├── build image
   ├── run checks/tests
   └── push image
          │
          ▼
        GHCR
```

The workflow should demonstrate that the Docker image can be built consistently outside your local machine.

---

# Documentation Requirements

The repository should contain a polished:

```text
README.md
```

The README should explain:

- What the project does
- Architecture
- Technology stack
- Prerequisites
- How to run the project
- Environment configuration
- Docker architecture
- Services
- Ports
- Volumes
- Useful Docker commands
- How to stop the application
- How to rebuild the application
- Troubleshooting basics

Include an architecture diagram if possible.

---

# Suggested Repository Structure

The finished project may look similar to:

```text
docker-task-tracker/
│
├── frontend/
│   ├── src/
│   ├── Dockerfile
│   └── .dockerignore
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
│
├── .github/
│   └── workflows/
│       └── docker.yml
│
├── compose.yaml
├── .env.example
├── .gitignore
├── PROJECT.md
└── README.md
```

The exact structure may evolve as the project is developed.

---

# Project Milestones

## Milestone 1 — Backend Container

Build the Flask API.

Containerize it with a Dockerfile.

Verify:

```text
Browser
   │
localhost
   │
   ▼
Flask container
```

---

## Milestone 2 — PostgreSQL

Add PostgreSQL.

Connect:

```text
Backend
   │
   ▼
PostgreSQL
```

Use environment variables for database configuration.

---

## Milestone 3 — Docker Compose

Manage the backend and database through Compose.

Verify container-to-container communication using service names.

---

## Milestone 4 — Persistent Storage

Add a named PostgreSQL volume.

Verify that data survives container replacement.

---

## Milestone 5 — Frontend

Build the frontend.

Containerize it separately.

Connect:

```text
Frontend
    ↓
Backend
    ↓
PostgreSQL
```

---

## Milestone 6 — Development Workflow

Add appropriate bind mounts and development configuration.

Make local development convenient without sacrificing understanding of how the production images work.

---

## Milestone 7 — Production Hardening

Improve the Dockerfiles and runtime configuration.

Review:

```text
image size
build caching
non-root users
health checks
production server
secrets
dependency versions
```

---

## Milestone 8 — Registry

Publish the application image to a container registry.

Practice:

```text
docker build
docker tag
docker push
docker pull
```

---

## Milestone 9 — CI/CD

Use GitHub Actions to automatically build the Docker image.

Optionally publish successful builds to the registry.

---

## Milestone 10 — Portfolio Polish

Finish the README.

Include:

- Architecture diagram
- Setup instructions
- Docker concepts demonstrated
- Screenshots
- Example API requests
- Troubleshooting information

Make sure a new developer can clone the repository and successfully run:

```bash
docker compose up --build
```

---

# Definition of Done

The capstone is complete when:

```text
✓ Frontend runs in Docker
✓ Backend runs in Docker
✓ PostgreSQL runs in Docker
✓ Docker Compose manages the application
✓ Containers communicate through Docker networking
✓ PostgreSQL uses persistent storage
✓ Configuration uses environment variables
✓ Secrets are not committed
✓ Dockerfiles use sensible caching strategies
✓ Production improvements are applied
✓ Image can be pushed to a registry
✓ CI builds the Docker image
✓ README documents the architecture and setup
```

Most importantly, you should be able to explain **why** each Docker decision was made rather than only knowing which commands to run.