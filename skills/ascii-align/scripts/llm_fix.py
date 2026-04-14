#!/usr/bin/env python3
"""llm_fix.py — Run ascii_align.py then call Claude Code to fix residuals.

Usage:
    python llm_fix.py <path>          # file or directory
    python llm_fix.py --dry-run <path>  # show prompt without calling LLM

Pipeline:
  1. Run ascii_align.py (rule-based pass)
  2. Run ascii_align.py --check to detect residuals
  3. For files with warnings, generate a prompt and call `claude -p` to fix
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ALIGN_SCRIPT = SCRIPT_DIR / "ascii_align.py"
PROMPT_TEMPLATE = SCRIPT_DIR / "llm_fix_prompt.md"


def run_align(targets: list[Path]) -> str:
    """Run ascii_align.py (apply mode). Returns stdout."""
    cmd = [sys.executable, str(ALIGN_SCRIPT)] + [str(t) for t in targets]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    return r.stdout + r.stderr


def run_check(filepath: Path) -> tuple[str, bool]:
    """Run ascii_align.py --check on one file. Returns (output, has_issues)."""
    cmd = [sys.executable, str(ALIGN_SCRIPT), "--check", str(filepath)]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    output = r.stdout + r.stderr
    has_issues = "⚠" in output or "Fixed:" in output
    return output, has_issues


def build_prompt(filepath: Path, diagnostics: str) -> str:
    """Build the LLM fix prompt for a file."""
    file_content = filepath.read_text(encoding="utf-8")

    return f"""Fix the ASCII box-drawing alignment issues in the code block below.

## Display Width Rules (Sarasa Mono TC)

| Type              | Examples              | Width |
|-------------------|-----------------------|-------|
| ASCII, Box-draw   | A-Z ─│├┐┘┤┌┬┴┼       | 1     |
| CJK               | 中文設備              | 2     |
| Fullwidth punct   | （）【】｜            | 2     |
| Arrows            | →←↑↓↔                | 2     |
| Geometric shapes  | ▼▲●○■□◆              | 2     |
| EM dash / ellipsis| —…                    | 2     |
| Circled digits    | ①②③                  | 2     |

## Common Error Patterns to Fix

1. **Off-by-1 width**: Every content line has 1 extra trailing space before
   the right border. Fix: remove 1 space from each line between the last
   meaningful character and the right border. Hrule lines lose 1 dash.

2. **Inner box spacing**: Side-by-side inner boxes have wrong inter-box gap
   or the right box shifted. Fix: ensure consistent gap between left box's
   right border and right box's left border, preserving total line width.

3. **Junction ─ count**: A segment between two junctions has wrong ─ count.
   Fix: adjust ─ count so junctions align vertically with │ in content lines.

4. **Branch connector displaced**: After ┌─┼─┐, the │ connectors below are
   merged or shifted. Fix: restore │ to align with ┼ and ┐ columns above.

5. **Inner box content displaced**: Nested box content has massive leading
   whitespace. Fix: remove excess space so content starts after the inner
   box's left │, matching ┌─┐ header width.

## Constraint

- Every line within the same box group MUST have identical display width.
- Only adjust spacing (trailing spaces, ─ fill). Never change text content.
- After fixing, the box should look correct in a monospace terminal.

## Diagnostics

```
{diagnostics}
```

## File Content

```
{file_content}
```

Fix the issues. Output ONLY the corrected file content (the full file, including ``` fences)."""


def call_claude(prompt: str, filepath: Path) -> str | None:
    """Call claude -p with the prompt. Returns response or None on failure."""
    cmd = [
        "claude",
        "-p", prompt,
        "--output-format", "text",
        "--no-input",
    ]
    try:
        r = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=120,
        )
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
        print(f"  claude returned code {r.returncode}", file=sys.stderr)
        if r.stderr:
            print(f"  stderr: {r.stderr[:200]}", file=sys.stderr)
        return None
    except FileNotFoundError:
        print("ERROR: 'claude' CLI not found in PATH", file=sys.stderr)
        return None
    except subprocess.TimeoutExpired:
        print("ERROR: claude timed out (120s)", file=sys.stderr)
        return None


def extract_code_block(response: str) -> str | None:
    """Extract content between ``` fences from LLM response."""
    lines = response.split("\n")
    in_block = False
    result = []
    for line in lines:
        if line.strip().startswith("```") and not in_block:
            in_block = True
            continue
        elif line.strip().startswith("```") and in_block:
            in_block = False
            continue
        if in_block:
            result.append(line)
    return "\n".join(result) if result else None


def main() -> None:
    dry_run = False
    raw_args = sys.argv[1:]
    args: list[str] = []
    for a in raw_args:
        if a == "--dry-run":
            dry_run = True
        else:
            args.append(a)

    if not args:
        print("Usage: python llm_fix.py [--dry-run] <path ...>")
        sys.exit(1)

    # Collect targets
    targets: list[Path] = []
    for arg in args:
        p = Path(arg)
        if p.is_file():
            targets.append(p)
        elif p.is_dir():
            targets.extend(sorted(p.glob("*.md")))
        else:
            print(f"WARNING: {arg} not found", file=sys.stderr)

    if not targets:
        print("No .md files found.")
        return

    # Step 1: rule-based pass
    print("=== Step 1: ascii_align.py (rule-based) ===")
    output = run_align(targets)
    print(output)

    # Step 2: check for residuals
    print("=== Step 2: checking for residuals ===")
    files_needing_fix: list[tuple[Path, str]] = []
    for fp in targets:
        diag, has_issues = run_check(fp)
        if has_issues:
            files_needing_fix.append((fp, diag))
            print(f"  NEEDS FIX: {fp.name}")
        else:
            print(f"  OK: {fp.name}")

    if not files_needing_fix:
        print("\nAll files clean after rule-based pass.")
        return

    # Step 3: LLM fix
    print(f"\n=== Step 3: LLM fix ({len(files_needing_fix)} files) ===")
    for fp, diag in files_needing_fix:
        prompt = build_prompt(fp, diag)

        if dry_run:
            print(f"\n--- Prompt for {fp.name} ({len(prompt)} chars) ---")
            print(prompt[:500])
            print("... (truncated)")
            continue

        print(f"\n  Fixing {fp.name} via claude -p ...")
        response = call_claude(prompt, fp)
        if response is None:
            print(f"  SKIP: no response for {fp.name}")
            continue

        # Extract corrected content
        corrected = extract_code_block(response)
        if corrected is None:
            # Try using the whole response as content
            corrected = response

        # Write back
        fp.write_text(corrected + "\n", encoding="utf-8")
        print(f"  WROTE: {fp.name}")

    # Step 4: final check
    print("\n=== Step 4: final check ===")
    for fp in targets:
        diag, has_issues = run_check(fp)
        status = "⚠ ISSUES" if has_issues else "OK"
        print(f"  {status}: {fp.name}")


if __name__ == "__main__":
    main()
