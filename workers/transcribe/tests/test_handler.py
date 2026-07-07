from typing import Dict, Any, List, Tuple, Optional

import pytest
from tubedigest.contracts import WorkerMessage

from workers.transcribe.handler import handle_message, HandlerDeps


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


class FakeTranscriber:
    def __init__(self, raise_on_transcribe: bool = False):
        self._raise = raise_on_transcribe

    def transcribe(self, audio_path: str) -> str:
        if self._raise:
            raise RuntimeError("transcription failed")
        return "fake transcript text"


@pytest.fixture
def deps():
    db = FakeDb()
    publisher = FakePublisher()
    transcriber = FakeTranscriber()
    return HandlerDeps(db=db, publisher=publisher, transcriber=transcriber)


class TestTranscribeHandler:
    def test_happy_path(self, deps: HandlerDeps):
        deps.db.jobs["job-1"] = {"audio_path": "/tmp/test.mp3"}
        message = WorkerMessage(job_id="job-1", video_id="vid-1")

        handle_message(message, deps)

        job = deps.db.jobs["job-1"]
        assert job["status"] == "summarizing"
        assert job["transcript"] == "fake transcript text"

        queues = [q for q, _ in deps.publisher.messages]
        assert "video.summarize" in queues

    def test_missing_job(self, deps: HandlerDeps):
        message = WorkerMessage(job_id="nonexistent", video_id="vid-1")

        handle_message(message, deps)

        assert deps.db.jobs["nonexistent"]["status"] == "failed"
        queues = [q for q, _ in deps.publisher.messages]
        assert "video.failed" in queues
        assert "video.summarize" not in queues

    def test_missing_audio_path(self, deps: HandlerDeps):
        deps.db.jobs["job-2"] = {}
        message = WorkerMessage(job_id="job-2", video_id="vid-2")

        handle_message(message, deps)

        assert deps.db.jobs["job-2"]["status"] == "failed"
        assert "no audio_path" in deps.db.jobs["job-2"]["error"]

    def test_transcriber_failure(self, deps: HandlerDeps):
        deps.transcriber = FakeTranscriber(raise_on_transcribe=True)
        deps.db.jobs["job-3"] = {"audio_path": "/tmp/test.mp3"}
        message = WorkerMessage(job_id="job-3", video_id="vid-3")

        handle_message(message, deps)

        assert deps.db.jobs["job-3"]["status"] == "failed"
        assert "transcription failed" in deps.db.jobs["job-3"]["error"]
        queues = [q for q, _ in deps.publisher.messages]
        assert "video.failed" in queues
        assert "video.summarize" not in queues
