# Testing Strategy

TubeDigest is built to demonstrate issue-driven multi-agent development. Tests are part of every issue.

## Test pyramid

1. Contract tests: Pydantic and Zod schemas.
2. Unit tests: backend services and worker handlers.
3. API/component tests: FastAPI and React behavior.
4. Minimal integration tests: fake full pipeline without real external services.

## Backend

- Use pytest.
- Use temporary SQLite DB.
- Mock queue publisher.
- Test status transitions and API responses.

## Workers

- Test `handler.py`, not RabbitMQ loops.
- Use fake deps for DB, publisher, storage, downloader, ffmpeg, Groq.
- Cover success and failure paths.

## Frontend

- Use Vitest + React Testing Library.
- Use mocked API responses.
- Validate responses through Zod.

## External service policy

Unit tests must not call:

- YouTube
- yt-dlp network downloads
- ffmpeg binary
- RabbitMQ
- Groq API

Integration tests may use RabbitMQ only when explicitly named as docker/e2e tests.
