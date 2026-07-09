from dataclasses import dataclass
from typing import Protocol, Dict, Any, Optional

from tubedigest.contracts import WorkerMessage
from tubedigest.contracts import (
    QUEUE_VIDEO_TRANSCRIBE,
    QUEUE_VIDEO_FAILED,
    QUEUE_VIDEO_STATUS,
    JobStatus,
)
from workers.ffmpeg.adapters import FfmpegAdapter


class Database(Protocol):
    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]: ...

    def update_job(self, job_id: str, updates: Dict[str, Any]) -> None: ...


class Publisher(Protocol):
    def publish(self, queue: str, message: dict) -> None: ...


@dataclass
class HandlerDeps:
    db: Database
    publisher: Publisher
    ffmpeg: FfmpegAdapter
    audio_dir: str
    thumbnails_dir: str


def handle_audio_extract(message: WorkerMessage, deps: HandlerDeps) -> None:
    try:
        job = deps.db.get_job(message.job_id)
        if job is None:
            raise ValueError(f"job {message.job_id} not found")

        deps.db.update_job(
            message.job_id,
            {"status": JobStatus.extracting_audio.value},
        )
        deps.publisher.publish(
            QUEUE_VIDEO_STATUS,
            {"job_id": message.job_id, "status": "extracting_audio", "current_step": "extracting_audio"},
        )

        video_path = job.get("video_path")
        if not video_path:
            raise ValueError("job has no video_path")

        audio_path = deps.ffmpeg.extract_audio(video_path, deps.audio_dir)

        deps.db.update_job(
            message.job_id,
            {
                "status": JobStatus.transcribing.value,
                "audio_path": audio_path,
            },
        )
        deps.publisher.publish(
            QUEUE_VIDEO_STATUS,
            {"job_id": message.job_id, "status": "transcribing", "current_step": "transcribing"},
        )

        deps.publisher.publish(
            QUEUE_VIDEO_TRANSCRIBE,
            {"job_id": message.job_id, "video_id": message.video_id},
        )
    except Exception as e:
        _fail(message, deps, str(e))


def handle_thumbnail_generate(message: WorkerMessage, deps: HandlerDeps) -> None:
    try:
        job = deps.db.get_job(message.job_id)
        if job is None:
            raise ValueError(f"job {message.job_id} not found")

        deps.db.update_job(
            message.job_id,
            {"status": JobStatus.generating_thumbnail.value},
        )
        deps.publisher.publish(
            QUEUE_VIDEO_STATUS,
            {"job_id": message.job_id, "status": "generating_thumbnail", "current_step": "generating_thumbnail"},
        )

        video_path = job.get("video_path")
        if not video_path:
            raise ValueError("job has no video_path")

        thumbnail_path = deps.ffmpeg.generate_thumbnail(video_path, deps.thumbnails_dir)

        deps.db.update_job(
            message.job_id,
            {
                "thumbnail_path": thumbnail_path,
            },
        )
    except Exception as e:
        _fail(message, deps, str(e))


def _fail(message: WorkerMessage, deps: HandlerDeps, error: str) -> None:
    deps.db.update_job(
        message.job_id,
        {
            "status": JobStatus.failed.value,
            "error": error,
        },
    )
    deps.publisher.publish(
        QUEUE_VIDEO_STATUS,
        {"job_id": message.job_id, "status": "failed", "current_step": "queued"},
    )
    deps.publisher.publish(
        QUEUE_VIDEO_FAILED,
        {"job_id": message.job_id, "video_id": message.video_id},
    )
