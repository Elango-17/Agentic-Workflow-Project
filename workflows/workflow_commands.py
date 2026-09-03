import typer
from enterprise_agent_framework.config import (
    AGENTS_DIR,
    TOOLS_DIR,
    WORKFLOWS_DIR,
)
from agents.agent_registry import AgentRegistry
from tools.tool_registry import ToolRegistry
from workflows.workflow_registry import (
    WorkflowRegistry,
)
from workflows.workflow_runtime import (
    WorkflowRuntime,
)
from workflows.workflow_crud import (
    create_workflow,
    edit_workflow,
    delete_workflow,
    list_workflows,
)
from workflows.workflow_execution import (
    execute_workflow,
)
from enterprise_agent_framework.cli.ui import (
    error,
    menu,
)


def workflow_menu():
    # -----------------------------------------
    # Registries
    # -----------------------------------------
    agents = AgentRegistry(
        AGENTS_DIR
    )
    workflows = WorkflowRegistry(
        WORKFLOWS_DIR
    )
    tools = ToolRegistry(
        TOOLS_DIR
    )
    tools.discover_tools()
    # -----------------------------------------
    # Runtime
    # -----------------------------------------
    runtime = WorkflowRuntime(
        agents,
        workflows,
        tools,
    )
    # -----------------------------------------
    # Menu
    # -----------------------------------------
    while True:
        menu(
            "Workflow Management",
            [
                "1. Create Workflow",
                "2. Edit Workflow",
                "3. Delete Workflow",
                "4. List Workflows",
                "5. Execute Workflow",
                "6. Back to Main Menu",
            ],
        )
        choice = typer.prompt(
            "Select an option"
        ).strip()
        try:
            if choice == "1":
                create_workflow(
                    agents,
                    workflows,
                )

            elif choice == "2":

                edit_workflow(
                    workflows
                )

            elif choice == "3":

                delete_workflow(
                    workflows
                )

            elif choice == "4":

                list_workflows(
                    workflows
                )

            elif choice == "5":

                execute_workflow(
                    runtime,
                    workflows,
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