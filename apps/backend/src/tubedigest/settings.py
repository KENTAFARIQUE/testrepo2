from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = "sqlite+aiosqlite:///./data/tubedigest.db"
    rabbitmq_url: str = "amqp://guest:guest@rabbitmq:5672/"
    groq_api_key: str = ""
    groq_transcribe_model: str = "whisper-large-v3-turbo"
    groq_llm_model: str = "llama-3.1-8b-instant"
    use_fake_download: bool = True
    use_fake_media: bool = True
    use_fake_models: bool = True
    use_fake_publisher: bool = False
    max_video_duration_seconds: int = 180
    cors_origins: str = "http://localhost:5173"
    storage_root: str = "/app/storage"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
