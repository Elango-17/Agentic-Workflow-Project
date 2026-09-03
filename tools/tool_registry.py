import importlib.util
import inspect

from pathlib import Path
from typing import Type

import yaml

from tools.base import BaseTool
from tools.tool import ToolSpec


class ToolRegistry:
    """
    Discovers and manages framework tools.

    Tool definitions are stored as YAML files under:
        tools/definitions/

    Tool implementations are stored as Python files under:
        tools/implementations/
    """

    def __init__(
        self,
        tools_directory: Path | str = "tools",
    ):
        self.tools_directory = Path(tools_directory)

        self.definitions_directory = (
            self.tools_directory / "definitions"
        )

        self.implementations_directory = (
            self.tools_directory / "implementations"
        )

        self._tools: dict[str, Type[BaseTool]] = {}
        self._specs: dict[str, ToolSpec] = {}

    # ---------------------------------------------------------
    # DISCOVERY
    # ---------------------------------------------------------

    def discover_tools(self) -> None:
        """
        Discover all tool implementations and tool definitions.
        """

        self._tools.clear()
        self._specs.clear()

        self._discover_implementations()
        self._discover_definitions()

    def _discover_implementations(self) -> None:
        """
        Discover Python tool implementations from:

            tools/implementations/
        """

        if not self.implementations_directory.exists():
            return

        for file_path in self.implementations_directory.glob("*.py"):

            if file_path.name == "__init__.py":
                continue

            self._load_tool(file_path)

    def _discover_definitions(self) -> None:
        """
        Discover ToolSpec YAML definitions from:

            tools/definitions/
        """

        if not self.definitions_directory.exists():
            return

        for file_path in self.definitions_directory.glob("*.yaml"):
            self._load_spec(file_path)

    # ---------------------------------------------------------
    # LOAD IMPLEMENTATION
    # ---------------------------------------------------------

    def _load_tool(
        self,
        file_path: Path,
    ) -> None:
        """
        Dynamically load a Python tool implementation
        and register its BaseTool class.
        """

        module_name = (
            f"enterprise_dynamic_tool_{file_path.stem}"
        )

        module_spec = importlib.util.spec_from_file_location(
            module_name,
            file_path,
        )

        if (
            module_spec is None
            or module_spec.loader is None
        ):
            raise ImportError(
                f"Unable to load tool: {file_path}"
            )

        module = importlib.util.module_from_spec(
            module_spec
        )

        module_spec.loader.exec_module(module)

        for _, obj in inspect.getmembers(
            module,
            inspect.isclass,
        ):

            if (
                issubclass(obj, BaseTool)
                and obj is not BaseTool
                and obj.__module__ == module.__name__
            ):
                tool_id = file_path.stem

                self.register(
                    tool_id,
                    obj,
                )

                break

    # ---------------------------------------------------------
    # LOAD DEFINITION
    # ---------------------------------------------------------

    def _load_spec(
        self,
        file_path: Path,
    ) -> None:
        """
        Load a ToolSpec from a YAML definition.
        """

        data = yaml.safe_load(
            file_path.read_text(
                encoding="utf-8"
            )
        )

        tool_spec = ToolSpec.model_validate(
            data
        )

        self.register_spec(
            tool_spec.id,
            tool_spec,
        )

    # ---------------------------------------------------------
    # REGISTER IMPLEMENTATION
    # ---------------------------------------------------------

    def register(
        self,
        tool_id: str,
        tool_class: Type[BaseTool],
    ) -> None:
        """
        Register a tool implementation.
        """

        if not tool_id.strip():
            raise ValueError(
                "Tool ID cannot be empty."
            )

        if not issubclass(
            tool_class,
            BaseTool,
        ):
            raise TypeError(
                "Tool must inherit from BaseTool."
            )

        self._tools[tool_id] = tool_class

    # ---------------------------------------------------------
    # REGISTER SPECIFICATION
    # ---------------------------------------------------------

    def register_spec(
        self,
        tool_id: str,
        tool_spec: ToolSpec,
    ) -> None:
        """
        Register a ToolSpec.
        """

        if not tool_id.strip():
            raise ValueError(
                "Tool ID cannot be empty."
            )

        self._specs[tool_id] = tool_spec

    # ---------------------------------------------------------
    # GET TOOL
    # ---------------------------------------------------------

    def get(
        self,
        tool_id: str,
    ) -> BaseTool:
        """
        Create and return an instance of a registered tool.
        """

        if tool_id not in self._tools:
            raise KeyError(
                f"Tool not found: {tool_id}"
            )

        tool_class = self._tools[tool_id]

        return tool_class()

    # ---------------------------------------------------------
    # GET SPEC
    # ---------------------------------------------------------

    def get_spec(
        self,
        tool_id: str,
    ) -> ToolSpec:
        """
        Return the ToolSpec for a registered tool.
        """

        if tool_id not in self._specs:
            raise KeyError(
                f"Tool specification not found: {tool_id}"
            )

        return self._specs[tool_id]

    # ---------------------------------------------------------
    # LIST TOOLS
    # ---------------------------------------------------------

    def list_tools(self) -> list[str]:
        """
        Return all discovered tool IDs.
        """

        return list(self._tools.keys())

    # ---------------------------------------------------------
    # REMOVE TOOL
    # ---------------------------------------------------------

    def remove(
        self,
        tool_id: str,
    ) -> None:
        """
        Remove a tool from the registry.
        """

        if tool_id not in self._tools:
            raise KeyError(
                f"Tool not found: {tool_id}"
            )

        del self._tools[tool_id]

        self._specs.pop(
            tool_id,
            None,
        )