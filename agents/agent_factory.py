import yaml

from src.llm.gateway import LLMGateway
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
        "model": "gemini",
        "temperature": 0.1,
        "top_p": 0.9,
        "max_iteration": 30,
        "max_rpm": 60,
        "max_execution_time": 500
    },
    "tools": [],
    "agent_skills": [],
    "kb": [],
    "guardrails": [],
    "prompt": [],
    "input_format": [],
    "output_format": []
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
11. Populate agent_skills with the skills required by the agent.
12. kb should initially be [].
13. Populate prompt as a list of arrays.
    Each prompt must be represented as its own array containing
    one or more prompt instruction strings.

    Correct:
    "prompt": [
        ["Fetch user stories from Jira."],
        ["Validate that each story contains an ID and summary."]
    ]

    Incorrect:
    "prompt": [
        "Fetch user stories from Jira.",
        "Validate that each story contains an ID and summary."
    ]
14. Populate input_file with the types of files the agent expects as input.
15. Populate input_data with the expected input structure.
16. Populate output_data with the expected output structure.
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