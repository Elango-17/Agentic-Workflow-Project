from dotenv import load_dotenv

load_dotenv()

from pathlib import Path

from enterprise_agent_framework.registries.agent_registry import AgentRegistry
from enterprise_agent_framework.registries.tool_registry import ToolRegistry
from enterprise_agent_framework.runtime.crew_runtime import CrewRuntime


agent_registry = AgentRegistry(
    Path("agents")
)

tool_registry = ToolRegistry(
    Path("tools")
)

tool_registry.discover_tools()

runtime = CrewRuntime(
    agent_registry,
    tool_registry,
)


result = runtime.execute(
    identifier="github_pr_fetcher_v1",

    task_description="""
Use the GitHub PR Fetcher tool to retrieve pull requests
from the configured public GitHub repository.

Use:
- max_prs: 10
- state: all

Return the tool result directly as valid JSON.
Do not summarize.
Do not analyze.
Do not invent or modify pull request data.
After receiving the tool result, immediately provide the final answer.
""",

    expected_output="""
A valid JSON list containing the retrieved GitHub pull requests.
""",
)


print("\nCrew execution completed.")

print("\nResult:")

print(result)