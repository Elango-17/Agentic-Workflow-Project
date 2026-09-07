from typing import Any

from crewai.tools import BaseTool as CrewAIBaseTool
from pydantic import create_model


class CrewAIToolAdapter(CrewAIBaseTool):
    """
    Adapter that converts an Enterprise Agent Framework
    tool into a CrewAI-compatible tool.
    """

    framework_tool: Any

    def __init__(
        self,
        framework_tool: Any,
        name: str,
        description: str,
        args_schema: type,
    ):
        super().__init__(
            framework_tool=framework_tool,
            name=name,
            description=description,
            args_schema=args_schema,
        )

    def _run(self, **kwargs: Any) -> Any:
        """
        Execute the underlying framework tool.
        """

        return self.framework_tool.execute(**kwargs)


def create_tool_schema(tool_spec):
    """
    Create a Pydantic input schema dynamically from ToolSpec.
    """

    fields = {}

    for input_spec in tool_spec.inputs:

        python_type = {

            "str": str,
            "string": str,
            "int": int,
            "integer": int,
            "float": float,
            "bool": bool,
            "boolean": bool,
            "list": list,
            "dict": dict,
            "object": dict,
        }.get(
           input_spec.type.lower(),
            str,
        )

        default = (
            ...
            if input_spec.required
            else None
        )

        fields[input_spec.name] = (
            python_type,
            default,
        )

    return create_model(
        f"{tool_spec.name.replace(' ', '')}Input",
        **fields,
    )