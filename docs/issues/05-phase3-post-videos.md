## Add POST /videos endpoint with queue publishing

## Owner
backend-agent

## Labels
agent:backend, scope:backend, type:feature

## Context
Users need to submit YouTube URLs for processing. This issue creates the POST /videos endpoint that validates the input, creates a VideoJob record, publishes a video.download message to RabbitMQ, and returns the job response.

## Scope
- Create apps/backend/src/tubedigest/routers/videos.py:
  - POST /videos endpoint
  - Accept CreateVideoRequest body (url string)
  - Call repository.create_job() to insert VideoJob
  - Construct WorkerMessage with job_id, video_id, url, attempt=1
  - Call publisher.publish(QUEUE_VIDEO_DOWNLOAD, message)
  - Return VideoJobResponse with 201 status
- Wire router into FastAPI app in main.py
- Tests for success and failure paths

## Out of scope
- GET endpoints
- URL format validation beyond non-empty
- Processing pipeline (handled by workers)

## Acceptance criteria
- POST /videos with valid URL returns 201 and VideoJobResponse
- Response body contains id, url, status=queued, current_step=queued
- A video.download WorkerMessage is published with correct job_id and url
- Empty url returns 422 ValidationError
- Published message has attempt=1

## Tests required
- Valid URL returns 201 with correct response shape
- Valid URL publishes video.download via FakePublisher
- Empty URL body returns 422
- DB contains new job with status=queued after POST
- Response fields match VideoJobResponse schema (id is UUID, etc.)

## Likely affected files
- apps/backend/src/tubedigest/routers/__init__.py (new)
- apps/backend/src/tubedigest/routers/videos.py (new)
- apps/backend/src/tubedigest/main.py (modify - add router)
- apps/backend/tests/test_api.py (new)

## Dependencies
- #3 (VideoJob model and repository)
- #4 (RabbitMQ publisher abstraction)

## Definition of Done
- implementation matches scope
- pytest apps/backend/tests/test_api.py passes
- POST /videos creates job, publishes message, returns 201
- Invalid URL returns 422
- PR has test evidence
