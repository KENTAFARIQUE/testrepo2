import json
from dataclasses import dataclass
from typing import Protocol, Dict, Any, Optional

from tubedigest.contracts import WorkerMessage
from tubedigest.contracts import (
    QUEUE_VIDEO_FAILED,
    QUEUE_VIDEO_STATUS,
    JobStatus,
)
from workers.tags.adapters import Tagger


class Database(Protocol):
    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]: ...

    def update_job(self, job_id: str, updates: Dict[str, Any]) -> None: ...


class Publisher(Protocol):
    def publish(self, queue: str, message: dict) -> None: ...


@dataclass
class HandlerDeps:
    db: Database
    publisher: Publisher
    tagger: Tagger


def handle_message(message: WorkerMessage, deps: HandlerDeps) -> None:
    try:
        job = deps.db.get_job(message.job_id)
        if job is None:
            raise ValueError(f"job {message.job_id} not found")

        deps.db.update_job(
            message.job_id,
            {"status": JobStatus.generating_tags.value},
        )
        deps.publisher.publish(
            QUEUE_VIDEO_STATUS,
            {"job_id": message.job_id, "status": "generating_tags", "current_step": "generating_tags"},
        )

        transcript = job.get("transcript")
        summary = job.get("summary")
        if not transcript:
            raise ValueError("job has no transcript")
        if not summary:
            raise ValueError("job has no summary")

        result = deps.tagger.generate_tags_and_chapters(transcript, summary)
        tags = result.get("tags", [])
        chapters = result.get("chapters", [])

        deps.db.update_job(
            message.job_id,
            {
                "status": JobStatus.completed.value,
                "tags": json.dumps(tags),
                "chapters": json.dumps(chapters),
            },
        )
        deps.publisher.publish(
            QUEUE_VIDEO_STATUS,
            {"job_id": message.job_id, "status": "completed", "current_step": "completed"},
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
            QUEUE_VIDEO_STATUS,
            {"job_id": message.job_id, "status": "failed", "current_step": "queued"},
        )
        deps.publisher.publish(
            QUEUE_VIDEO_FAILED,
            {"job_id": message.job_id, "video_id": message.video_id},
        )
