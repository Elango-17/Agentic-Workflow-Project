from pathlib import Path

from dotenv import load_dotenv

from enterprise_agent_framework.registries.agent_registry import (
    AgentRegistry,
)
from enterprise_agent_framework.registries.tool_registry import (
    ToolRegistry,
)
from enterprise_agent_framework.runtime.agent_runtime import (
    AgentRuntime,
)

load_dotenv()

agent_registry = AgentRegistry(
    Path("agents")
)

tool_registry = ToolRegistry(
    Path("tools")
)

tool_registry.discover_tools()

runtime = AgentRuntime(
    agent_registry,
    tool_registry,
)


agent = runtime.load_agent(
    "github_pr_fetcher_v1"
)

print("Agent:")
print(agent.agent.name)

print("\nConfigured tools:")
print(agent.tools)

resolved_tools = runtime.resolve_tools(
    agent
)

print("\nResolved tools:")

for tool_id, tool in resolved_tools.items():

    print(
        tool_id,
        "->",
        type(tool).__name__
    )

print("\nTool execution test:")

try:

    result = runtime.execute_tool(
        agent,
        "get_user_stories_from_jira",
        {
            "jira_url": "https://example.com",
            "issue_type": "Story",
        },
    )

    print("Tool result:")
    print(result)

except Exception as exc:

    print("Tool execution error:")
    print(exc)