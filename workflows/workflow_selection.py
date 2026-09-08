import typer


PRACTICE_AREAS = [
    "Testing",
    "AI/ML",
    "API & Integration",
    "Backend Engineering",
    "Business Operations",
    "Cloud & DevOps",
    "Cross-Functional",
    "Data Engineering",
    "Experience Design",
    "Legacy Modernization",
    "Product Management",
    "Quality Engineering",
    "Security & Compliance",
    "UI Engineering",
]


GOOD_AT_OPTIONS = [
    "instruction",
    "monitoring",
    "refactor",
    "qa",
    "scheduling",
    "validation",
    "parser",
    "orchestration",
    "automation",
    "retrieval and parser",
    "retrieval",
    "UX-testing",
    "conversion",
    "generation",
    "exporter",
    "summarization",
    "embedding",
    "regex-filter",
    "classification",
    "review",
    "integration",
]


def select_practice_area() -> str:
    typer.echo("\nPractice Area\n")

    for index, practice_area in enumerate(
        PRACTICE_AREAS,
        start=1,
    ):
        typer.echo(
            f"{index}. {practice_area}"
        )

    choice = typer.prompt(
        "Select Practice Area",
        default="1",
    ).strip()

    if not choice:
        return "Testing"

    if not choice.isdigit():
        raise ValueError(
            "Practice Area selection must be a number."
        )

    index = int(choice)

    if index < 1 or index > len(PRACTICE_AREAS):
        raise ValueError(
            "Invalid Practice Area selection."
        )

    return PRACTICE_AREAS[index - 1]


def select_good_at() -> list[str]:
    typer.echo("\nGood At\n")

    for index, option in enumerate(
        GOOD_AT_OPTIONS,
        start=1,
    ):
        typer.echo(
            f"{index}. {option}"
        )

    typer.echo(
        "\nEnter multiple numbers separated by commas."
    )

    selection = typer.prompt(
        "Select Good At",
        default="",
    ).strip()

    if not selection:
        return []

    selected = []

    for value in selection.split(","):

        value = value.strip()

        if not value.isdigit():
            raise ValueError(
                f"Invalid Good At selection: {value}"
            )

        index = int(value)

        if index < 1 or index > len(GOOD_AT_OPTIONS):
            raise ValueError(
                f"Invalid Good At selection: {index}"
            )

        option = GOOD_AT_OPTIONS[index - 1]

        if option not in selected:
            selected.append(option)

    return selected