from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path.cwd()

# -----------------------------------------
# Agents
# -----------------------------------------

AGENTS_DIR = (
    PROJECT_ROOT
    / "agents"
    / "definitions"
)

# -----------------------------------------
# Tools
# -----------------------------------------

TOOLS_DIR = (
    PROJECT_ROOT
    / "tools"
)

TOOL_DEFINITIONS_DIR = (
    TOOLS_DIR
    / "definitions"
)

TOOL_IMPLEMENTATIONS_DIR = (
    TOOLS_DIR
    / "implementations"
)

# -----------------------------------------
# Workflows
# -----------------------------------------

WORKFLOWS_DIR = PROJECT_ROOT / "workflows" / "definitions"

# -----------------------------------------
# LLM
# -----------------------------------------

LLM_PROVIDER = os.getenv(
    "LLM_PROVIDER",
    "mock"
).lower()

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY",
    ""
)

OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-4o"
)

OPENAI_BASE_URL = (
    os.getenv("OPENAI_BASE_URL")
    or None
)

EDITOR = os.getenv(
    "EDITOR",
    "auto"
)


def ensure_directories():

    for directory in (
        AGENTS_DIR,
        WORKFLOWS_DIR,
        TOOL_DEFINITIONS_DIR,
        TOOL_IMPLEMENTATIONS_DIR,
    ):

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )