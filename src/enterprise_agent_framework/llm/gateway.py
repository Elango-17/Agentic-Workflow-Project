import os

from enterprise_agent_framework.llm.gemini_provider import (
    GeminiProvider,
)


class LLMGateway:

    def __init__(self):

        provider = os.getenv(
            "LLM_PROVIDER",
            "gemini",
        ).lower()

        if provider == "gemini":

            api_key = os.getenv(
                "GEMINI_API_KEY"
            )

            if not api_key:
                raise RuntimeError(
                    "GEMINI_API_KEY is not configured."
                )

            self.provider = GeminiProvider(
                api_key=api_key,
                model=os.getenv(
                    "GEMINI_MODEL",
                    "gemini-3.5-flash-lite",
                ),
            )

        else:

            raise ValueError(
                f"Unsupported LLM provider: {provider}"
            )

    def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> dict:

        return self.provider.generate_json(
            system_prompt,
            user_prompt,
        )

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:

        return self.provider.generate(
            system_prompt,
            user_prompt,
        )



# import os

# from enterprise_agent_framework.llm.ollama_provider import (
#     OllamaProvider,
# )


# class LLMGateway:
#     """
#     Central gateway for interacting with the configured LLM.

#     Currently, the framework uses Ollama with a locally
#     running Qwen3 model.
#     """

#     def __init__(self):
#         """
#         Initialize the configured LLM provider.
#         """

#         provider = os.getenv(
#             "LLM_PROVIDER",
#             "ollama",
#         ).lower()

#         if provider == "ollama":

#             self.provider = OllamaProvider(
#                 model=os.getenv(
#                     "OLLAMA_MODEL",
#                     "qwen3:8b",
#                 ),
#                 host=os.getenv(
#                     "OLLAMA_HOST",
#                     "http://localhost:11434",
#                 ),
#             )

#         else:

#             raise ValueError(
#                 f"Unsupported LLM provider: {provider}"
#             )

#     def generate_json(
#         self,
#         system_prompt: str,
#         user_prompt: str,
#     ) -> dict:
#         """
#         Generate a structured JSON response using
#         the configured LLM provider.
#         """

#         return self.provider.generate_json(
#             system_prompt,
#             user_prompt,
#         )

#     def generate(
#         self,
#         system_prompt: str,
#         user_prompt: str,
#     ) -> str:
#         """
#         Generate a normal text response using
#         the configured LLM provider.
#         """

#         return self.provider.generate(
#             system_prompt,
#             user_prompt,
#         )