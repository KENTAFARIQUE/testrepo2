# Example Issues

## Issue: Backend video creation endpoint

Goal: Implement `POST /videos`.

Scope:
- Validate URL.
- Create `VideoJob` with status `queued`.
- Publish `video.download` message.

Required tests:
- valid URL creates job;
- invalid URL returns 422;
- queue publisher receives valid `WorkerMessage`;
- DB row has expected initial status.

## Issue: ytd worker

Goal: Implement download worker handler.

Scope:
- Consume `WorkerMessage`.
- Use downloader adapter.
- Save `video_path`.
- Publish `video.audio.extract` and `video.thumbnail.generate`.

Required tests:
- successful download updates job;
- publishes both next messages;
- downloader error marks failed;
- invalid message is rejected.

## Issue: Frontend status timeline

Goal: Render job progress from status/current_step.

Required tests:
- queued job shows first step active;
- transcribing job shows previous steps complete;
- failed job shows error state;
- completed job shows result card.
