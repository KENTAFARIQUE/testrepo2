from typing import Protocol


class Summarizer(Protocol):
    def summarize(self, transcript: str) -> str: ...


class FakeSummarizer:
    def summarize(self, transcript: str) -> str:
        return "This is a fake summary for testing purposes."


class GroqSummarizer:
    def __init__(self, api_key: str, model: str = "llama-3.1-8b-instant"):
        self._api_key = api_key
        self._model = model

    def summarize(self, transcript: str) -> str:
        from groq import Groq

        client = Groq(api_key=self._api_key)
        completion = client.chat.completions.create(
            model=self._model,
            messages=[
                {
                    "role": "system",
                    "content": "Summarize the following YouTube video transcript "
                    "in 3-5 sentences. Focus on the main points.",
                },
                {"role": "user", "content": transcript},
            ],
        )
        return completion.choices[0].message.content or ""
