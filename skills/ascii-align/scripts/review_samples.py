#!/usr/bin/env python3
"""review_samples.py — Automated review of fixed ASCII-art files.

Checks _sample_XXX.md files and renames them:
  v_sample_XXX.md  — PASS (no issues)
  x_sample_XXX.md  — FAIL (issues remain)

Review criteria:
  1. No illegal Unicode symbols in code blocks
  2. No width mismatches (every │...│ row matches hrule display width)

Usage:
    python review_samples.py [dir]        # review all _sample_*.md in dir
    python review_samples.py <file.md>    # review single file
    python review_samples.py --dry-run [dir]  # report only, no rename
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from symbol_fix import find_illegal, width_diagnostic

_FENCE_RE = re.compile(r"(```+)\n(.*?)\1", re.DOTALL)


def check_file(path: Path) -> list[str]:
    """Return list of issue strings. Empty = PASS."""
    text = path.read_text(encoding="utf-8")
    issues: list[str] = []

    for m in _FENCE_RE.finditer(text):
        content = m.group(2)
        lines = content.split("\n")

        # Check 1: illegal symbols
        for i, line in enumerate(lines):
            for _, ch, name in find_illegal(line):
                issues.append(f"L{i+1}: illegal symbol `{ch}` ({name})")

        # Check 2: width mismatches
        for diag in width_diagnostic(lines):
            issues.append(diag.strip())

    return issues


def _strip_prefix(name: str) -> str:
    """Strip known state prefixes (_  p_  v_  x_) from filename."""
    for prefix in ("v_", "x_", "p_", "_"):
        if name.startswith(prefix):
            return name[len(prefix):]
    return name


def review(path: Path, dry_run: bool = False) -> str:
    """Review one file. Returns 'PASS' or 'FAIL: <reason>'."""
    issues = check_file(path)
    base = _strip_prefix(path.name)

    if not issues:
        if not dry_run:
            new_name = path.parent / ("v_" + base)
            if new_name.exists():
                new_name.unlink()
            path.rename(new_name)
        return "PASS"
    else:
        summary = "; ".join(issues[:3]) + ("..." if len(issues) > 3 else "")
        if not dry_run:
            new_name = path.parent / ("x_" + base)
            if new_name.exists():
                new_name.unlink()
            path.rename(new_name)
        return f"FAIL: {summary}"


def resolve_paths(args: list[str]) -> list[Path]:
    if not args:
        args = ["."]
    paths: list[Path] = []
    for a in args:
        p = Path(a)
        if p.is_file() and p.suffix == ".md":
            paths.append(p)
        elif p.is_dir():
            paths.extend(sorted(p.glob("_sample_*.md")))
    return paths


def main() -> None:
    raw = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry_run = "--dry-run" in sys.argv

    paths = resolve_paths(raw)
    if not paths:
        print("No _sample_*.md files found.")
        sys.exit(0)

    passed = failed = 0
    for p in paths:
        result = review(p, dry_run=dry_run)
        tag = "DRY " if dry_run else ""
        print(f"{tag}{result:6}  {p.name}")
        if result == "PASS":
            passed += 1
        else:
            failed += 1

    print(f"\n{passed} PASS  {failed} FAIL  (total {passed+failed})")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
