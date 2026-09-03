from typing import Any

from typing import Any

from agents.agent_registry import AgentRegistry
from tools.tool_registry import ToolRegistry
from agents.agent import AgentSpec


class AgentRuntime:
    """
    Runtime responsible for loading an agent,
    resolving its configured tools, and executing tools.
    """

    def __init__(
        self,
        agent_registry: AgentRegistry,
        tool_registry: ToolRegistry,
    ):
        self.agent_registry = agent_registry
        self.tool_registry = tool_registry

    def load_agent(
        self,
        identifier: str,
    ) -> AgentSpec:
        """
        Load an agent specification by ID or name.
        """

        return self.agent_registry.get(
            identifier
        )

    def resolve_tools(
        self,
        agent: AgentSpec,
    ) -> dict:
        """
        Resolve all tools configured for the agent.
        """

        resolved_tools = {}

        for tool_id in agent.tools:

            tool = self.tool_registry.get(
                tool_id
            )

            resolved_tools[tool_id] = tool

        return resolved_tools

    def execute_tool(
        self,
        agent: AgentSpec,
        tool_id: str,
        arguments: dict[str, Any],
    ) -> Any:
        """
        Execute a tool configured for the agent.
        """

        if tool_id not in agent.tools:

            raise ValueError(
                f"Tool '{tool_id}' is not configured "
                f"for agent '{agent.id}'."
            )

        tool = self.tool_registry.get(
            tool_id
        )

        if not hasattr(tool, "execute"):

            raise TypeError(
                f"Tool '{tool_id}' does not provide "
                "an execute() method."
            )

        return tool.execute(
            **arguments
        )