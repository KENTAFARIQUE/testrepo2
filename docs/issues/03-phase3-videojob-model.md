## Add SQLAlchemy VideoJob model and database setup

## Owner
backend-agent

## Labels
agent:backend, scope:backend, type:feature

## Context
The backend needs to persist video processing jobs in SQLite. This issue creates the SQLAlchemy VideoJob ORM model, database engine/session management, and a repository layer for CRUD operations.

## Scope
- Create apps/backend/src/tubedigest/database.py with async SQLite engine, session, get_db dependency
- Create apps/backend/src/tubedigest/models.py with SQLAlchemy VideoJob table:
  - id (UUID, primary key), url (required), title (nullable)
  - status (default queued), current_step (default queued)
  - video_path, audio_path, thumbnail_path (nullable)
  - transcript, summary (nullable text)
  - tags, chapters (nullable JSON)
  - error (nullable text)
  - created_at, updated_at (datetime)
- Create apps/backend/src/tubedigest/repository.py with create_job, get_job, list_jobs, update_job
- Tests using temporary SQLite DB for all CRUD operations

## Out of scope
- API endpoints (POST/GET) - separate issues
- RabbitMQ publishing
- Data migration scripts

## Acceptance criteria
- create_job inserts a row with correct defaults (status=queued)
- get_job returns the correct job by UUID
- get_job returns None for missing ID
- list_jobs returns all jobs ordered by created_at desc
- update_job modifies specified fields and updates updated_at
- All CRUD operations work with async SQLite session
- create_all creates the schema from the model

## Tests required
- Create job: verify id, url, status defaults
- Get job: fetch by id returns correct job
- Get job: missing id returns None
- List jobs: empty list, multiple jobs, ordering
- Update job: change status, verify updated_at changes
- Update job: set nullable fields (video_path, error)

## Likely affected files
- apps/backend/src/tubedigest/database.py (new)
- apps/backend/src/tubedigest/models.py (new)
- apps/backend/src/tubedigest/repository.py (new)
- apps/backend/tests/test_repository.py (new)

## Dependencies
#2 (backend bootstrap - needs pyproject.toml with SQLAlchemy deps)

## Definition of Done
- implementation matches scope
- pytest apps/backend/tests/test_repository.py passes
- All CRUD operations tested with temp SQLite
- PR has test evidence
