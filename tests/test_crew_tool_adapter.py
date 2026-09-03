from pathlib import Path

from enterprise_agent_framework.registries.tool_registry import (
    ToolRegistry,
)
from enterprise_agent_framework.runtime.crew_tool_adapter import (
    CrewAIToolAdapter,
    create_tool_schema,
)


tool_registry = ToolRegistry(
    Path("tools")
)

tool_registry.discover_tools()

tool_spec = tool_registry.get_spec(
    "fetch_workitems_from_ado"
)

tool = tool_registry.get(
    "github_pr_fetcher_v1"
)

args_schema = create_tool_schema(
    tool_spec
)

crew_tool = CrewAIToolAdapter(
    framework_tool=tool,
    name=tool_spec.name,
    description=tool_spec.description,
    args_schema=args_schema,
)

print("Framework tool:")
print(type(tool).__name__)

print("\nCrewAI tool:")
print(crew_tool.name)

print("\nCrewAI description:")
print(crew_tool.description)

print("\nCrewAI args schema:")
print(crew_tool.args_schema)

print("\nAdapter created successfully.")