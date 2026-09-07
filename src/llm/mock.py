from llm.base import LLMProvider
from utils.slug import slugify
class MockLLMProvider(LLMProvider):
    def generate_json(self, system_prompt: str, user_prompt: str):
        if "agent specification" in system_prompt.lower():
            name = "Generated Analysis Agent"
            return {"id": slugify(name), "agent": {"name": name, "details": "Generated enterprise analysis agent.", "practice_area": "Software Engineering", "good_at": "Analysis, classification, structured reasoning"}, "behaviour": {"role": "Software Analysis Specialist", "goal": user_prompt, "back_story": "An experienced enterprise software analyst.", "description": user_prompt, "expected_output": "Structured analysis with evidence and confidence."}, "llm_configuration": {"model": "gpt-4o", "temperature": 0.7, "top_p": 0.9, "max_iteration": 10, "max_rpm": 60, "max_execution_time": 120}, "tools": []}
        return {"tool_name": "generated_tool", "code": '"""Generated tool."""\n\ndef execute(input_data: object) -> dict:\n    """Implement the requested functionality here."""\n    return {"status": "not_implemented", "input": input_data}\n'}
