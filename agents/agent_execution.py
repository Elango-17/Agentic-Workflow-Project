import json
import typer
from agents.agent_registry import AgentRegistry
from agents.agent_crud import select_agent
from src.runtime.crew_runtime import (
    CrewRuntime,
)

from cli.ui import (
    info,
    success,
)


def execute_agent(
    runtime: CrewRuntime,
    registry: AgentRegistry,
):
    # -----------------------------------------
    # Select Agent
    # -----------------------------------------

    agent = select_agent(
        registry
    )

    if agent is None:
        return

    info(
        f"Executing agent: {agent.agent.name}"
    )

    # -----------------------------------------
    # Input
    # -----------------------------------------

    user_input = typer.prompt(
        "Enter agent input"
    )

    if not user_input.strip():
        raise ValueError(
            "Agent input cannot be empty."
        )

    # -----------------------------------------
    # Parse JSON
    # -----------------------------------------

    try:
        inputs = json.loads(
            user_input
        )

    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON input: {exc}"
        )

    # -----------------------------------------
    # Execute
    # -----------------------------------------

    info(
        "Executing agent..."
    )

    result = runtime.execute(
        identifier=agent.id,
        inputs=inputs,
    )

    # -----------------------------------------
    # Result
    # -----------------------------------------

    success(
        "Agent execution completed."
    )

    typer.echo(
        "\nAgent Result:"
    )

    typer.echo(
        result
    )

    typer.echo()