from enterprise_agent_framework.registries.tool_registry import (
    ToolRegistry,
)


registry = ToolRegistry()

registry.discover_tools()

print("Available tools:")
print(registry.list_tools())


tool = registry.get(
    "get_user_stories_from_jira"
)

print(
    "Loaded tool:",
    type(tool).__name__
)
