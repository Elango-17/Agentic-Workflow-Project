from rich.console import Console
from rich.panel import Panel

console = Console()


def header():
    console.print()
    console.print(
        Panel.fit(
            "[bold cyan]Hello User!! What will you create today?[/bold cyan]\n\n"
            "1. Agent\n"
            "2. Workflow\n"
            "3. Tool\n"
            "4. Exit",
            title="Enterprise Agent Framework",
            border_style="cyan",
        )
    )
    console.print()


def menu(title, items):
    console.print()
    console.print(f"[bold]{title}[/bold]")
    console.print()

    for item in items:
        console.print(item)

    console.print()


def success(message):
    console.print()
    console.print(f"[green]✓ {message}[/green]")
    console.print()


def error(message):
    console.print()
    console.print(f"[red]✗ {message}[/red]")
    console.print()


def info(message):
    console.print()
    console.print(f"[cyan]• {message}[/cyan]")
    console.print()