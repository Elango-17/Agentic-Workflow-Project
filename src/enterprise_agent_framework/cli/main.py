import typer
from rich.console import Console
from enterprise_agent_framework.cli.ui import (
    error,
    menu,
)
console = Console()
from agents.agent_commands import agent_menu
from tools.tool_commands import tool_menu
from workflows.workflow_commands import workflow_menu


def main_menu():

    typer.echo("=============================================================")
    typer.echo("          Hello User!! What will you create today?")
    typer.echo("Build, manage, and execute AI agents, tools, and workflows.")
    typer.echo("=============================================================")

    while True:
        console.print(
"""
Main Menu

1. Agent
2. Workflow
3. Tool
4. Exit
======================================================
"""
        )

        choice = typer.prompt(
            "Select an option"
        ).strip()

        try:

            if choice == "1":

                agent_menu()

            elif choice == "2":
                workflow_menu()

            elif choice == "3":
                tool_menu()

            elif choice == "4":

                typer.echo("Exiting...")
                return

            else:

                error(
                    "Please select 1, 2, 3, or 4."
                )

        except Exception as exc:
            error(str(exc))

        except typer.Abort:
            typer.secho(
                "\nAborted!",
                fg=typer.colors.RED,
            )


if __name__ == "__main__":
    main_menu()