## Implement Groq tags/chapters worker

## Owner
worker-agent

## Labels
agent:worker, scope:workers, type:feature

## Context
The tags worker uses a Groq LLM to generate tags and chapters from the transcript and summary. It listens on video.tags, processes the content, saves tags and chapters, and marks the job as completed.

## Scope
- Create workers/tags/handler.py:
  - handle_message(message, deps) function
  - Validate WorkerMessage
  - Load transcript and summary from job
  - Call Groq LLM adapter to generate tags and chapters
  - Save tags and chapters in DB
  - Update status to completed
  - On error: mark job failed, publish QUEUE_VIDEO_FAILED
- Create workers/tags/adapters.py:
  - Tagger protocol
  - GroqTagger using groq SDK
  - FakeTagger for testing (returns canned tags/chapters)
- Create workers/tags/main.py - RabbitMQ loop entry point
- Create workers/tags/schemas.py - imports from contracts
- Create workers/tags/requirements.txt with groq, pika, tubedigest-contracts
- Create workers/tags/Dockerfile
- Tests using fake tagger, fake DB, fake publisher

## Out of scope
- Summarization (handled by summary-worker)
- Transcription (handled by transcribe-worker)
- Frontend changes

## Acceptance criteria
- Successful processing saves tags array in DB
- Successful processing saves chapters array in DB
- Successful processing sets status to completed
- Groq API failure marks job as failed
- Empty input handled gracefully
- Invalid messages are rejected

## Tests required
- Valid message: handler generates tags/chapters, saves them, marks completed
- Groq failure: handler marks job failed, publishes to failed queue
- Invalid message: rejected with validation error
- FakeTagger returns expected tags and chapters
- Completed job has status=completed

## Likely affected files
- workers/tags/handler.py (new)
- workers/tags/adapters.py (new)
- workers/tags/main.py (new)
- workers/tags/schemas.py (new)
- workers/tags/requirements.txt (new)
- workers/tags/Dockerfile (new)
- workers/tags/tests/test_handler.py (new)

## Dependencies
None directly - contracts package provides schemas and queues.

## Definition of Done
- implementation matches scope
- pytest workers/tags/tests passes
- Handler testable without RabbitMQ
- Groq behind adapter with fake for tests
- PR has test evidence
