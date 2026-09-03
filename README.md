# Enterprise Agent Framework - CLI Scaffolding MVP

This is the first control-plane milestone for the planned enterprise agent/workflow framework.

It implements interactive creation, editing, deletion, validation, LLM-backed generation, and editor opening for Agents, Workflows, and Tools.

## Run

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -e ".[dev,openai]"
```

For a no-API-key smoke test, put `LLM_PROVIDER=mock` in `.env`.

Then run:

```bash
python -m enterprise_agent_framework.cli.main
```

## Runtime boundary

```text
AgentSpec / WorkflowSpec / ToolSpec
              |
              v
        Your framework
              |
              v
        CrewAI Adapter
              |
              v
     CrewAI Agent / Crew / Flow
```

Generated tools are syntax-checked but never executed automatically.
