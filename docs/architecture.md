# Architecture

## System shape
TubeDigest is a small asynchronous media-processing system.

```text
Frontend
  ↓ HTTP
Backend API
  ↓ SQLite
Database
  ↓ publish
RabbitMQ
  ↓ consume
Workers
  ↓ update
Database + local storage
```

## Applications

### Backend
FastAPI application responsible for:

- accepting video processing requests;
- validating API input;
- creating `VideoJob` records;
- exposing job status and results;
- publishing initial RabbitMQ messages.

The backend must not download videos, run ffmpeg, call Groq, or process media.

### Frontend
React application responsible for:

- URL submission;
- job list;
- job details;
- status timeline;
- result rendering;
- user-visible error states.

The frontend only communicates with the backend over HTTP. It never talks to RabbitMQ directly.

### Workers
Workers are independent processes. Each worker consumes one queue or one closely related family of queues and performs one responsibility.

Workers must be mostly stateless. Long-lived state belongs in SQLite or local storage.

## Persistence
SQLite is used for the MVP because it is fast to set up and easy to run locally.

SQLAlchemy is the ORM.

## Storage
Local filesystem storage is used for demo media artifacts:

- `storage/videos/`
- `storage/audio/`
- `storage/thumbnails/`
- `storage/transcripts/`

Media artifacts must not be committed to git.

## Messaging
RabbitMQ coordinates asynchronous work.

Rules:

- Workers do not call each other directly.
- Workers publish the next message only after successfully updating the job state.
- Queue messages carry IDs and metadata, not large files.
- File paths and results are stored in the database or filesystem.

## Architectural principles

1. One component, one responsibility.
2. Message contracts are explicit and validated.
3. External tools and APIs live behind adapters.
4. Business logic is testable without infrastructure.
5. CI must run without paid APIs or flaky external services.
6. Documentation is the source of truth for agents.
