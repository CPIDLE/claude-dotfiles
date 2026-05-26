#!/usr/bin/env python3
"""index-append.py — PostToolUse hook: append new files to INDEX.md.

Fires after every Write tool call. If INDEX.md exists in the same
directory as the written file and the filename is not already listed,
appends a placeholder row.
"""

import json
import sys
from datetime import date
from pathlib import Path


def main():
    raw = sys.stdin.buffer.read().decode("utf-8-sig")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    file_path = data.get("tool_input", {}).get("file_path", "")
    if not file_path:
        sys.exit(0)

    written = Path(file_path).resolve()
    filename = written.name

    if filename.upper() == "INDEX.MD":
        sys.exit(0)

    index_path = written.parent / "INDEX.md"
    if not index_path.exists():
        sys.exit(0)

    try:
        content = index_path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError):
        sys.exit(0)

    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("|"):
            cells = [c.strip() for c in stripped.split("|")]
            if len(cells) >= 2 and cells[1] == filename:
                sys.exit(0)

    today = date.today().isoformat()
    new_row = f"| {filename} | — | draft | {today} | — |\n"

    try:
        with open(index_path, "a", encoding="utf-8") as f:
            f.write(new_row)
    except OSError:
        sys.exit(0)

    print(f"INDEX.md: appended {filename}")


if __name__ == "__main__":
    main()
