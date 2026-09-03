import typer

from enterprise_agent_framework.config import (
    TOOLS_DIR,
    TOOL_DEFINITIONS_DIR,
    TOOL_IMPLEMENTATIONS_DIR,
)

from tools.tool_factory import ToolFactory
from tools.tool_registry import ToolRegistry

from tools.tool_crud import (
    create_tool,
    edit_tool,
    delete_tool,
    list_tools,
)

from tools.tool_execution import (
    execute_tool,
)

from enterprise_agent_framework.llm.gateway import (
    LLMGateway,
)

from enterprise_agent_framework.cli.ui import (
    error,
    menu,
)


def tool_menu():

    # -----------------------------------------
    # Directories
    # -----------------------------------------

    TOOL_DEFINITIONS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    TOOL_IMPLEMENTATIONS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # -----------------------------------------
    # Tool Registry
    # -----------------------------------------

    registry = ToolRegistry(
        TOOLS_DIR
    )

    registry.discover_tools()

    # -----------------------------------------
    # Tool Factory
    # -----------------------------------------

    factory = ToolFactory(
        LLMGateway()
    )

    # -----------------------------------------
    # Menu
    # -----------------------------------------

    while True:

        menu(
            "Tool Management",
            [
                "1. Create Tool",
                "2. Edit Tool",
                "3. Delete Tool",
                "4. List Tools",
                "5. Execute Tool",
                "6. Back to Main Menu",
            ],
        )

        choice = typer.prompt(
            "Select an option"
        ).strip()

        try:

            if choice == "1":

                create_tool(
                    factory
                )

            elif choice == "2":

                edit_tool()

            elif choice == "3":

                delete_tool()

            elif choice == "4":

                list_tools()

            elif choice == "5":

                execute_tool(
                    registry
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