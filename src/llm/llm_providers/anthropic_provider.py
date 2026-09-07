import json
import re
from typing import Any

from anthropic import Anthropic

from llm.base import LLMProvider


class AnthropicProvider(LLMProvider):

    def __init__(self, api_key: str, model: str):
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def generate_json(
        self,
        system_prompt: str,
        user_prompt: str
    ) -> dict[str, Any]:

        response = self.client.messages.create(
            model=self.model,
            system=system_prompt,  # System prompt is a top-level parameter in Anthropic
            messages=[
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0,
            max_tokens=4096  # max_tokens is strictly required by the Anthropic API
        )

        # Anthropic returns a list of content blocks
        content = response.content[0].text

        if not content:
            raise RuntimeError("LLM returned empty response.")

        # Anthropic doesn't have a strict JSON-mode flag without a schema, 
        # so we strip markdown blocks just in case it wraps the output in ```json
        clean_text = re.sub(r"^```(?:json)?\s*", "", content, flags=re.IGNORECASE)
        clean_text = re.sub(r"\s*```$", "", clean_text).strip()

        return json.loads(clean_text)