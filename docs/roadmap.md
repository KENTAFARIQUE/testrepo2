# MVP Roadmap

## Phase 1 — Repository and infrastructure
Goal: create a runnable skeleton.

Issues:

- Bootstrap monorepo structure.
- Add Docker Compose with RabbitMQ.
- Add Makefile and `.env.example`.
- Add CI skeleton.

## Phase 2 — Contracts
Goal: define shared API and queue contracts.

Issues:

- Add Pydantic schemas.
- Add Zod schemas.
- Add queue constants and WorkerMessage.
- Add contract tests.

## Phase 3 — Backend
Goal: allow user to create and inspect jobs.

Issues:

- Add SQLAlchemy VideoJob model.
- Add POST /videos.
- Add GET /videos and GET /videos/{id}.
- Add RabbitMQ publisher abstraction.

## Phase 4 — Workers
Goal: implement asynchronous pipeline.

Issues:

- ytd download worker.
- ffmpeg audio worker.
- ffmpeg thumbnail worker.
- Groq transcribe worker.
- Groq summary worker.
- Groq tags/chapters worker.

## Phase 5 — Frontend
Goal: show the pipeline to the user.

Issues:

- Add URL submit form.
- Add job list.
- Add status timeline.
- Add result card.
- Add frontend tests.

## Phase 6 — Quality gate
Goal: make agents accountable.

Issues:

- Add GitHub Actions CI.
- Add agent guard workflow.
- Add PR/issue templates.
- Add fake full pipeline integration test.

## Phase 7 — Demo
Goal: make the project easy to present.

Issues:

- Add README demo script.
- Add sample issue flow.
- Add troubleshooting docs.
