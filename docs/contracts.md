# Contracts

Contracts are shared across backend, workers, and frontend.

Backend and workers use Pydantic. Frontend uses Zod. Contract names and enum values must stay aligned.

## REST API

### POST /videos
Request:

```json
{
  "url": "https://www.youtube.com/watch?v=example"
}
```

Response:

```json
{
  "id": "uuid",
  "url": "https://www.youtube.com/watch?v=example",
  "status": "queued",
  "current_step": "queued",
  "created_at": "2026-07-06T12:00:00Z"
}
```

### GET /videos
Returns list of `VideoJobResponse`.

### GET /videos/{id}
Returns one `VideoJobResponse`.

## VideoJobResponse

```json
{
  "id": "uuid",
  "url": "string",
  "title": "string|null",
  "status": "queued|downloading|downloaded|extracting_audio|generating_thumbnail|transcribing|summarizing|generating_tags|completed|failed",
  "current_step": "string",
  "video_path": "string|null",
  "audio_path": "string|null",
  "thumbnail_path": "string|null",
  "transcript": "string|null",
  "summary": "string|null",
  "tags": ["string"],
  "chapters": [
    {
      "start": "00:00",
      "title": "Introduction"
    }
  ],
  "error": "string|null",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## RabbitMQ WorkerMessage
All queues use the same base message:

```json
{
  "job_id": "uuid",
  "video_id": "uuid",
  "attempt": 1
}
```

The backend may include `url` in the first `video.download` message for convenience:

```json
{
  "job_id": "uuid",
  "video_id": "uuid",
  "url": "https://www.youtube.com/watch?v=example",
  "attempt": 1
}
```

## Contract rules

- No agent may silently change field names.
- Contract changes require tests in Python and TypeScript.
- Queue names are constants, not string literals scattered through code.
- Invalid payloads must fail validation loudly.
