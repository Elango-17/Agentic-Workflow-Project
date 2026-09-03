import json
from typing import Any

from ollama import Client

from enterprise_agent_framework.llm.base import LLMProvider


class OllamaProvider(LLMProvider):

    def __init__(
        self,
        model: str = "qwen3:8b",
        host: str = "http://localhost:11434",
    ):
        self.model = model
        self.client = Client(host=host)

    def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> dict[str, Any]:

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            format="json",
        )

        content = response["message"]["content"]

        if not content:
            raise RuntimeError(
                "Ollama returned an empty response."
            )

        try:
            return json.loads(content)

        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "Ollama returned invalid JSON."
            ) from exc

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        """
        Generate a normal text response from Ollama.
        """

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        content = response["message"]["content"]

        if not content:
            raise RuntimeError(
                "Ollama returned an empty response."
            )

        return content