from typing import Any


def evaluate_condition(
    condition: str,
    context: dict[str, Any],
) -> bool:

    condition = condition.strip()

    if not condition:
        raise ValueError(
            "Condition cannot be empty."
        )

    # -----------------------------------------
    # contains
    # -----------------------------------------

    if " contains " in condition:

        left, right = condition.split(
            " contains ",
            1,
        )

        value = context.get(
            left.strip()
        )

        expected = right.strip().strip(
            "\"'"
        )

        if value is None:
            return False

        return expected.lower() in str(
            value
        ).lower()

    # -----------------------------------------
    # equals
    # -----------------------------------------

    if "==" in condition:

        left, right = condition.split(
            "==",
            1,
        )

        value = context.get(
            left.strip()
        )

        expected = right.strip().strip(
            "\"'"
        )

        return str(value) == expected

    # -----------------------------------------
    # not equals
    # -----------------------------------------

    if "!=" in condition:

        left, right = condition.split(
            "!=",
            1,
        )

        value = context.get(
            left.strip()
        )

        expected = right.strip().strip(
            "\"'"
        )

        return str(value) != expected

    raise ValueError(
        f"Unsupported condition: {condition}"
    )