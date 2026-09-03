import json
from typing import Any

from google import genai

from enterprise_agent_framework.llm.base import LLMProvider


class GeminiProvider(LLMProvider):

    def __init__(
        self,
        api_key: str,
        model: str,
    ):
        self.client = genai.Client(
            api_key=api_key
        )

        self.model = model

    def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> dict[str, Any]:

        response = self.client.models.generate_content(
            model=self.model,
            contents=user_prompt,
            config={
                "system_instruction": system_prompt,
                "temperature": 0,
                "response_mime_type": "application/json",
            },
        )

        content = response.text

        if not content:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        try:
            return json.loads(content)

        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "Gemini returned invalid JSON."
            ) from exc

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:

        response = self.client.models.generate_content(
            model=self.model,
            contents=user_prompt,
            config={
                "system_instruction": system_prompt,
                "temperature": 0,
            },
        )

        content = response.text

        if not content:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return content