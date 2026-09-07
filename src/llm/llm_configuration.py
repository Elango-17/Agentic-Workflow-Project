import os

import typer


LLM_PROVIDERS = [
    "gemini",
    "ollama",
    "openai",
    "anthropic",
]


LLM_MODEL_ENV_VARS = {
    "gemini": "GEMINI_MODEL",
    "ollama": "OLLAMA_MODEL",
    "openai": "OPENAI_MODEL",
    "anthropic": "ANTHROPIC_MODEL",
}


def select_llm_provider() -> str:

    typer.echo("\nLLM Configuration\n")
    typer.echo("Available LLM Providers:\n")

    for index, provider in enumerate(
        LLM_PROVIDERS,
        start=1,
    ):
        typer.echo(
            f"{index}. {provider.capitalize()}"
        )

    choice = typer.prompt(
        "Select LLM provider",
        type=int,
    )

    if choice < 1 or choice > len(LLM_PROVIDERS):
        raise ValueError(
            "Invalid LLM provider selection."
        )

    return LLM_PROVIDERS[choice - 1]


def get_model_for_provider(
    provider: str,
) -> str:

    env_variable = LLM_MODEL_ENV_VARS.get(
        provider
    )

    if not env_variable:
        raise ValueError(
            f"Unsupported LLM provider: {provider}"
        )

    model = os.getenv(
        env_variable
    )

    if not model:
        raise RuntimeError(
            f"{env_variable} is not configured in .env"
        )

    return model