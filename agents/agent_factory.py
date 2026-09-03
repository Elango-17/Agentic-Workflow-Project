import yaml

from enterprise_agent_framework.llm.gateway import LLMGateway
from agents.agent import AgentSpec


SYSTEM_PROMPT = """
You are an enterprise agent specification generator.

The user will describe what they want an AI agent to do.

Your job is to convert the user's requirement into a
complete AgentSpec.

Return ONLY valid JSON.

Do not return Markdown.
Do not return explanations.
Do not add extra fields.

The JSON must contain exactly:

{
    "id": "",
    "agent": {
        "name": "",
        "details": "",
        "practice_area": "",
        "good_at": ""
    },
    "behaviour": {
        "role": "",
        "goal": "",
        "back_story": "",
        "description": "",
        "expected_output": ""
    },
    "llm_configuration": {
        "model": "gpt-4o",
        "temperature": 0.7,
        "top_p": 0.9,
        "max_iteration": 10,
        "max_rpm": 60,
        "max_execution_time": 120
    },
    "tools": []
}

Rules:

1. Generate a meaningful unique snake_case ID.
2. Infer the practice area from the requirement.
3. Identify the agent's core competencies.
4. Create a professional role.
5. Define a clear goal.
6. Define a useful back story.
7. Provide a detailed description with steps in a clear way.
8. Define the expected output.
9. Do not invent tools unless explicitly requested.
10. tools should initially be [].
"""


class AgentFactory:

    def __init__(self, llm: LLMGateway):
        self.llm = llm

    def generate(
        self,
        user_requirement: str,
    ) -> AgentSpec:

        raw_response = self.llm.generate_json(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_requirement,
        )

        agent_spec = AgentSpec.model_validate(
            raw_response
        )

        return agent_spec

    @staticmethod
    def to_yaml(
        agent_spec: AgentSpec,
    ) -> str:

        return yaml.safe_dump(
            agent_spec.model_dump(),
            sort_keys=False,
            allow_unicode=True,
        )