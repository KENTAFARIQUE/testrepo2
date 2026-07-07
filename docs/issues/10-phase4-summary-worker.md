## Implement Groq summary worker

## Owner
worker-agent

## Labels
agent:worker, scope:workers, type:feature

## Context
The summary worker uses a Groq LLM to summarize transcripts. It listens on video.summarize, reads the transcript, calls Groq LLM, saves the summary, and publishes video.tags.

## Scope
- Create workers/summary/handler.py:
  - handle_message(message, deps) function
  - Validate WorkerMessage
  - Load transcript from job
  - Call Groq LLM adapter to generate summary
  - Save summary in DB
  - Publish QUEUE_VIDEO_TAGS
  - On error: mark job failed, publish QUEUE_VIDEO_FAILED
- Create workers/summary/adapters.py:
  - Summarizer protocol
  - GroqSummarizer using groq SDK
  - FakeSummarizer for testing (returns canned text)
- Create workers/summary/main.py - RabbitMQ loop entry point
- Create workers/summary/schemas.py - imports from contracts
- Create workers/summary/requirements.txt with groq, pika, tubedigest-contracts
- Create workers/summary/Dockerfile
- Tests using fake summarizer, fake DB, fake publisher

## Out of scope
- Transcription (handled by transcribe-worker)
- Tags/chapters generation (handled by tags-worker)
- Frontend changes

## Acceptance criteria
- Successful summarization updates summary field in DB
- Successful summarization publishes video.tags
- Groq API failure marks job as failed
- Empty transcript handled gracefully
- Invalid messages are rejected

## Tests required
- Valid message: handler summarizes, saves summary, publishes tags
- Groq failure: handler marks job failed, publishes to failed queue
- Invalid message: rejected with validation error
- FakeSummarizer returns expected summary text

## Likely affected files
- workers/summary/handler.py (new)
- workers/summary/adapters.py (new)
- workers/summary/main.py (new)
- workers/summary/schemas.py (new)
- workers/summary/requirements.txt (new)
- workers/summary/Dockerfile (new)
- workers/summary/tests/test_handler.py (new)

## Dependencies
None directly - contracts package provides schemas and queues.

## Definition of Done
- implementation matches scope
- pytest workers/summary/tests passes
- Handler testable without RabbitMQ
- Groq behind adapter with fake for tests
- PR has test evidence
