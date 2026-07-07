# TubeDigest — Project Brief

## Goal
Build a one-hour MVP that demonstrates issue-driven multi-agent development with opencode.

The product is a YouTube processing pipeline: a user submits a YouTube URL, the system downloads the video, extracts audio and thumbnail, transcribes audio with Groq Whisper, summarizes the transcript with a Groq LLM, generates tags/chapters, and shows progress in a React dashboard.

## Primary objective
Demonstrate engineering process, not just code generation:

- GitHub Issues drive all work.
- Each issue has one owner, clear scope, acceptance criteria, and tests.
- Agents collaborate through issues, PRs, contracts, CI, and review comments.
- Every layer is protected by automated tests.

## Timebox
The MVP is designed for a 60-minute implementation/demo window.

## MVP scope
Included:

- FastAPI backend.
- SQLite + SQLAlchemy persistence.
- RabbitMQ messaging.
- React + Vite + TypeScript frontend.
- Tailwind CSS UI.
- Zod frontend validation.
- Pydantic backend/worker validation.
- yt-dlp download worker.
- ffmpeg media worker.
- Groq transcription worker.
- Groq summary worker.
- Groq tags/chapters worker.
- GitHub Actions CI.
- GitHub CLI workflow documentation.
- Autotests for backend, frontend, workers, contracts, and one fake pipeline integration test.

Excluded from MVP:

- User accounts.
- Payments.
- Persistent object storage like S3/MinIO.
- Real-time WebSocket updates.
- Production deployment.
- Long video support.
- Perfect transcription accuracy.

## Demo constraints
To keep the demo reliable:

- Unit tests must never call real YouTube, RabbitMQ, ffmpeg, or Groq.
- Real external integrations are allowed in runtime, but must be behind adapters.
- Video length should be limited by configuration.
- The project must support fake/mock mode for CI and local testing.
