import os

from llm.llm_providers.gemini_provider import GeminiProvider
from llm.llm_providers.ollama_provider import OllamaProvider
from llm.llm_providers.openai_provider import OpenAIProvider
from llm.llm_providers.anthropic_provider import AnthropicProvider

class LLMGateway:
    """
    Central gateway for interacting with the configured LLM.
    Dynamically loads the provider specified in the .env file.
    """

    def __init__(self):
        """
        Initialize the configured LLM provider strictly from .env.
        """
        provider = os.getenv("LLM_PROVIDER")
        if not provider:
            raise RuntimeError("LLM_PROVIDER is not configured in .env")
            
        provider = provider.lower()

        if provider == "gemini":
            api_key = os.getenv("GEMINI_API_KEY")
            model = os.getenv("GEMINI_MODEL")
            
            if not api_key or not model:
                raise RuntimeError("GEMINI_API_KEY or GEMINI_MODEL is not configured in .env.")
            
            self.provider = GeminiProvider(
                api_key=api_key,
                model=model,
            )

        elif provider == "ollama":
            model = os.getenv("OLLAMA_MODEL")
            host = os.getenv("OLLAMA_HOST")
            
            if not model or not host:
                raise RuntimeError("OLLAMA_MODEL or OLLAMA_HOST is not configured in .env.")
                
            self.provider = OllamaProvider(
                model=model,
                host=host,
            )

        elif provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            model = os.getenv("OPENAI_MODEL")
            
            if not api_key or not model:
                raise RuntimeError("OPENAI_API_KEY or OPENAI_MODEL is not configured in .env.")
                
            self.provider = OpenAIProvider(
                api_key=api_key,
                model=model,
            )

        elif provider == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            model = os.getenv("ANTHROPIC_MODEL")
            
            if not api_key or not model:
                raise RuntimeError("ANTHROPIC_API_KEY or ANTHROPIC_MODEL is not configured in .env.")
                
            self.provider = AnthropicProvider(
                api_key=api_key,
                model=model,
            )

        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> dict:
        return self.provider.generate_json(system_prompt, user_prompt)

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        return self.provider.generate(system_prompt, user_prompt)