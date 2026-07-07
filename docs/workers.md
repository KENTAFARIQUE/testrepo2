# Workers

## Shared worker design
Each worker should have this shape:

```text
main.py      # RabbitMQ loop and process wiring
handler.py   # pure/testable business flow
adapters.py  # external tool/API wrappers
schemas.py   # worker-local imports from contracts
```

Handlers receive dependencies explicitly:

```python
handle_message(message, deps)
```

Dependencies may include:

- repository/database client;
- publisher;
- storage path builder;
- downloader;
- ffmpeg adapter;
- Groq client.

## ytd-worker
Owns queue: `video.download`.

Responsibilities:

- validate `WorkerMessage`;
- update status to `downloading`;
- download video with yt-dlp adapter;
- save `video_path`;
- update status to `downloaded`;
- publish `video.audio.extract`;
- publish `video.thumbnail.generate`.

Must not:

- run ffmpeg;
- call Groq;
- create summaries;
- touch frontend code.

## ffmpeg-worker
Owns queues:

- `video.audio.extract`
- `video.thumbnail.generate`

Responsibilities:

- extract audio file;
- generate thumbnail image;
- save `audio_path` and `thumbnail_path`;
- publish `video.transcribe` after audio extraction.

Must not:

- download videos;
- call Groq;
- summarize transcript.

## transcribe-worker
Owns queue: `video.transcribe`.

Responsibilities:

- load `audio_path`;
- call Groq Whisper through adapter;
- save transcript in DB and/or `storage/transcripts/`;
- publish `video.summarize`.

Must not:

- call yt-dlp;
- run ffmpeg;
- generate UI output directly.

## summary-worker
Owns queue: `video.summarize`.

Responsibilities:

- read transcript;
- call Groq LLM through adapter;
- save summary and key points;
- publish `video.tags`.

## tags-worker
Owns queue: `video.tags`.

Responsibilities:

- read transcript and summary;
- call Groq LLM or deterministic fallback;
- save tags and chapters;
- mark job `completed`.

## Testing requirement
Every worker issue must include tests for:

- valid message success path;
- invalid message rejection;
- adapter failure;
- DB update;
- next queue publication where applicable.
