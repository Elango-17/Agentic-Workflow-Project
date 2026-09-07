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
    # Contains
    # -----------------------------------------

    if " contains " in condition:

        left, right = condition.split(
            " contains ",
            1,
        )

        value = context.get(left.strip())

        expected = right.strip().strip(
            "\"'"
        )

        if value is None:
            return False

        return expected.lower() in str(
            value
        ).lower()

    # -----------------------------------------
    # Not equals
    # -----------------------------------------

    if "!=" in condition:

        left, right = condition.split(
            "!=",
            1,
        )

        value = context.get(left.strip())

        expected = right.strip().strip(
            "\"'"
        )

        return str(value) != expected

    # -----------------------------------------
    # Greater than or equal
    # -----------------------------------------

    if ">=" in condition:

        left, right = condition.split(
            ">=",
            1,
        )

        value = context.get(left.strip())

        if value is None:
            return False

        try:
            return float(value) >= float(
                right.strip()
            )

        except (TypeError, ValueError):
            raise ValueError(
                f"Condition values must be numeric: "
                f"{condition}"
            )

    # -----------------------------------------
    # Less than or equal
    # -----------------------------------------

    if "<=" in condition:

        left, right = condition.split(
            "<=",
            1,
        )

        value = context.get(left.strip())

        if value is None:
            return False

        try:
            return float(value) <= float(
                right.strip()
            )

        except (TypeError, ValueError):
            raise ValueError(
                f"Condition values must be numeric: "
                f"{condition}"
            )

    # -----------------------------------------
    # Greater than
    # -----------------------------------------

    if ">" in condition:

        left, right = condition.split(
            ">",
            1,
        )

        value = context.get(left.strip())

        if value is None:
            return False

        try:
            return float(value) > float(
                right.strip()
            )

        except (TypeError, ValueError):
            raise ValueError(
                f"Condition values must be numeric: "
                f"{condition}"
            )

    # -----------------------------------------
    # Less than
    # -----------------------------------------

    if "<" in condition:

        left, right = condition.split(
            "<",
            1,
        )

        value = context.get(left.strip())

        if value is None:
            return False

        try:
            return float(value) < float(
                right.strip()
            )

        except (TypeError, ValueError):
            raise ValueError(
                f"Condition values must be numeric: "
                f"{condition}"
            )

    # -----------------------------------------
    # Equals
    # -----------------------------------------

    if "==" in condition:

        left, right = condition.split(
            "==",
            1,
        )

        value = context.get(left.strip())

        expected = right.strip().strip(
            "\"'"
        )

        return str(value) == expected

    raise ValueError(
        f"Unsupported condition: {condition}"
    )