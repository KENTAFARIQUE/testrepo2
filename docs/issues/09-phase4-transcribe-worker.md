## Implement Groq transcription worker

## Owner
worker-agent

## Labels
agent:worker, scope:workers, type:feature

## Context
The transcription worker uses Groq Whisper to transcribe audio. It listens on video.transcribe, loads the audio file, calls Groq Whisper, saves the transcript, and publishes video.summarize.

## Scope
- Create workers/transcribe/handler.py:
  - handle_message(message, deps) function
  - Validate WorkerMessage
  - Load audio_path from job
  - Call Groq Whisper adapter to transcribe
  - Save transcript in DB
  - Publish QUEUE_VIDEO_SUMMARIZE
  - On error: mark job failed, publish QUEUE_VIDEO_FAILED
- Create workers/transcribe/adapters.py:
  - Transcriber protocol
  - GroqTranscriber using groq SDK
  - FakeTranscriber for testing (returns canned text)
- Create workers/transcribe/main.py - RabbitMQ loop entry point
- Create workers/transcribe/schemas.py - imports from contracts
- Create workers/transcribe/requirements.txt with groq, pika, tubedigest-contracts
- Create workers/transcribe/Dockerfile
- Tests using fake transcriber, fake DB, fake publisher

## Out of scope
- ffmpeg or yt-dlp operations
- LLM summarization
- Frontend changes

## Acceptance criteria
- Successful transcription updates transcript field in DB
- Successful transcription publishes video.summarize
- Groq API failure marks job as failed
- Invalid messages are rejected
- Fake transcriber works without Groq API key

## Tests required
- Valid message: handler transcribes, saves transcript, publishes summarize
- Groq failure: handler marks job failed, publishes to failed queue
- Invalid message: rejected with validation error
- FakeTranscriber returns expected transcript text

## Likely affected files
- workers/transcribe/handler.py (new)
- workers/transcribe/adapters.py (new)
- workers/transcribe/main.py (new)
- workers/transcribe/schemas.py (new)
- workers/transcribe/requirements.txt (new)
- workers/transcribe/Dockerfile (new)
- workers/transcribe/tests/test_handler.py (new)

## Dependencies
None directly - contracts package provides schemas and queues.

## Definition of Done
- implementation matches scope
- pytest workers/transcribe/tests passes
- Handler testable without RabbitMQ
- Groq behind adapter with fake for tests
- PR has test evidence
