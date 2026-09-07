import typer
from agents.agent_factory import AgentFactory
from agents.agent_registry import AgentRegistry
from agents.agent_crud import (
    create_agent,
    edit_agent,
    delete_agent,
    list_agents,
)
from agents.agent_execution import (
    execute_agent,
)
from tools.tool_registry import ToolRegistry
from config import (
    AGENTS_DIR,
    TOOLS_DIR,
)
from llm.gateway import (
    LLMGateway,
)
from runtime.crew_runtime import (
    CrewRuntime,
)
from cli.ui import (
    error,
    menu,
)


def agent_menu():
    # -----------------------------------------
    # Registries
    # -----------------------------------------
    agent_registry = AgentRegistry(
        AGENTS_DIR
    )
    tool_registry = ToolRegistry(
        TOOLS_DIR
    )
    tool_registry.discover_tools()
    # -----------------------------------------
    # Agent Factory
    # -----------------------------------------
    factory = AgentFactory(
        LLMGateway()
    )
    # -----------------------------------------
    # Runtime
    # -----------------------------------------
    runtime = CrewRuntime(
        agent_registry,
        tool_registry,
    )
    # -----------------------------------------
    # Menu
    # -----------------------------------------
    while True:
        menu(
            "Agent Management",
            [
                "1. Create Agent",
                "2. Edit Agent",
                "3. Delete Agent",
                "4. List Agents",
                "5. Execute Agent",
                "6. Back to Main Menu",
            ],
        )
        choice = typer.prompt(
            "Select an option"
        ).strip()
        try:
            if choice == "1":
                create_agent(
                    factory,
                    agent_registry,
                    tool_registry
                )

            elif choice == "2":
                edit_agent(
                    agent_registry,
                    tool_registry
                )

            elif choice == "3":
                delete_agent(
                    agent_registry
                )

            elif choice == "4":
                list_agents(
                    agent_registry
                )

            elif choice == "5":
                execute_agent(
                    runtime,
                    agent_registry,
                )

            elif choice == "6":
                return

            else:
                error(
                    "Please select 1, 2, 3, 4, 5, or 6."
                )

        except Exception as exc:

            error(
                str(exc)
            )