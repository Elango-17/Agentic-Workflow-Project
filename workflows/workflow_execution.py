import typer

from workflows.workflow_registry import (
    WorkflowRegistry,
)

from workflows.workflow_crud import (
    select_workflow,
)

from workflows.workflow_runtime import (
    WorkflowRuntime,
)

from enterprise_agent_framework.cli.ui import (
    info,
    success,
)


def execute_workflow(
    runtime: WorkflowRuntime,
    workflows: WorkflowRegistry,
):

    # -----------------------------------------
    # Select Workflow
    # -----------------------------------------

    workflow = select_workflow(
        workflows
    )

    if workflow is None:
        return

    info(
        f"Executing workflow: {workflow.name}"
    )

    # -----------------------------------------
    # Input
    # -----------------------------------------

    user_input = typer.prompt(
        "Enter workflow input"
    )

    if not user_input.strip():

        raise ValueError(
            "Workflow input cannot be empty."
        )

    # -----------------------------------------
    # Execute
    # -----------------------------------------

    info(
        "Executing workflow agents..."
    )

    result = runtime.execute(
        workflow_id=workflow.id,
        user_input=user_input,
    )

    # -----------------------------------------
    # Result
    # -----------------------------------------

    success(
        "Workflow execution completed."
    )

    typer.echo(
        "\nWorkflow Result:"
    )

    typer.echo(
        result
    )

    typer.echo()