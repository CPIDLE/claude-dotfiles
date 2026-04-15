#!/usr/bin/env python3
"""intercept-rm.py — PreToolUse hook: redirect `rm` to Recycle Bin.

Reads Bash tool input from stdin (JSON), detects rm commands,
and rewrites them to use trash.py (send2trash) instead.

Exit codes:
  0 — allow (possibly with updatedInput)
"""

import json
import re
import shlex
import sys
from pathlib import Path

TRASH_SCRIPT = str(Path(__file__).resolve().parent / "trash.py")


def main():
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    command = data.get("tool_input", {}).get("command", "")
    stripped = command.strip()

    # Only intercept standalone rm commands (not piped/chained)
    rm_match = re.match(r"^rm\s+(.+)$", stripped)
    if not rm_match:
        sys.exit(0)

    rest = rm_match.group(1)
    if any(op in rest for op in ["|", "&&", ";", "$(", "`"]):
        sys.exit(0)

    # Parse flags and file paths
    try:
        parts = shlex.split(rest)
    except ValueError:
        sys.exit(0)

    files = [p for p in parts if not p.startswith("-")]
    if not files:
        sys.exit(0)

    # Build replacement command
    quoted_files = " ".join(shlex.quote(f) for f in files)
    trash_cmd = f'python "{TRASH_SCRIPT}" {quoted_files}'

    result = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": f"rm → Recycle Bin: {', '.join(files)}",
            "updatedInput": {
                "command": trash_cmd
            },
        }
    }
    json.dump(result, sys.stdout)
    sys.exit(0)


if __name__ == "__main__":
    main()
