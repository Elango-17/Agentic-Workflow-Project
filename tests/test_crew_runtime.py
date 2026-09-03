from pathlib import Path

from enterprise_agent_framework.registries.agent_registry import (
    AgentRegistry,
)
from enterprise_agent_framework.registries.tool_registry import (
    ToolRegistry,
)
from enterprise_agent_framework.runtime.crew_runtime import (
    CrewRuntime,
)


# --------------------------------------------------
# Create registries
# --------------------------------------------------

agent_registry = AgentRegistry(
    Path("agents")
)

tool_registry = ToolRegistry(
    Path("tools")
)


# --------------------------------------------------
# Discover tools
# --------------------------------------------------

tool_registry.discover_tools()


# --------------------------------------------------
# Create Crew Runtime
# --------------------------------------------------

runtime = CrewRuntime(
    agent_registry,
    tool_registry,
)


# --------------------------------------------------
# Build CrewAI Agent
# --------------------------------------------------

agent = runtime.build_agent(
    "github_pr_fetcher_v1"
)


# --------------------------------------------------
# Display result
# --------------------------------------------------

print("\nCrewAI agent created successfully.")

print("\nAgent role:")
print(agent.role)

print("\nAgent goal:")
print(agent.goal)

print("\nAgent backstory:")
print(agent.backstory)

print("\nConfigured CrewAI tools:")

for tool in agent.tools:
    print(
        tool.name
    )