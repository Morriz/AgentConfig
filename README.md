# Agent commands and tooling

Parses and distributes agent-native implementations of commands and tools.

Run `./bin/distribute.py` to only build dist/ targets.
Run `./bin/distribute.py --deploy` to build dist/ targets and deploy them.

Note: the script already points to the repo-managed `.venv` in its shebang; just execute it—do not recreate the venv or install anything system-wide.
