import sys
import json
from dotenv import load_dotenv
from enterprise_agent_framework.config import (
    AGENTS_DIR,
    TOOLS_DIR,
)
from agents.agent_registry import AgentRegistry
from tools.tool_registry import ToolRegistry
from enterprise_agent_framework.runtime.crew_runtime import (
    CrewRuntime,
)


def main():

    load_dotenv()

    # -----------------------------------------
    # Agent ID
    # -----------------------------------------

    if len(sys.argv) < 2:

        print(
            "Usage: "
            "python -m enterprise_agent_framework.app <agent_id>"
        )

        return

    agent_id = sys.argv[1]

    # -----------------------------------------
    # Runtime input
    # -----------------------------------------

    print("\nEnter input JSON.")
    print("Press Enter if no input is required.")
    print("> ", end="")

    user_input = input().strip()
    if user_input:
        try:
            inputs = json.loads(user_input)
        except json.JSONDecodeError as exc:
            print(
                f"\nInvalid JSON input: {exc}"
            )
            return
    else:
        inputs = {}
    # -----------------------------------------
    # Registries
    # -----------------------------------------
    agent_registry = AgentRegistry(
        AGENTS_DIR
    )
    tool_registry = ToolRegistry(
        TOOLS_DIR
    )
    tool_registry.discover_tools()

    # -----------------------------------------
    # Runtime
    # -----------------------------------------
    runtime = CrewRuntime(
        agent_registry,
        tool_registry,
    )
    # -----------------------------------------
    # Execute agent
    # -----------------------------------------
    result = runtime.execute(
        identifier=agent_id,
        inputs=inputs,
    )
    # -----------------------------------------
    # Result
    # -----------------------------------------
    print("\n===================================")
    print("Execution Completed")
    print("===================================\n")
    print(result)

if __name__ == "__main__":
    main()