from typing import Any

from crewai import Crew, Process, Task

from agents.agent_registry import AgentRegistry
from tools.tool_registry import ToolRegistry

from workflows.workflow_registry import WorkflowRegistry

from enterprise_agent_framework.runtime.crew_runtime import (
    CrewRuntime,
)


class WorkflowRuntime:

    def __init__(
        self,
        agent_registry: AgentRegistry,
        workflow_registry: WorkflowRegistry,
        tool_registry: ToolRegistry,
    ):

        self.agent_registry = agent_registry
        self.workflow_registry = workflow_registry

        self.crew_runtime = CrewRuntime(
            agent_registry,
            tool_registry,
        )

    def execute(
        self,
        workflow_id: str,
        user_input: str,
    ) -> Any:

        workflow = self.workflow_registry.get(
            workflow_id
        )

        if not user_input.strip():
            raise ValueError(
                "Workflow input cannot be empty."
            )

        agents = []
        tasks = []

        for index, agent_id in enumerate(
            workflow.agents
        ):

            agent = self.crew_runtime.build_agent(
                agent_id
            )

            agents.append(agent)

            task = self._build_task(
                workflow,
                agent_id,
                agent,
                index,
                user_input,
                tasks,
            )

            tasks.append(task)

        return self._execute_crew(
            agents,
            tasks,
        )

    def _build_task(
        self,
        workflow,
        agent_id: str,
        agent,
        index: int,
        user_input: str,
        previous_tasks: list,
    ):

        agent_spec = self.agent_registry.get(
            agent_id
        )

        description = (
            f"{agent_spec.behaviour.description}\n\n"
            f"Workflow: {workflow.name}\n"
            f"Workflow Description: "
            f"{workflow.description}\n\n"
            f"Practice Area: "
            f"{workflow.practice_area}\n\n"
        )

        if index == 0:

            description += (
                "Analyze the following workflow input:\n\n"
                f"{user_input}"
            )

            context = None

        else:

            description += (
                "Analyze and process the output "
                "from the previous workflow agent."
            )

            context = previous_tasks[-1:]

        return Task(
            description=description,
            expected_output=(
                agent_spec.behaviour.expected_output
            ),
            agent=agent,
            context=context,
        )

    def _execute_crew(
        self,
        agents,
        tasks,
    ):

        crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
        )

        return crew.kickoff()