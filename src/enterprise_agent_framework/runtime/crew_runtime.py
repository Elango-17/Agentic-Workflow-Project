import os
from typing import Any, Optional
from crewai import Crew, Process, Task, LLM

from agents.agent_registry import AgentRegistry
from tools.tool_registry import ToolRegistry
from agents.agent_runtime import AgentRuntime
from enterprise_agent_framework.runtime.crewai_adapter import CrewAIRuntimeAdapter
from enterprise_agent_framework.runtime.crew_tool_adapter import (
    CrewAIToolAdapter,
    create_tool_schema,
)


class CrewRuntime:

    def __init__(
        self,
        agent_registry: AgentRegistry,
        tool_registry: ToolRegistry,
    ):
        self.agent_runtime = AgentRuntime(
            agent_registry,
            tool_registry,
        )

        self.tool_registry = tool_registry

        self.crewai_adapter = CrewAIRuntimeAdapter()

    def build_agent(
        self,
        identifier: str,
        llm: Optional[Any] = None,
    ):
        agent_spec = self.agent_runtime.load_agent(
            identifier
        )

        framework_tools = self.agent_runtime.resolve_tools(
            agent_spec
        )

        crew_tools = []

        for tool_id, framework_tool in framework_tools.items():

            tool_spec = self.tool_registry.get_spec(
                tool_id
            )

            args_schema = create_tool_schema(
                tool_spec
            )

            crew_tool = CrewAIToolAdapter(
                framework_tool=framework_tool,
                name=tool_spec.name,
                description=tool_spec.description,
                args_schema=args_schema,
            )

            crew_tools.append(
                crew_tool
            )

        if llm is None:
            llm = self._create_llm()

        return self.crewai_adapter.build_agent(
            agent_spec,
            tools=crew_tools,
            llm=llm,
        )

    def _create_llm(self):

        api_key = os.getenv(
            "GEMINI_API_KEY"
        )
        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured."
            )
        return LLM(
            model="gemini/gemini-3.5-flash-lite",
            api_key=api_key,
        )

    # def _create_llm(self):
    #     model = os.getenv(
    #         "OLLAMA_MODEL",
    #         "qwen3:8b",
    #     )

    #     base_url = os.getenv(
    #         "OLLAMA_HOST",
    #         "http://localhost:11434",
    #     )

    #     return LLM(
    #         model=f"ollama/{model}",
    #         base_url=base_url,
    #     )

    def execute(
        self,
        identifier: str,
        task_description: Optional[str] = None,
        expected_output: Optional[str] = None,
        inputs: Optional[dict] = None,
        llm: Optional[Any] = None,
    ) -> Any:

        agent = self.build_agent(
            identifier,
            llm=llm,
        )

        if task_description is None:
            task_description = (
                "Execute the configured agent task "
                "using the provided input."
            )

        if inputs:
            task_description = (
                f"{task_description}\n\n"
                f"Runtime Input:\n"
                f"{inputs}"
            )

        if expected_output is None:
            expected_output = (
                "Return the result as valid JSON."
            )

        task = Task(
            description=task_description,
            expected_output=expected_output,
            agent=agent,
        )

        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True,
        )

        return crew.kickoff()