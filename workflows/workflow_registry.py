from pathlib import Path

import yaml

from exceptions import (
    ArtifactNotFoundError,
)

from workflows.workflow import WorkflowSpec


class WorkflowRegistry:

    def __init__(
        self,
        directory: Path,
    ):
        self.directory = directory

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def save(
        self,
        spec: WorkflowSpec,
    ):

        path = (
            self.directory
            / f"{spec.id}.yaml"
        )

        path.write_text(
            yaml.safe_dump(
                spec.model_dump(exclude_none=True),
                sort_keys=False,
                allow_unicode=True,
            ),
            encoding="utf-8",
        )

        return path

    def get(
        self,
        identifier: str,
    ):

        for path in self.directory.glob("*.yaml"):

            try:

                spec = WorkflowSpec.model_validate(
                    yaml.safe_load(
                        path.read_text(
                            encoding="utf-8"
                        )
                    )
                )

                if (
                    spec.id.lower()
                    == identifier.lower()
                    or
                    spec.name.lower()
                    == identifier.lower()
                ):
                    return spec

            except Exception:
                continue

        raise ArtifactNotFoundError(
            f"Workflow '{identifier}' was not found."
        )

    def list_workflows(self):

        workflows = []

        for path in self.directory.glob("*.yaml"):

            try:

                spec = WorkflowSpec.model_validate(
                    yaml.safe_load(
                        path.read_text(
                            encoding="utf-8"
                        )
                    )
                )

                workflows.append(spec)

            except Exception:
                continue

        return workflows

    def path_for(
        self,
        identifier: str,
    ):

        return (
            self.directory
            / f"{self.get(identifier).id}.yaml"
        )

    def delete(
        self,
        identifier: str,
    ):

        path = self.path_for(
            identifier
        )

        path.unlink()

        return path