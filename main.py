import typer
from rich.console import Console

from src.cli.docker_runner import run_docker
from src.cli.hosting import select_hosting
from agents.agent_commands import agent_menu
from tools.tool_commands import tool_menu
from workflows.workflow_commands import workflow_menu
from src.cli.ui import error
from src.cli.greeting import get_welcome_message


console = Console()


def main_menu():
    typer.echo(get_welcome_message())

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

        except typer.Abort:

            typer.secho(
                "\nAborted!",
                fg=typer.colors.RED,
            )

        except Exception as exc:

            error(str(exc))


def main():

    hosting = select_hosting()

    if hosting == "exit":
        typer.echo("Exiting...")
        return

    if hosting == "python":
        main_menu()

    elif hosting == "docker":
        run_docker()


if __name__ == "__main__":
    main()