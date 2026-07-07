import os
from typing import Protocol


class Transcriber(Protocol):
    def transcribe(self, audio_path: str) -> str: ...


class FakeTranscriber:
    def transcribe(self, audio_path: str) -> str:
        return "This is a fake transcript for testing purposes."


class GroqTranscriber:
    def __init__(self, api_key: str, model: str = "whisper-large-v3-turbo"):
        self._api_key = api_key
        self._model = model

    def transcribe(self, audio_path: str) -> str:
        from groq import Groq

        client = Groq(api_key=self._api_key)
        with open(audio_path, "rb") as f:
            translation = client.audio.transcriptions.create(
                file=(os.path.basename(audio_path), f),
                model=self._model,
                response_format="text",
            )
        return translation
