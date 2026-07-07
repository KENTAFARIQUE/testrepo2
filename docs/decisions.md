# Architecture Decision Records

## ADR-001 — Use FastAPI for backend
Status: accepted

Reason: FastAPI is quick to scaffold, has good Pydantic support, and fits async API work.

## ADR-002 — Use SQLite for MVP persistence
Status: accepted

Reason: SQLite reduces setup cost and is enough for a one-hour MVP. PostgreSQL is out of scope.

## ADR-003 — Use SQLAlchemy
Status: accepted

Reason: SQLAlchemy gives explicit models and can be moved to PostgreSQL later if needed.

## ADR-004 — Use RabbitMQ for messaging
Status: accepted

Reason: RabbitMQ clearly demonstrates queue-driven worker orchestration and routing.

## ADR-005 — Use local filesystem storage
Status: accepted

Reason: S3/MinIO would add setup overhead. Local storage is enough for demo artifacts.

## ADR-006 — Use Groq for model workers
Status: accepted

Reason: Groq offers fast API access to Whisper and LLM models without local GPU setup.

## ADR-007 — Use fake adapters in tests
Status: accepted

Reason: CI must be deterministic and must not depend on YouTube, ffmpeg, RabbitMQ, or paid API calls.

## ADR-008 — Documentation is source of truth
Status: accepted

Reason: Agents need stable context. If code and docs disagree, the agent must stop and report inconsistency.
