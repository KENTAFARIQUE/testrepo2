from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from tubedigest.contracts import (
    Chapter,
    CreateVideoRequest,
    JobStatus,
    VideoJobResponse,
    WorkerMessage,
)


class TestJobStatus:
    def test_all_values_are_valid(self):
        values = [
            "queued",
            "downloading",
            "downloaded",
            "extracting_audio",
            "generating_thumbnail",
            "transcribing",
            "summarizing",
            "generating_tags",
            "completed",
            "failed",
        ]
        for v in values:
            assert JobStatus(v) is not None

    def test_rejects_invalid(self):
        with pytest.raises(ValueError):
            JobStatus("invalid_status")


class TestChapter:
    def test_valid(self):
        ch = Chapter(start="00:00", title="Intro")
        assert ch.start == "00:00"
        assert ch.title == "Intro"

    def test_rejects_empty_start(self):
        with pytest.raises(ValidationError):
            Chapter(start="", title="Intro")

    def test_rejects_empty_title(self):
        with pytest.raises(ValidationError):
            Chapter(start="00:00", title="")


class TestCreateVideoRequest:
    def test_valid(self):
        req = CreateVideoRequest(url="https://youtube.com/watch?v=test")
        assert req.url == "https://youtube.com/watch?v=test"

    def test_rejects_empty_url(self):
        with pytest.raises(ValidationError):
            CreateVideoRequest(url="")

    def test_rejects_missing_url(self):
        with pytest.raises(ValidationError):
            CreateVideoRequest()


class TestVideoJobResponse:
    NOW = datetime.now(timezone.utc)

    def test_minimal(self):
        job = VideoJobResponse(
            id="abc-123",
            url="https://youtube.com/watch?v=test",
            created_at=self.NOW,
            updated_at=self.NOW,
        )
        assert job.id == "abc-123"
        assert job.status == JobStatus.queued
        assert job.current_step == "queued"
        assert job.tags == []
        assert job.chapters == []

    def test_full(self):
        job = VideoJobResponse(
            id="abc-123",
            url="https://youtube.com/watch?v=test",
            title="Test Video",
            status=JobStatus.completed,
            current_step="completed",
            video_path="/storage/videos/test.mp4",
            audio_path="/storage/audio/test.mp3",
            thumbnail_path="/storage/thumbnails/test.jpg",
            transcript="Hello world",
            summary="A test video",
            tags=["test", "demo"],
            chapters=[Chapter(start="00:00", title="Intro")],
            created_at=self.NOW,
            updated_at=self.NOW,
        )
        assert job.title == "Test Video"
        assert job.tags == ["test", "demo"]
        assert len(job.chapters) == 1

    def test_rejects_missing_id(self):
        with pytest.raises(ValidationError):
            VideoJobResponse(
                url="https://youtube.com/watch?v=test",
                created_at=self.NOW,
                updated_at=self.NOW,
            )

    def test_rejects_invalid_status(self):
        with pytest.raises(ValidationError):
            VideoJobResponse(
                id="abc-123",
                url="https://youtube.com/watch?v=test",
                status="invalid",
                created_at=self.NOW,
                updated_at=self.NOW,
            )


class TestWorkerMessage:
    def test_minimal(self):
        msg = WorkerMessage(job_id="j1", video_id="v1")
        assert msg.job_id == "j1"
        assert msg.video_id == "v1"
        assert msg.attempt == 1
        assert msg.url is None

    def test_with_url(self):
        msg = WorkerMessage(
            job_id="j1",
            video_id="v1",
            url="https://youtube.com/watch?v=test",
        )
        assert msg.url == "https://youtube.com/watch?v=test"

    def test_with_attempt(self):
        msg = WorkerMessage(job_id="j1", video_id="v1", attempt=3)
        assert msg.attempt == 3

    def test_rejects_missing_job_id(self):
        with pytest.raises(ValidationError):
            WorkerMessage(video_id="v1")

    def test_rejects_missing_video_id(self):
        with pytest.raises(ValidationError):
            WorkerMessage(job_id="j1")
