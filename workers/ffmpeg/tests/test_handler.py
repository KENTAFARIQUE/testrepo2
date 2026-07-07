import os
import tempfile
from typing import Dict, Any, List, Tuple, Optional

import pytest
from tubedigest.contracts import WorkerMessage

from workers.ffmpeg.handler import (
    handle_audio_extract,
    handle_thumbnail_generate,
    HandlerDeps,
)


class FakeDb:
    def __init__(self):
        self.jobs: Dict[str, Dict[str, Any]] = {}

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        return self.jobs.get(job_id)

    def update_job(self, job_id: str, updates: Dict[str, Any]) -> None:
        if job_id not in self.jobs:
            self.jobs[job_id] = {}
        self.jobs[job_id].update(updates)


class FakePublisher:
    def __init__(self):
        self.messages: List[Tuple[str, dict]] = []

    def publish(self, queue: str, message: dict) -> None:
        self.messages.append((queue, message))


class FakeFfmpegAdapter:
    def __init__(self, raise_on_audio: bool = False, raise_on_thumbnail: bool = False):
        self._raise_audio = raise_on_audio
        self._raise_thumbnail = raise_on_thumbnail

    def extract_audio(self, video_path: str, output_dir: str) -> str:
        if self._raise_audio:
            raise RuntimeError("audio extraction failed")
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, "audio.mp3")
        with open(path, "wb") as f:
            f.write(b"fake audio")
        return path

    def generate_thumbnail(self, video_path: str, output_dir: str) -> str:
        if self._raise_thumbnail:
            raise RuntimeError("thumbnail generation failed")
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, "thumb.jpg")
        with open(path, "wb") as f:
            f.write(b"fake thumbnail")
        return path


@pytest.fixture
def deps():
    db = FakeDb()
    publisher = FakePublisher()
    ffmpeg = FakeFfmpegAdapter()
    audio_dir = tempfile.mkdtemp()
    thumbnails_dir = tempfile.mkdtemp()
    return HandlerDeps(
        db=db,
        publisher=publisher,
        ffmpeg=ffmpeg,
        audio_dir=audio_dir,
        thumbnails_dir=thumbnails_dir,
    )


class TestFfmpegHandler:
    def test_audio_extract_happy_path(self, deps: HandlerDeps):
        deps.db.jobs["job-1"] = {"video_path": "/tmp/test_video.mp4"}
        message = WorkerMessage(job_id="job-1", video_id="vid-1")

        handle_audio_extract(message, deps)

        job = deps.db.jobs["job-1"]
        assert job["status"] == "transcribing"
        assert os.path.exists(job["audio_path"])

        queues = [q for q, _ in deps.publisher.messages]
        assert "video.transcribe" in queues

    def test_audio_extract_missing_job(self, deps: HandlerDeps):
        message = WorkerMessage(job_id="nonexistent", video_id="vid-1")

        handle_audio_extract(message, deps)

        assert deps.db.jobs["nonexistent"]["status"] == "failed"
        queues = [q for q, _ in deps.publisher.messages]
        assert "video.failed" in queues

    def test_audio_extract_missing_video_path(self, deps: HandlerDeps):
        deps.db.jobs["job-2"] = {}
        message = WorkerMessage(job_id="job-2", video_id="vid-2")

        handle_audio_extract(message, deps)

        assert deps.db.jobs["job-2"]["status"] == "failed"
        assert "no video_path" in deps.db.jobs["job-2"]["error"]

    def test_audio_extract_adapter_failure(self, deps: HandlerDeps):
        deps.ffmpeg = FakeFfmpegAdapter(raise_on_audio=True)
        deps.db.jobs["job-3"] = {"video_path": "/tmp/test_video.mp4"}
        message = WorkerMessage(job_id="job-3", video_id="vid-3")

        handle_audio_extract(message, deps)

        assert deps.db.jobs["job-3"]["status"] == "failed"
        assert "audio extraction failed" in deps.db.jobs["job-3"]["error"]
        queues = [q for q, _ in deps.publisher.messages]
        assert "video.failed" in queues
        assert "video.transcribe" not in queues

    def test_thumbnail_happy_path(self, deps: HandlerDeps):
        deps.db.jobs["job-4"] = {"video_path": "/tmp/test_video.mp4"}
        message = WorkerMessage(job_id="job-4", video_id="vid-4")

        handle_thumbnail_generate(message, deps)

        job = deps.db.jobs["job-4"]
        assert os.path.exists(job["thumbnail_path"])

    def test_thumbnail_missing_job(self, deps: HandlerDeps):
        message = WorkerMessage(job_id="nonexistent", video_id="vid-5")

        handle_thumbnail_generate(message, deps)

        assert deps.db.jobs["nonexistent"]["status"] == "failed"

    def test_thumbnail_adapter_failure(self, deps: HandlerDeps):
        deps.ffmpeg = FakeFfmpegAdapter(raise_on_thumbnail=True)
        deps.db.jobs["job-6"] = {"video_path": "/tmp/test_video.mp4"}
        message = WorkerMessage(job_id="job-6", video_id="vid-6")

        handle_thumbnail_generate(message, deps)

        assert deps.db.jobs["job-6"]["status"] == "failed"
        assert "thumbnail generation failed" in deps.db.jobs["job-6"]["error"]
