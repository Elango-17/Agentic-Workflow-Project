import ast
import typer
from enterprise_agent_framework.config import (
    TOOL_DEFINITIONS_DIR,
    TOOL_IMPLEMENTATIONS_DIR,
)
from tools.tool_factory import ToolFactory
from enterprise_agent_framework.utils.editor import open_in_editor
from enterprise_agent_framework.utils.slug import slugify
from enterprise_agent_framework.cli.ui import (
    info,
    success,
)


def create_tool(factory: ToolFactory):

    description = typer.prompt(
        "Enter your tool requirements / functional description"
    )

    if not description.strip():
        raise ValueError(
            "Description cannot be empty."
        )

    info(
        "Generating tool specification..."
    )

    tool_spec = factory.generate(
        description
    )

    # -----------------------------------------
    # Definition YAML
    # -----------------------------------------

    definition_path = (
        TOOL_DEFINITIONS_DIR
        / f"{slugify(tool_spec.id)}.yaml"
    )

    # -----------------------------------------
    # Python implementation
    # -----------------------------------------

    info(
        "Generating and syntax-validating Python..."
    )

    code = factory.generate_implementation(
        tool_spec
    )

    implementation_path = (
        TOOL_IMPLEMENTATIONS_DIR
        / tool_spec.implementation_file
    )

    if implementation_path.exists():

        if not typer.confirm(
            f"{implementation_path.name} exists. Overwrite?"
        ):
            info("Creation cancelled.")
            return

    # -----------------------------------------
    # Validate generated Python
    # -----------------------------------------

    ast.parse(
        code,
        filename=str(implementation_path),
    )

    # -----------------------------------------
    # Save YAML definition
    # -----------------------------------------

    definition_path.write_text(
        factory.to_yaml(tool_spec),
        encoding="utf-8",
    )

    # -----------------------------------------
    # Save Python implementation
    # -----------------------------------------

    implementation_path.write_text(
        code.rstrip() + "\n",
        encoding="utf-8",
    )

    success(
        f"Tool definition created: {definition_path}"
    )

    success(
        f"Tool implementation created: {implementation_path}"
    )


def find_tool(name):

    implementation_path = (
        TOOL_IMPLEMENTATIONS_DIR
        / f"{slugify(name)}.py"
    )

    if implementation_path.is_file():
        return implementation_path

    for path in TOOL_IMPLEMENTATIONS_DIR.glob("*.py"):

        if path.stem.lower() == name.lower():
            return path

    raise FileNotFoundError(
        f"Tool '{name}' was not found."
    )


def edit_tool():

    path = select_tool()

    if path is None:
        return

    info(
        "Opened in editor."
        if open_in_editor(path)
        else f"File: {path}"
    )


def delete_tool():

    path = select_tool()

    if path is None:
        return

    definition_path = (
        TOOL_DEFINITIONS_DIR
        / f"{path.stem}.yaml"
    )

    if not typer.confirm(
        f"Delete tool '{path.stem}'?"
    ):
        info(
            "Deletion cancelled."
        )
        return

    path.unlink()

    if definition_path.exists():
        definition_path.unlink()

    success(
        f"Tool deleted successfully: {path.stem}"
    )


def list_tools():

    tools = list(
        TOOL_IMPLEMENTATIONS_DIR.glob("*.py")
    )

    if not tools:
        info(
            "No tools found."
        )
        return []
    typer.echo(
        "\nAvailable Tools:"
    )
    for index, tool in enumerate(
        tools,
        start=1,
    ):
        typer.echo(
            f"{index}. {tool.stem}"
        )
    typer.echo()
    return tools


def select_tool():
    tools = list_tools()
    if not tools:
        return None
    choice = typer.prompt(
        "Select a tool",
        type=int,
    )
    if choice < 1 or choice > len(tools):
        raise ValueError(
            "Invalid tool selection."
        )
    return tools[
        choice - 1
    ]