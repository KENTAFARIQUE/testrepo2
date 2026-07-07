from tubedigest.contracts import WorkerMessage
from tubedigest.publisher import FakePublisher


class TestFakePublisher:
    async def test_stores_published_message(self):
        pub = FakePublisher()
        msg = WorkerMessage(job_id="j1", video_id="v1")
        await pub.publish("video.download", msg)
        assert len(pub.published_messages) == 1
        queue, stored = pub.published_messages[0]
        assert queue == "video.download"
        assert stored.job_id == "j1"
        assert stored.video_id == "v1"

    async def test_stores_multiple_messages_in_order(self):
        pub = FakePublisher()
        await pub.publish("video.download", WorkerMessage(job_id="j1", video_id="v1"))
        await pub.publish("video.transcribe", WorkerMessage(job_id="j2", video_id="v2"))
        assert len(pub.published_messages) == 2
        assert pub.published_messages[0][0] == "video.download"
        assert pub.published_messages[1][0] == "video.transcribe"

    async def test_reset_clears_messages(self):
        pub = FakePublisher()
        await pub.publish("video.download", WorkerMessage(job_id="j1", video_id="v1"))
        pub.reset()
        assert pub.published_messages == []

    async def test_publish_with_worker_message_serialization(self):
        pub = FakePublisher()
        msg = WorkerMessage(job_id="j1", video_id="v1", attempt=2, url="https://example.com")
        await pub.publish("video.download", msg)
        _, stored = pub.published_messages[0]
        assert stored.attempt == 2
        assert stored.url == "https://example.com"
