import typer


def select_guardrails() -> list[str]:
    typer.echo("\nGuardrails Configuration\n")

    guardrails = [
        "input_validation",
        "output_validation",
        "prompt_injection_protection",
        "sensitive_data_protection",
    ]

    typer.echo("Available Guardrails:\n")

    for index, guardrail in enumerate(guardrails, start=1):
        typer.echo(f"{index}. {guardrail}")

    typer.echo("\nEnter guardrail numbers separated by commas.")
    typer.echo("Press Enter to skip guardrails.")

    selection = typer.prompt(
        "Select guardrails",
        default=""
    ).strip()

    if not selection:
        return []

    selected_guardrails = []

    for value in selection.split(","):
        value = value.strip()

        if not value.isdigit():
            raise ValueError(
                f"Invalid guardrail selection: {value}"
            )

        index = int(value)

        if index < 1 or index > len(guardrails):
            raise ValueError(
                f"Invalid guardrail selection: {index}"
            )

        guardrail = guardrails[index - 1]

        if guardrail not in selected_guardrails:
            selected_guardrails.append(guardrail)

    return selected_guardrails