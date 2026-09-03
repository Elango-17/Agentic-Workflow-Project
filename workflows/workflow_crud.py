import typer
from agents.agent_registry import AgentRegistry
from enterprise_agent_framework.config import (
    AGENTS_DIR,
    WORKFLOWS_DIR,
)
from enterprise_agent_framework.utils.editor import (
    open_in_editor,
)
from enterprise_agent_framework.utils.slug import (
    slugify,
)
from enterprise_agent_framework.cli.ui import (
    info,
    success,
)
from workflows.workflow import WorkflowSpec
from workflows.workflow_registry import WorkflowRegistry

def create_workflow(
    agents: AgentRegistry,
    workflows: WorkflowRegistry,
):

    name = typer.prompt(
        "Workflow Name"
    )

    description = typer.prompt(
        "Description"
    )

    practice_area = typer.prompt(
        "Practice Area"
    )

    good_at = typer.prompt(
        "Good At"
    )

    count = typer.prompt(
        "Number of agents required",
        type=int,
    )

    if count < 1:
        raise ValueError(
            "Number of agents must be at least 1."
        )

    # -----------------------------------------
    # Get Available Agents
    # -----------------------------------------

    agent_ids = []

    available_agents = agents.list_agents()

    if not available_agents:
        raise ValueError(
            "No agents found. Create at least one agent first."
        )

    typer.echo(
        "\nAvailable Agents:"
    )

    for index, agent in enumerate(
        available_agents,
        start=1,
    ):
        typer.echo(
            f"{index}. {agent.agent.name}"
        )

    typer.echo()

    # -----------------------------------------
    # Select Agents
    # -----------------------------------------

    for index in range(1, count + 1):

        choice = typer.prompt(
            f"{index}. Select Agent",
            type=int,
        )

        if (
            choice < 1
            or choice > len(available_agents)
        ):
            raise ValueError(
                "Invalid agent selection."
            )

        selected_agent = available_agents[
            choice - 1
        ]

        agent_ids.append(
            selected_agent.id
        )

    # -----------------------------------------
    # Create Workflow
    # -----------------------------------------

    spec = WorkflowSpec(
        id=slugify(name),
        name=name,
        description=description,
        practice_area=practice_area,
        good_at=good_at,
        agents=agent_ids,
    )

    # -----------------------------------------
    # Save Workflow
    # -----------------------------------------

    path = workflows.save(
        spec
    )

    success(
        f"Workflow created: {path}"
    )

    if open_in_editor(path):

        info(
            "Workflow file opened in editor."
        )

    else:

        info(
            f"Edit manually: {path}"
        )

def select_workflow(
    workflows: WorkflowRegistry,
):

    workflow_list = (
        workflows.list_workflows()
    )

    if not workflow_list:

        info(
            "No workflows found."
        )

        return None

    typer.echo(
        "\nAvailable Workflows:"
    )

    for index, workflow in enumerate(
        workflow_list,
        start=1,
    ):

        typer.echo(
            f"{index}. {workflow.name}"
        )

    choice = typer.prompt(
        "Select a workflow",
        type=int,
    )

    if (
        choice < 1
        or choice > len(workflow_list)
    ):

        raise ValueError(
            "Invalid workflow selection."
        )

    return workflow_list[
        choice - 1
    ]

def edit_workflow(
    workflows: WorkflowRegistry,
):

    workflow = select_workflow(
        workflows
    )

    if workflow is None:
        return

    path = workflows.path_for(
        workflow.id
    )

    if open_in_editor(path):

        info(
            "Workflow file opened in editor."
        )

    else:

        info(
            f"File: {path}"
        )

def delete_workflow(
    workflows: WorkflowRegistry,
):

    workflow = select_workflow(
        workflows
    )

    if workflow is None:
        return

    path = workflows.path_for(
        workflow.id
    )

    if not typer.confirm(
        f"Delete '{workflow.name}'?"
    ):

        info(
            "Deletion cancelled."
        )

        return

    workflows.delete(
        workflow.id
    )

    success(
        f"Workflow deleted successfully: "
        f"{path.name}"
    )


def list_workflows(
    workflows: WorkflowRegistry,
):

    workflow_list = (
        workflows.list_workflows()
    )

    if not workflow_list:

        info(
            "No workflows found."
        )

        return

    typer.echo(
        "\nAvailable Workflows:"
    )

    for index, workflow in enumerate(
        workflow_list,
        start=1,
    ):

        typer.echo(
            f"{index}. {workflow.name}"
        )

    typer.echo()