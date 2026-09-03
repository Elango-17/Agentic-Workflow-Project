import typer
from agents.agent_factory import AgentFactory
from agents.agent_registry import AgentRegistry
from enterprise_agent_framework.utils.editor import open_in_editor
from enterprise_agent_framework.cli.ui import (
    info,
    success,
)


def create_agent(
    factory: AgentFactory,
    registry: AgentRegistry,
):
    requirement = typer.prompt(
        "Describe what the agent should do"
    )
    if not requirement.strip():
        raise ValueError(
            "Description cannot be empty."
        )
    info(
        "Generating AgentSpec..."
    )
    spec = factory.generate(
        requirement
    )
    path = registry.save(
        spec
    )
    success(
        f"Agent created: {path}"
    )
    if open_in_editor(path):
        info(
            "Agent file opened in editor."
        )
    else:
        info(
            f"Edit manually: {path}"
        )


def list_agents(
    registry: AgentRegistry,
):
    agents = registry.list_agents()
    if not agents:
        info(
            "No agents found."
        )
        return []

    typer.echo(
        "\nAvailable Agents:"
    )
    for index, agent in enumerate(
        agents,
        start=1,
    ):
        typer.echo(
            f"{index}. {agent.agent.name}"
        )

    typer.echo()
    return agents


def select_agent(
    registry: AgentRegistry,
):
    agents = list_agents(
        registry
    )
    if not agents:
        return None
    choice = typer.prompt(
        "Select an agent",
        type=int,
    )
    if choice < 1 or choice > len(agents):
        raise ValueError(
            "Invalid agent selection."
        )
    return agents[
        choice - 1
    ]

def edit_agent(
    registry: AgentRegistry,
):
    agent = select_agent(
        registry
    )
    if agent is None:
        return
    path = registry.path_for(
        agent.id
    )
    if open_in_editor(path):
        info(
            "Agent file opened in editor."
        )
    else:
        info(
            f"File: {path}"
        )

def delete_agent(
    registry: AgentRegistry,
):
    agent = select_agent(
        registry
    )
    if agent is None:
        return
    path = registry.path_for(
        agent.id
    )
    if not typer.confirm(
        f"Delete '{agent.agent.name}'?"
    ):
        info("Deletion cancelled.")
        return
    
    registry.delete(
        agent.id
    )
    success(
        f"Agent deleted successfully: {path.name}"
    )