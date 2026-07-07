from dataclasses import dataclass
from typing import Protocol, Dict, Any

from tubedigest.contracts import WorkerMessage
from tubedigest.contracts import (
    QUEUE_VIDEO_AUDIO_EXTRACT,
    QUEUE_VIDEO_THUMBNAIL_GENERATE,
    QUEUE_VIDEO_FAILED,
    JobStatus,
)
from workers.ytd.adapters import Downloader


class Database(Protocol):
    def update_job(self, job_id: str, updates: Dict[str, Any]) -> None: ...


class Publisher(Protocol):
    def publish(self, queue: str, message: dict) -> None: ...


@dataclass
class HandlerDeps:
    db: Database
    publisher: Publisher
    downloader: Downloader
    videos_dir: str


def handle_message(message: WorkerMessage, deps: HandlerDeps) -> None:
    if message.url is None:
        raise ValueError("message.url is required for video.download")

    try:
        deps.db.update_job(
            message.job_id,
            {"status": JobStatus.downloading.value},
        )

        video_path = deps.downloader.download(message.url, deps.videos_dir)

        deps.db.update_job(
            message.job_id,
            {
                "status": JobStatus.downloaded.value,
                "video_path": video_path,
            },
        )

        deps.publisher.publish(
            QUEUE_VIDEO_AUDIO_EXTRACT,
            {"job_id": message.job_id, "video_id": message.video_id},
        )
        deps.publisher.publish(
            QUEUE_VIDEO_THUMBNAIL_GENERATE,
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
