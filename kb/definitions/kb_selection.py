import typer


def select_kbs() -> list[str]:
    typer.echo("\nKnowledge Base Configuration\n")

    typer.echo("Available Knowledge Bases:\n")

    # Prototype KBs
    knowledge_bases = [
        "jira_knowledge_base",
        "github_knowledge_base",
        "testing_knowledge_base",
    ]

    for index, kb in enumerate(knowledge_bases, start=1):
        typer.echo(f"{index}. {kb}")

    typer.echo("\nEnter KB numbers separated by commas.")
    typer.echo("Press Enter to skip KBs.")

    selection = typer.prompt(
        "Select knowledge bases",
        default=""
    ).strip()

    if not selection:
        return []

    selected_kbs = []

    for value in selection.split(","):
        value = value.strip()

        if not value.isdigit():
            raise ValueError(
                f"Invalid KB selection: {value}"
            )

        index = int(value)

        if index < 1 or index > len(knowledge_bases):
            raise ValueError(
                f"Invalid KB selection: {index}"
            )

        kb = knowledge_bases[index - 1]

        if kb not in selected_kbs:
            selected_kbs.append(kb)

    return selected_kbs