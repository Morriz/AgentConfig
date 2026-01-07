# Agent commands and tooling

Parses and distributes agent-native implementations of commands and tools.

## Prerequisites

Install [uv](https://github.com/astral-sh/uv) for Python dependency management:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Usage

Run `./bin/distribute.py` to only build dist/ targets.
Run `./bin/distribute.py --deploy` to build dist/ targets and deploy them.

Codex expects a `prompts/` folder (not `commands/`), so Codex commands build into `dist/codex/prompts` and deploy into `~/.codex/prompts`.
Deploy merges each agent's `dist/<agent>/` tree into its target (equivalent to `cp -R dist/<agent>/* ~/.<agent>/`).

Skills deploy to:
- `dist/claude/skills` → `~/.claude/skills`
- `dist/codex/skills` → `~/.codex/skills`
- `dist/gemini/skills` → `~/.gemini/skills`

**Note:** The script uses `uv run` via shebang to automatically manage dependencies. No manual venv setup required.
