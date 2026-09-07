import typer

#selection modules
from src.llm.llm_configuration import (
    select_llm_provider,
    get_model_for_provider,
)
from tools.tool_selection import (
    select_tools,
    select_tools_for_edit,
)
from kb.kb_selection import select_kbs
from guardrails.guardrail_selection import select_guardrails

from tools.tool_registry import ToolRegistry
from agents.agent_factory import AgentFactory
from agents.agent_registry import AgentRegistry
from utils.editor import open_in_editor
from cli.ui import (
    info,
    success,
)


def create_agent(
    factory: AgentFactory,
    registry: AgentRegistry,
    tool_registry: ToolRegistry
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

    # LLM
    provider = select_llm_provider()
    model = get_model_for_provider(
        provider
    )
    # Apply LLM configuration
    spec.llm_configuration.provider = provider
    spec.llm_configuration.model = model

    # Tools
    selected_tools = select_tools(tool_registry)
    spec.tools = selected_tools

    # Knowledge Base
    selected_kbs = select_kbs()
    spec.kb = selected_kbs

    # Guardrails
    selected_guardrails = select_guardrails()
    spec.guardrails = selected_guardrails


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
    tool_registry: ToolRegistry,
):
    agent = select_agent(
        registry
    )
    if agent is None:
        return

    # LLM
    provider = select_llm_provider()
    model = get_model_for_provider(
        provider
    )

    agent.llm_configuration.provider = provider
    agent.llm_configuration.model = model

    # Tools
    selected_tools = select_tools_for_edit(
        tool_registry,
        current_tools=agent.tools,
    )
    agent.tools = selected_tools

    # Knowledge Base
    selected_kbs = select_kbs()
    agent.kb = selected_kbs

    # Guardrails
    selected_guardrails = select_guardrails()
    agent.guardrails = selected_guardrails

    path = registry.save(
        agent
    )
    success(
        f"Agent updated: {path}"
    )

    if open_in_editor(path):
        info(
            "Agent file opened in editor."
        )
    else:
        info(
            f"Edit manually: {path}"
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