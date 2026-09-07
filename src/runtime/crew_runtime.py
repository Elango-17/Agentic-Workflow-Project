import os
import json
import re
from typing import Any, Optional

from crewai import Crew, Process, Task, LLM

from agents.agent_registry import AgentRegistry
from tools.tool_registry import ToolRegistry
from agents.agent_runtime import AgentRuntime

from runtime.crewai_adapter import (
    CrewAIRuntimeAdapter,
)

from runtime.crew_tool_adapter import (
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

    # =========================================================
    # BUILD AGENT
    # =========================================================

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

    # =========================================================
    # LLM
    # =========================================================

    def _create_llm(self):
        provider = os.getenv("LLM_PROVIDER")
        if not provider:
            raise RuntimeError("LLM_PROVIDER is not configured in .env")
        
        provider = provider.lower()

        if provider == "gemini":
            api_key = os.getenv("GEMINI_API_KEY")
            model = os.getenv("GEMINI_MODEL")
            
            if not api_key or not model:
                raise RuntimeError("GEMINI_API_KEY or GEMINI_MODEL is not configured in .env.")
            
            # Ensure the gemini/ prefix is present for CrewAI native integration
            if not model.startswith("gemini/"):
                model = f"gemini/{model}"
                
            return LLM(
                model=model,
                api_key=api_key,
            )

        elif provider == "ollama":
            model = os.getenv("OLLAMA_MODEL")
            base_url = os.getenv("OLLAMA_HOST")
            
            if not model or not base_url:
                raise RuntimeError("OLLAMA_MODEL or OLLAMA_HOST is not configured in .env.")
                
            return LLM(
                model=f"ollama/{model}",
                base_url=base_url,
            )

        elif provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            model = os.getenv("OPENAI_MODEL")
            
            if not api_key or not model:
                raise RuntimeError("OPENAI_API_KEY or OPENAI_MODEL is not configured in .env.")
            
            # Ensure the openai/ prefix is present
            if not model.startswith("openai/"):
                model = f"openai/{model}"
                
            return LLM(
                model=model,
                api_key=api_key,
            )

        elif provider == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            model = os.getenv("ANTHROPIC_MODEL")
            
            if not api_key or not model:
                raise RuntimeError("ANTHROPIC_API_KEY or ANTHROPIC_MODEL is not configured in .env.")
            
            # Ensure the anthropic/ prefix is present
            if not model.startswith("anthropic/"):
                model = f"anthropic/{model}"
                
            return LLM(
                model=model,
                api_key=api_key,
            )

        else:
            raise ValueError(f"Unsupported LLM provider configured in .env: {provider}")

    # =========================================================
    # EXECUTE AGENT
    # =========================================================

    def execute(
        self,
        identifier: str,
        task_description: Optional[str] = None,
        expected_output: Optional[str] = None,
        inputs: Optional[dict] = None,
        llm: Optional[Any] = None,
    ) -> Any:
        
        # 1. Load the agent spec to get access to the YAML properties
        agent_spec = self.agent_runtime.load_agent(identifier)

        agent = self.build_agent(
            identifier,
            llm=llm,
        )

        # 2. Use the YAML description if available, otherwise fallback
        if task_description is None:
            if hasattr(agent_spec.behaviour, "description") and agent_spec.behaviour.description:
                task_description = agent_spec.behaviour.description
            else:
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

        # 3. Use the YAML expected_output if available, otherwise fallback
        if expected_output is None:
            if hasattr(agent_spec.behaviour, "expected_output") and agent_spec.behaviour.expected_output:
                expected_output = agent_spec.behaviour.expected_output
            else:
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

        # -----------------------------------------------------
        # Execute CrewAI
        # -----------------------------------------------------

        result = crew.kickoff()

        # -----------------------------------------------------
        # Normalize structured JSON output
        # -----------------------------------------------------

        if (
            hasattr(result, "json_dict")
            and result.json_dict
        ):
            return result.json_dict

        # -----------------------------------------------------
        # Fallback: Strip markdown and parse JSON manually
        # -----------------------------------------------------
        raw_text = result.raw if hasattr(result, "raw") else str(result)
        
        # Remove ```json at the start and ``` at the end
        clean_text = re.sub(r"^```(?:json)?\s*", "", raw_text, flags=re.IGNORECASE)
        clean_text = re.sub(r"\s*```$", "", clean_text).strip()

        try:
            # If it's valid JSON, return it as a dictionary
            return json.loads(clean_text)
        except Exception:
            # If parsing fails, return the raw text
            return raw_text