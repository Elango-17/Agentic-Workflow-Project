from typing import Any
from workflows.workflow import WorkflowStep

class WorkflowStepExecutor:
    def __init__(
        self,
        runtime,
    ):
        self.runtime = runtime

    def execute_step(
        self,
        step: WorkflowStep,
        context: dict[str, Any],
    ) -> Any:

        if step.type == "agent":
            return self._execute_agent(
                step,
                context,
            )

        if step.type == "condition":
            return self._evaluate_condition(
                step,
                context,
            )

        if step.type == "loop":
            return self._execute_loop(
                step,
                context,
            )

        raise ValueError(
            f"Unsupported workflow step type: {step.type}"
        )

    def _execute_agent(
        self,
        step: WorkflowStep,
        context: dict[str, Any],
    ) -> Any:

        if not step.agent:
            raise ValueError(
                f"Agent step '{step.id}' requires an agent."
            )

        return self.runtime.execute(
            identifier=step.agent,
            inputs=context,
        )

    def _evaluate_condition(
        self,
        step: WorkflowStep,
        context: dict[str, Any],
    ) -> bool:

        if not step.condition:
            raise ValueError(
                f"Condition step '{step.id}' requires a condition."
            )

        return bool(
            context.get(
                step.condition,
                False,
            )
        )

    def _execute_loop(
        self,
        step: WorkflowStep,
        context: dict[str, Any],
    ) -> list[Any]:

        if not step.next:
            raise ValueError(
                f"Loop step '{step.id}' requires a next step."
            )

        max_iterations = (
            step.max_iterations or 1
        )

        results = []

        for _ in range(max_iterations):

            result = self.runtime.execute(
                identifier=step.next,
                inputs=context,
            )

            results.append(result)

            context["last_result"] = result

        return results