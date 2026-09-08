import typer

from agents.agent_registry import AgentRegistry

from utils.editor import (
    open_in_editor,
)

from utils.slug import (
    slugify,
)

from cli.ui import (
    info,
    success,
)

from workflows.workflow_selection import (
    select_practice_area,
    select_good_at,
)

from workflows.workflow import (
    WorkflowSpec,
)
from workflows.workflow_registry import (
    WorkflowRegistry,
)
from workflows.workflow_builder import (
    WorkflowBuilder,
)


def create_workflow(
    agents: AgentRegistry,
    workflows: WorkflowRegistry,
):

    # -----------------------------------------
    # Workflow Information
    # -----------------------------------------

    name = typer.prompt(
        "Workflow Name"
    )

    description = typer.prompt(
        "Description"
    )

    practice_area = select_practice_area()

    good_at = select_good_at()

    # -----------------------------------------
    # Build Execution Plan
    # -----------------------------------------

    builder = WorkflowBuilder(
        agents
    )

    execution = builder.build()

    # -----------------------------------------
    # Collect Agent IDs
    # -----------------------------------------

    agent_ids = []

    for step in execution.steps:

        if (
            step.agent
            and step.agent not in agent_ids
        ):
            agent_ids.append(
                step.agent
            )

    # -----------------------------------------
    # Validate Agents
    # -----------------------------------------

    if not agent_ids:

        raise ValueError(
            "Workflow must contain at least one agent."
        )

    # -----------------------------------------
    # Create Workflow Specification
    # -----------------------------------------

    spec = WorkflowSpec(
        id=slugify(name),
        name=name,
        description=description,
        practice_area=practice_area,
        good_at=good_at,
        agents=agent_ids,
        execution=execution,
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

    # -----------------------------------------
    # Open Workflow
    # -----------------------------------------

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