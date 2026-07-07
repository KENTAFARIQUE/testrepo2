# Processing Pipeline

## Happy path

```text
POST /videos
  ↓
Backend creates VideoJob(status=queued)
  ↓
RabbitMQ: video.download
  ↓
ytd-worker
  ↓
RabbitMQ:
  ├─ video.audio.extract
  └─ video.thumbnail.generate
  ↓
ffmpeg-worker
  ↓
RabbitMQ: video.transcribe
  ↓
transcribe-worker / Groq Whisper
  ↓
RabbitMQ: video.summarize
  ↓
summary-worker / Groq LLM
  ↓
RabbitMQ: video.tags
  ↓
tags-worker / Groq LLM
  ↓
VideoJob(status=completed)
```

## Queues

- `video.download`
- `video.audio.extract`
- `video.thumbnail.generate`
- `video.transcribe`
- `video.summarize`
- `video.tags`
- `video.failed`

## Statuses

- `queued`
- `downloading`
- `downloaded`
- `extracting_audio`
- `generating_thumbnail`
- `transcribing`
- `summarizing`
- `generating_tags`
- `completed`
- `failed`

## Parallelism
After download, two independent branches can run:

```text
video.mp4
  ├─ audio extraction → transcription → summary → tags
  └─ thumbnail generation
```

The thumbnail branch must not block transcription unless the frontend requires the thumbnail for display.

## Failure handling
Each worker must:

1. validate the input message;
2. mark the job as the active status;
3. run its adapter;
4. update the job with output paths/results;
5. publish the next message;
6. mark the job failed on unrecoverable error.

Retries and DLQ can be represented in the MVP as documented behavior plus minimal queue naming, but unit tests must cover failure paths.
