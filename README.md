# Agent commands and tooling

Parses and distributes agent-native implementations of commands and tools.

Run `./bin/distribute.py` to only build dist/ targets.
Run `./bin/distribute.py --deploy` to build dist/ targets and deploy them.

Codex expects a `prompts/` folder (not `commands/`), so Codex commands build into `dist/codex/prompts` and deploy into `~/.codex/prompts`.
Deploy merges each agent’s `dist/<agent>/` tree into its target (equivalent to `cp -R dist/<agent>/* ~/.<agent>/`).

Note: the script already points to the repo-managed `.venv` in its shebang; just execute it—do not recreate the venv or install anything system-wide.
