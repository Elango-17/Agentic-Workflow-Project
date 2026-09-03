import json
import typer

from tools.tool_registry import ToolRegistry

from enterprise_agent_framework.cli.ui import (
    info,
    success,
)


def execute_tool(
    registry: ToolRegistry,
):

    # -----------------------------------------
    # Select Tool
    # -----------------------------------------

    tool_id = select_tool(
        registry
    )

    if tool_id is None:
        return

    info(
        f"Executing tool: {tool_id}"
    )

    # -----------------------------------------
    # Input
    # -----------------------------------------

    user_input = typer.prompt(
        "Enter tool input JSON"
    )

    if not user_input.strip():

        raise ValueError(
            "Tool input cannot be empty."
        )

    # -----------------------------------------
    # Validate JSON
    # -----------------------------------------

    try:

        arguments = json.loads(
            user_input
        )

    except json.JSONDecodeError as exc:

        raise ValueError(
            f"Invalid JSON input: {exc}"
        )

    if not isinstance(
        arguments,
        dict,
    ):

        raise ValueError(
            "Tool input must be a JSON object."
        )

    # -----------------------------------------
    # Load Tool
    # -----------------------------------------

    tool = registry.get(
        tool_id
    )

    # -----------------------------------------
    # Execute
    # -----------------------------------------

    info(
        "Executing tool..."
    )

    if not hasattr(
        tool,
        "execute",
    ):

        raise TypeError(
            f"Tool '{tool_id}' does not "
            "provide an execute() method."
        )

    result = tool.execute(
        **arguments
    )

    # -----------------------------------------
    # Result
    # -----------------------------------------

    success(
        "Tool execution completed."
    )

    typer.echo(
        "\nTool Result:"
    )

    typer.echo(
        result
    )

    typer.echo()


def select_tool(
    registry: ToolRegistry,
):

    # -----------------------------------------
    # Discover Tools
    # -----------------------------------------

    registry.discover_tools()

    tools = registry.list_tools()

    if not tools:

        info(
            "No tools found."
        )

        return None

    # -----------------------------------------
    # Display Tools
    # -----------------------------------------

    typer.echo(
        "\nAvailable Tools:"
    )

    for index, tool_id in enumerate(
        tools,
        start=1,
    ):

        try:

            spec = registry.get_spec(
                tool_id
            )

            display_name = spec.name

        except Exception:

            display_name = tool_id

        typer.echo(
            f"{index}. {display_name}"
        )

    typer.echo()

    # -----------------------------------------
    # Select Tool
    # -----------------------------------------

    choice = typer.prompt(
        "Select a tool",
        type=int,
    )

    if (
        choice < 1
        or choice > len(tools)
    ):

        raise ValueError(
            "Invalid tool selection."
        )

    return tools[
        choice - 1
    ]