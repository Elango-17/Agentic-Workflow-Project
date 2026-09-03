import yaml

from enterprise_agent_framework.llm.gateway import LLMGateway
from workflows.workflow import WorkflowSpec


SYSTEM_PROMPT = """
You are an enterprise workflow specification generator.

The user will describe what they want a multi-agent
workflow to accomplish.

Your job is to convert the requirement into a complete
WorkflowSpec.

Return ONLY valid JSON.

Do not return Markdown.
Do not return explanations.
Do not add extra fields.

The JSON must contain exactly:

{
    "id": "",
    "name": "",
    "description": "",
    "practice_area": "",
    "good_at": "",
    "agents": []
}

Rules:

1. Generate a meaningful unique snake_case ID.
2. Generate a clear workflow name.
3. Generate a professional workflow description.
4. Infer the practice area.
5. Describe what the workflow is good at.
6. The agents list must contain agent IDs.
7. Do not invent agent IDs.
8. Use only agent IDs provided by the application.
"""


class WorkflowFactory:

    def __init__(self, llm: LLMGateway):
        self.llm = llm

    def generate(
        self,
        user_requirement: str,
        available_agents: list[str],
    ) -> WorkflowSpec:

        user_prompt = f"""
Workflow Requirement:

{user_requirement}

Available Agent IDs:

{available_agents}

Select agents only from the available Agent IDs.
"""

        raw_response = self.llm.generate_json(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )

        workflow_spec = WorkflowSpec.model_validate(
            raw_response
        )

        return workflow_spec

    @staticmethod
    def to_yaml(
        workflow_spec: WorkflowSpec,
    ) -> str:

        return yaml.safe_dump(
            workflow_spec.model_dump(),
            sort_keys=False,
            allow_unicode=True,
        )