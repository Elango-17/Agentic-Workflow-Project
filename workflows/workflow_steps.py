from typing import Any

from workflows.workflow import WorkflowStep
from workflows.workflow_context import WorkflowContext
from workflows.workflow_conditions import evaluate_condition

from runtime.crew_runtime import (
    CrewRuntime,
)


class WorkflowStepExecutor:

    def __init__(
        self,
        crew_runtime: CrewRuntime,
    ):
        self.crew_runtime = crew_runtime

    # ---------------------------------------------------------
    # EXECUTE STEP
    # ---------------------------------------------------------

    def execute(
        self,
        step: WorkflowStep,
        context: WorkflowContext,
    ) -> Any:

        context.current_step = step.id

        if step.type == "agent":
            return self._execute_agent(
                step,
                context,
            )

        if step.type == "condition":
            return self._execute_condition(
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

    # ---------------------------------------------------------
    # AGENT
    # ---------------------------------------------------------

    def _execute_agent(
        self,
        step: WorkflowStep,
        context: WorkflowContext,
    ) -> Any:

        if not step.agent:
            raise ValueError(
                f"Agent step '{step.id}' "
                "must define an agent."
            )

        result = self.crew_runtime.execute(
            identifier=step.agent,
            inputs={
                "user_input": context.user_input,
                "previous_output": context.latest_output(),
                "variables": context.variables,
            },
        )

        context.set_output(
            step.id,
            result,
        )

        return result

    # ---------------------------------------------------------
    # CONDITION
    # ---------------------------------------------------------

    def _execute_condition(
        self,
        step: WorkflowStep,
        context: WorkflowContext,
    ) -> str:

        if not step.condition:
            raise ValueError(
                f"Condition step '{step.id}' "
                "must define a condition."
            )

        condition_context = {
            **context.variables,
            "user_input": context.user_input,
            "latest_output": context.latest_output(),
        }

        result = evaluate_condition(
            step.condition,
            condition_context,
        )

        if result:
            next_step = step.if_true

        else:
            next_step = step.if_false

        context.set_output(
            step.id,
            result,
        )

        return next_step

    # ---------------------------------------------------------
    # LOOP
    # ---------------------------------------------------------

    def _execute_loop(
        self,
        step: WorkflowStep,
        context: WorkflowContext,
    ) -> Any:

        if not step.agent:
            raise ValueError(
                f"Loop step '{step.id}' "
                "must define an agent."
            )

        if not step.max_iterations:
            raise ValueError(
                f"Loop step '{step.id}' "
                "must define max_iterations."
            )

        results = []

        for iteration in range(
            step.max_iterations
        ):

            context.iteration = iteration + 1

            result = self.crew_runtime.execute(
                identifier=step.agent,
                inputs={
                    "user_input": context.user_input,
                    "previous_output": context.latest_output(),
                    "variables": context.variables,
                    "iteration": context.iteration,
                },
            )

            results.append(result)

            context.set_output(
                step.id,
                result,
            )

        return results