from tubedigest.contracts.queues import (
    QUEUE_VIDEO_DOWNLOAD,
    QUEUE_VIDEO_AUDIO_EXTRACT,
    QUEUE_VIDEO_THUMBNAIL_GENERATE,
    QUEUE_VIDEO_TRANSCRIBE,
    QUEUE_VIDEO_SUMMARIZE,
    QUEUE_VIDEO_TAGS,
    QUEUE_VIDEO_FAILED,
    ALL_QUEUES,
)


class TestQueueConstants:
    def test_values_match_pipeline_doc(self):
        assert QUEUE_VIDEO_DOWNLOAD == "video.download"
        assert QUEUE_VIDEO_AUDIO_EXTRACT == "video.audio.extract"
        assert QUEUE_VIDEO_THUMBNAIL_GENERATE == "video.thumbnail.generate"
        assert QUEUE_VIDEO_TRANSCRIBE == "video.transcribe"
        assert QUEUE_VIDEO_SUMMARIZE == "video.summarize"
        assert QUEUE_VIDEO_TAGS == "video.tags"
        assert QUEUE_VIDEO_FAILED == "video.failed"

    def test_all_queues_seven_values(self):
        assert len(ALL_QUEUES) == 7

    def test_all_queues_no_duplicates(self):
        assert len(ALL_QUEUES) == len(set(ALL_QUEUES))

    def test_all_queues_contains_each_queue(self):
        expected = {
            QUEUE_VIDEO_DOWNLOAD,
            QUEUE_VIDEO_AUDIO_EXTRACT,
            QUEUE_VIDEO_THUMBNAIL_GENERATE,
            QUEUE_VIDEO_TRANSCRIBE,
            QUEUE_VIDEO_SUMMARIZE,
            QUEUE_VIDEO_TAGS,
            QUEUE_VIDEO_FAILED,
        }
        assert set(ALL_QUEUES) == expected
