# Testing Strategy

## Core rule
No issue is complete without tests.

## Test layers

### Backend
Tools:

- pytest
- pytest-asyncio where needed
- httpx/TestClient
- temp SQLite

Required coverage:

- API endpoints;
- DB CRUD;
- status transitions;
- publisher abstraction;
- invalid URL handling.

### Workers
Tools:

- pytest
- fake adapters
- fake repository
- fake publisher

Required coverage per worker:

- success path;
- invalid message;
- dependency failure;
- status update;
- next queue publication.

No worker unit test may call real yt-dlp, ffmpeg, RabbitMQ, YouTube, or Groq.

### Contracts
Tools:

- pytest for Pydantic;
- Vitest for Zod.

Required coverage:

- valid payload parsing;
- invalid payload rejection;
- enum values;
- sample fixtures shared by docs/tests where possible.

### Frontend
Tools:

- Vitest;
- React Testing Library;
- mocked fetch or MSW.

Required coverage:

- submit form;
- status badge/timeline;
- result card;
- error state;
- Zod response validation.

### Integration
At least one fake full pipeline test:

```text
create job
→ ytd handler with fake downloader
→ ffmpeg handler with fake processor
→ transcribe handler with fake Groq client
→ summary handler with fake Groq client
→ tags handler with fake Groq client
→ job is completed
```

This test must not require Docker or RabbitMQ.

## Minimum MVP test count

- Backend: 4 tests.
- Frontend: 3 tests.
- Each worker: 3 tests.
- Contracts: 3 tests.
- Pipeline: 1 integration test.

Target: around 26 meaningful tests.
