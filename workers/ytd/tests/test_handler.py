import os
import tempfile
from typing import Dict, Any, List, Tuple

import pytest
from tubedigest.contracts import WorkerMessage

from workers.ytd.handler import handle_message, HandlerDeps


class FakeDb:
    def __init__(self):
        self.jobs: Dict[str, Dict[str, Any]] = {}

    def update_job(self, job_id: str, updates: Dict[str, Any]) -> None:
        if job_id not in self.jobs:
            self.jobs[job_id] = {}
        self.jobs[job_id].update(updates)


class FakePublisher:
    def __init__(self):
        self.messages: List[Tuple[str, dict]] = []

    def publish(self, queue: str, message: dict) -> None:
        self.messages.append((queue, message))


class FakeDownloader:
    def __init__(self, raise_on_download: bool = False):
        self._raise = raise_on_download

    def download(self, url: str, work_dir: str) -> str:
        if self._raise:
            raise RuntimeError("download failed")
        os.makedirs(work_dir, exist_ok=True)
        path = os.path.join(work_dir, "test_video.mp4")
        with open(path, "wb") as f:
            f.write(b"test video content")
        return path


@pytest.fixture
def deps():
    db = FakeDb()
    publisher = FakePublisher()
    downloader = FakeDownloader()
    videos_dir = tempfile.mkdtemp()
    return HandlerDeps(
        db=db,
        publisher=publisher,
        downloader=downloader,
        videos_dir=videos_dir,
    )


class TestYtdHandler:
    def test_happy_path(self, deps: HandlerDeps):
        message = WorkerMessage(
            job_id="job-1",
            video_id="vid-1",
            url="https://www.youtube.com/watch?v=test123",
        )

        handle_message(message, deps)

        job = deps.db.jobs["job-1"]
        assert job["status"] == "downloaded"
        assert job["video_path"] is not None
        assert os.path.exists(job["video_path"])

        queues = [q for q, _ in deps.publisher.messages]
        assert "video.audio.extract" in queues
        assert "video.thumbnail.generate" in queues

    def test_downloader_failure(self, deps: HandlerDeps):
        deps.downloader = FakeDownloader(raise_on_download=True)
        message = WorkerMessage(
            job_id="job-2",
            video_id="vid-2",
            url="https://www.youtube.com/watch?v=bad",
        )

        handle_message(message, deps)

        job = deps.db.jobs["job-2"]
        assert job["status"] == "failed"
        assert "download failed" in job["error"]

        queues = [q for q, _ in deps.publisher.messages]
        assert "video.failed" in queues
        assert "video.audio.extract" not in queues

    def test_missing_url_raises(self):
        db = FakeDb()
        publisher = FakePublisher()
        downloader = FakeDownloader()
        deps = HandlerDeps(
            db=db,
            publisher=publisher,
            downloader=downloader,
            videos_dir="/tmp",
        )
        message = WorkerMessage(
            job_id="job-3",
            video_id="vid-3",
            url=None,
        )

        with pytest.raises(ValueError, match="url is required"):
            handle_message(message, deps)

        job = db.jobs.get("job-3")
        if job:
            assert job["status"] == "failed"
