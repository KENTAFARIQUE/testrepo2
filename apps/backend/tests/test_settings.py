from tubedigest.settings import Settings


class TestSettings:
    def test_default_values(self):
        s = Settings()
        assert s.app_env == "development"
        assert s.use_fake_models is True
        assert s.max_video_duration_seconds == 180

    def test_can_override(self):
        s = Settings(app_env="production", max_video_duration_seconds=300)
        assert s.app_env == "production"
        assert s.max_video_duration_seconds == 300
