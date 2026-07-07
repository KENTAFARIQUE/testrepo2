import json
from typing import Dict, Any, List, Tuple, Optional

import pytest
from tubedigest.contracts import WorkerMessage

from workers.tags.handler import handle_message, HandlerDeps


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


class FakeTagger:
    def __init__(self, raise_on_generate: bool = False):
        self._raise = raise_on_generate

    def generate_tags_and_chapters(self, transcript: str, summary: str) -> Dict[str, Any]:
        if self._raise:
            raise RuntimeError("tags generation failed")
        return {
            "tags": ["ai", "tutorial"],
            "chapters": [{"start": "00:00", "title": "Intro"}],
        }


@pytest.fixture
def deps():
    db = FakeDb()
    publisher = FakePublisher()
    tagger = FakeTagger()
    return HandlerDeps(db=db, publisher=publisher, tagger=tagger)


class TestTagsHandler:
    def test_happy_path(self, deps: HandlerDeps):
        deps.db.jobs["job-1"] = {
            "transcript": "some transcript",
            "summary": "some summary",
        }
        message = WorkerMessage(job_id="job-1", video_id="vid-1")

        handle_message(message, deps)

        job = deps.db.jobs["job-1"]
        assert job["status"] == "completed"
        assert json.loads(job["tags"]) == ["ai", "tutorial"]
        assert json.loads(job["chapters"]) == [{"start": "00:00", "title": "Intro"}]

    def test_missing_job(self, deps: HandlerDeps):
        message = WorkerMessage(job_id="nonexistent", video_id="vid-1")

        handle_message(message, deps)

        assert deps.db.jobs["nonexistent"]["status"] == "failed"
        queues = [q for q, _ in deps.publisher.messages]
        assert "video.failed" in queues

    def test_missing_transcript(self, deps: HandlerDeps):
        deps.db.jobs["job-2"] = {"summary": "some summary"}
        message = WorkerMessage(job_id="job-2", video_id="vid-2")

        handle_message(message, deps)

        assert deps.db.jobs["job-2"]["status"] == "failed"
        assert "no transcript" in deps.db.jobs["job-2"]["error"]

    def test_missing_summary(self, deps: HandlerDeps):
        deps.db.jobs["job-3"] = {"transcript": "some transcript"}
        message = WorkerMessage(job_id="job-3", video_id="vid-3")

        handle_message(message, deps)

        assert deps.db.jobs["job-3"]["status"] == "failed"
        assert "no summary" in deps.db.jobs["job-3"]["error"]

    def test_tagger_failure(self, deps: HandlerDeps):
        deps.tagger = FakeTagger(raise_on_generate=True)
        deps.db.jobs["job-4"] = {
            "transcript": "some transcript",
            "summary": "some summary",
        }
        message = WorkerMessage(job_id="job-4", video_id="vid-4")

        handle_message(message, deps)

        assert deps.db.jobs["job-4"]["status"] == "failed"
        assert "tags generation failed" in deps.db.jobs["job-4"]["error"]
        queues = [q for q, _ in deps.publisher.messages]
        assert "video.failed" in queues
