import json
from typing import Protocol, Dict, Any


class Tagger(Protocol):
    def generate_tags_and_chapters(self, transcript: str, summary: str) -> Dict[str, Any]: ...


class FakeTagger:
    def generate_tags_and_chapters(self, transcript: str, summary: str) -> Dict[str, Any]:
        return {
            "tags": ["technology", "tutorial", "review"],
            "chapters": [
                {"start": "00:00", "title": "Introduction"},
                {"start": "01:30", "title": "Main Content"},
            ],
        }


class GroqTagger:
    def __init__(self, api_key: str, model: str = "llama-3.1-8b-instant"):
        self._api_key = api_key
        self._model = model

    def generate_tags_and_chapters(self, transcript: str, summary: str) -> Dict[str, Any]:
        from groq import Groq

        client = Groq(api_key=self._api_key)
        completion = client.chat.completions.create(
            model=self._model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a content analysis assistant. Given a video transcript "
                        "and summary, generate:\n"
                        "1. A list of 3-5 relevant tags (keywords)\n"
                        "2. A list of chapters with start time and title\n\n"
                        "Return valid JSON with keys 'tags' (list of strings) and "
                        "'chapters' (list of objects with 'start' and 'title'). "
                        "Example:\n"
                        '{"tags": ["ai", "tutorial"], '
                        '"chapters": [{"start": "00:00", "title": "Intro"}]}'
                    ),
                },
                {
                    "role": "user",
                    "content": f"Transcript: {transcript}\n\nSummary: {summary}",
                },
            ],
            response_format={"type": "json_object"},
        )
        return json.loads(completion.choices[0].message.content or "{}")
