## Bootstrap backend FastAPI project with Dockerfile

## Owner
backend-agent

## Labels
agent:backend, scope:backend, type:feature

## Context
Phase 3 requires a FastAPI backend application. The apps/backend/ directory currently only has a README.md. This issue creates the project skeleton including dependency management, application entry point, health endpoint, and Dockerfile.

## Scope
- Create apps/backend/pyproject.toml with dependencies: fastapi, uvicorn, pydantic, pydantic-settings, sqlalchemy, aiosqlite, pika, tubedigest-contracts
- Create apps/backend/src/tubedigest/main.py with FastAPI app instance
- Add GET /health endpoint returning a JSON status response
- Create apps/backend/src/tubedigest/settings.py with pydantic-settings for env vars
- Create apps/backend/Dockerfile using python:3.12-slim
- Create apps/backend/.dockerignore

## Out of scope
- SQLAlchemy models or database setup
- RabbitMQ publisher implementation
- Any API routes beyond GET /health
- Worker code or frontend changes

## Acceptance criteria
- uvicorn tubedigest.main:app starts and responds on GET /health
- Settings load from environment variables with defaults from .env.example
- Dockerfile builds without error
- docker compose config shows valid backend service
- pip install -e apps/backend[dev] installs cleanly

## Tests required
- Health endpoint returns 200 with expected status response
- Settings load default values when env vars are absent

## Likely affected files
- apps/backend/pyproject.toml (new)
- apps/backend/src/tubedigest/__init__.py (new)
- apps/backend/src/tubedigest/main.py (new)
- apps/backend/src/tubedigest/settings.py (new)
- apps/backend/Dockerfile (new)
- apps/backend/.dockerignore (new)

## Dependencies
None - contracts package already provides Pydantic schemas.

## Definition of Done
- implementation matches scope
- pytest apps/backend passes
- docker compose config validates
- PR has test evidence
