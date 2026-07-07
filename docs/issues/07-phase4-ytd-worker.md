## Implement ytd download worker

## Owner
worker-agent

## Labels
agent:worker, scope:workers, type:feature

## Context
The first pipeline worker downloads YouTube videos using yt-dlp. It listens on video.download, downloads the video, saves it to storage, and publishes audio.extract and thumbnail.generate messages.

## Scope
- Create workers/ytd/handler.py:
  - handle_message(message, deps) function
  - Validate WorkerMessage
  - Update status to downloading
  - Call yt-dlp adapter to download
  - Save video_path to job
  - Update status to downloaded
  - Publish QUEUE_VIDEO_AUDIO_EXTRACT
  - Publish QUEUE_VIDEO_THUMBNAIL_GENERATE
  - On error: mark job failed, publish QUEUE_VIDEO_FAILED
- Create workers/ytd/adapters.py:
  - Downloader protocol/abstract
  - RealYoutubeDownloader using yt-dlp
  - FakeDownloader for testing
- Create workers/ytd/main.py - RabbitMQ loop entry point
- Create workers/ytd/schemas.py - imports from contracts
- Create workers/ytd/requirements.txt with yt-dlp, pika, tubedigest-contracts
- Create workers/ytd/Dockerfile
- Tests using fake downloader, fake DB, fake publisher

## Out of scope
- ffmpeg processing
- Groq model calls
- Frontend changes

## Acceptance criteria
- Successful download updates job status to downloaded
- Successful download saves video_path in DB
- Successful download publishes audio.extract and thumbnail.generate
- Downloader failure marks job as failed
- Invalid message is rejected (missing job_id, etc.)

## Tests required
- Valid message: handler updates status, calls downloader, saves path, publishes both next messages
- Downloader failure: handler marks job failed, publishes to failed queue
- Invalid message (missing job_id): handler raises validation error
- FakeDownloader returns expected output path

## Likely affected files
- workers/ytd/handler.py (new)
- workers/ytd/adapters.py (new)
- workers/ytd/main.py (new)
- workers/ytd/schemas.py (new)
- workers/ytd/requirements.txt (new)
- workers/ytd/Dockerfile (new)
- workers/ytd/tests/test_handler.py (new)

## Dependencies
None directly - contracts package provides schemas and queues.

## Definition of Done
- implementation matches scope
- pytest workers/ytd/tests passes
- Handler testable without RabbitMQ
- Downloader behind adapter with fake for tests
- PR has test evidence
