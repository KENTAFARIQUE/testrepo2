## Implement ffmpeg media worker

## Owner
worker-agent

## Labels
agent:worker, scope:workers, type:feature

## Context
The ffmpeg worker handles audio extraction and thumbnail generation. It listens on two queues: video.audio.extract and video.thumbnail.generate. After audio extraction it publishes video.transcribe.

## Scope
- Create workers/ffmpeg/handler.py:
  - handle_audio_extract(message, deps) function
  - handle_thumbnail_generate(message, deps) function
  - Validate WorkerMessage
  - Call ffmpeg adapter to extract audio and/or generate thumbnail
  - Save audio_path and thumbnail_path in DB
  - After audio extraction: publish QUEUE_VIDEO_TRANSCRIBE
  - On error: mark job failed, publish QUEUE_VIDEO_FAILED
- Create workers/ffmpeg/adapters.py:
  - FfmpegAdapter protocol with extract_audio() and generate_thumbnail()
  - RealFfmpegAdapter using subprocess/ffmpeg binary
  - FakeFfmpegAdapter for testing
- Create workers/ffmpeg/main.py - RabbitMQ loop entry point
- Create workers/ffmpeg/schemas.py - imports from contracts
- Create workers/ffmpeg/requirements.txt with pika, tubedigest-contracts
- Create workers/ffmpeg/Dockerfile with ffmpeg installed
- Tests using fake ffmpeg adapter, fake DB, fake publisher

## Out of scope
- Video downloading (handled by ytd-worker)
- Groq model calls
- Frontend changes

## Acceptance criteria
- Audio extraction updates audio_path and status
- Thumbnail generation updates thumbnail_path and status
- Audio extraction publishes video.transcribe message
- Both operations handle ffmpeg failures gracefully
- Invalid messages are rejected

## Tests required
- Audio extraction: updates status, calls adapter, saves path, publishes transcribe
- Thumbnail generation: updates status, calls adapter, saves path
- Adapter failure: marks job failed, publishes to failed queue
- Invalid message: rejected with validation error
- FakeFfmpegAdapter returns expected paths

## Likely affected files
- workers/ffmpeg/handler.py (new)
- workers/ffmpeg/adapters.py (new)
- workers/ffmpeg/main.py (new)
- workers/ffmpeg/schemas.py (new)
- workers/ffmpeg/requirements.txt (new)
- workers/ffmpeg/Dockerfile (new)
- workers/ffmpeg/tests/test_handler.py (new)

## Dependencies
None directly - contracts package provides schemas and queues.

## Definition of Done
- implementation matches scope
- pytest workers/ffmpeg/tests passes
- Handler testable without RabbitMQ
- ffmpeg behind adapter with fake for tests
- PR has test evidence
