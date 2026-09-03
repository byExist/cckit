#!/usr/bin/env python3
"""PostToolUse hook: lint the just-edited markdown file with markdownlint-cli2
and hand the agent a framed instruction, never a raw tool dump.

Two framings, because the agent reacts to whatever this injects:
- exit 1 (lint violations): scope the fix to this edit, so the agent does not
  mass-clean pre-existing violations in files it barely touched.
- any other failure (broken config, env breakage, linter crash): say the tool
  failed and the file is fine, so the agent neither "fixes" healthy content
  nor derails into debugging the environment.

Base config resolution (project .markdownlint* files still layer on top via
markdownlint-cli2's own discovery, so the project always wins):
1. MARKDOWNLINT_HOOK_CONFIG env var (for tests)
2. ~/.claude/.markdownlint-cli2.jsonc (personal override, when present)
3. the config bundled with this plugin (team default)
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def resolve_config() -> str:
    env = os.environ.get("MARKDOWNLINT_HOOK_CONFIG")
    if env:
        return env
    personal = Path.home() / ".claude" / ".markdownlint-cli2.jsonc"
    if personal.is_file():
        return str(personal)
    return str(Path(__file__).resolve().parent.parent / ".markdownlint-cli2.jsonc")


CONFIG = resolve_config()
# realpath: on macOS /tmp resolves to /private/tmp and $TMPDIR to /var/folders/…
TMP_ROOTS = tuple(
    root.rstrip("/") + "/"
    for root in {os.path.realpath(tempfile.gettempdir()), os.path.realpath("/tmp")}
)


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return
    path = data.get("tool_input", {}).get("file_path", "")
    if not path.lower().endswith(".md"):
        return
    if os.path.realpath(path).startswith(TMP_ROOTS):
        return
    cli = shutil.which("markdownlint-cli2")
    if not Path(path).is_file() or cli is None:
        return
    try:
        result = subprocess.run(
            [cli, "--config", CONFIG, f":{path}"],
            capture_output=True, text=True, timeout=8,
        )
    except subprocess.TimeoutExpired:
        return
    if result.returncode == 0:
        return
    output = (result.stdout + result.stderr).strip()
    if result.returncode == 1:
        context = (
            f"markdownlint found issues in {path}. They cover the whole file, "
            "not only the lines just edited: fix what this edit introduced, "
            "and leave pre-existing violations alone unless the user asks.\n"
            f"{output}"
        )
    else:
        head = [
            line for line in output.splitlines()
            if line
            and not line.lstrip().startswith("at ")
            and not line.startswith("markdownlint-cli2 v")
        ][:3]
        context = (
            f"markdownlint itself failed (exit {result.returncode}) - a config "
            f"or environment problem, unrelated to {path}. Do not modify the "
            "file because of this; mention the failure to the user in one "
            "line.\n" + "\n".join(head)
        )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": context,
        }
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
