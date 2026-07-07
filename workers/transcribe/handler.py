from dataclasses import dataclass
from typing import Protocol, Dict, Any, Optional

from tubedigest.contracts import WorkerMessage
from tubedigest.contracts import (
    QUEUE_VIDEO_SUMMARIZE,
    QUEUE_VIDEO_FAILED,
    JobStatus,
)
from workers.transcribe.adapters import Transcriber


class Database(Protocol):
    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]: ...

    def update_job(self, job_id: str, updates: Dict[str, Any]) -> None: ...


class Publisher(Protocol):
    def publish(self, queue: str, message: dict) -> None: ...


@dataclass
class HandlerDeps:
    db: Database
    publisher: Publisher
    transcriber: Transcriber


def handle_message(message: WorkerMessage, deps: HandlerDeps) -> None:
    try:
        job = deps.db.get_job(message.job_id)
        if job is None:
            raise ValueError(f"job {message.job_id} not found")

        deps.db.update_job(
            message.job_id,
            {"status": JobStatus.transcribing.value},
        )

        audio_path = job.get("audio_path")
        if not audio_path:
            raise ValueError("job has no audio_path")

        transcript = deps.transcriber.transcribe(audio_path)

        deps.db.update_job(
            message.job_id,
            {
                "status": JobStatus.summarizing.value,
                "transcript": transcript,
            },
        )

        deps.publisher.publish(
            QUEUE_VIDEO_SUMMARIZE,
            {"job_id": message.job_id, "video_id": message.video_id},
        )
    except Exception as e:
        deps.db.update_job(
            message.job_id,
            {
                "status": JobStatus.failed.value,
                "error": str(e),
            },
        )
        deps.publisher.publish(
            QUEUE_VIDEO_FAILED,
            {"job_id": message.job_id, "video_id": message.video_id},
        )
