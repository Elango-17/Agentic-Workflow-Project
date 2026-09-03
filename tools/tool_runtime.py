from typing import Any
from tools.tool_registry import ToolRegistry


class ToolRuntime:
    """
    Runtime responsible for resolving and executing tools.
    """

    def __init__(self, tool_registry: ToolRegistry):
        self.tool_registry = tool_registry

    def execute(
        self,
        tool_id: str,
        arguments: dict[str, Any],
    ) -> Any:
        """
        Resolve a tool from the registry and execute it
        with the provided arguments.
        """

        tool = self.tool_registry.get(tool_id)

        if not hasattr(tool, "execute"):
            raise TypeError(
                f"Tool '{tool_id}' does not provide "
                "an execute() method."
            )

        return tool.execute(**arguments)