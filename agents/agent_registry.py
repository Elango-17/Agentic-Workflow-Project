from pathlib import Path
import yaml

from enterprise_agent_framework.exceptions import ArtifactNotFoundError
from agents.agent import AgentSpec


class AgentRegistry:

    def __init__(self, directory: Path):
        self.directory = directory

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ---------------------------------------------------------
    # SAVE
    # ---------------------------------------------------------

    def save(self, spec: AgentSpec):

        path = self.directory / f"{spec.id}.yaml"

        path.write_text(
            yaml.safe_dump(
                spec.model_dump(),
                sort_keys=False,
                allow_unicode=True,
            ),
            encoding="utf-8",
        )

        return path

    # ---------------------------------------------------------
    # GET
    # ---------------------------------------------------------

    def get(self, identifier: str):

        for path in self.directory.glob("*.yaml"):

            try:

                spec = AgentSpec.model_validate(
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
                    spec.agent.name.lower()
                    == identifier.lower()
                ):
                    return spec

            except Exception:
                continue

        raise ArtifactNotFoundError(
            f"Agent '{identifier}' was not found."
        )

    # ---------------------------------------------------------
    # LIST
    # ---------------------------------------------------------

    def list_agents(self):

        agents = []

        for path in self.directory.glob("*.yaml"):

            try:

                spec = AgentSpec.model_validate(
                    yaml.safe_load(
                        path.read_text(
                            encoding="utf-8"
                        )
                    )
                )

                agents.append(spec)

            except Exception:
                continue

        return agents

    # ---------------------------------------------------------
    # PATH
    # ---------------------------------------------------------

    def path_for(self, identifier: str):

        return (
            self.directory
            / f"{self.get(identifier).id}.yaml"
        )

    # ---------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------

    def delete(self, identifier: str):

        path = self.path_for(
            identifier
        )

        path.unlink()

        return path