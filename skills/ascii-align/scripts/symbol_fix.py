#!/usr/bin/env python3
"""symbol_fix.py — Replace illegal Unicode symbols in ASCII-art code blocks.

Stage 1 tool: replace w2 Unicode symbols with ASCII equivalents, then
print a width diagnostic for manual or LLM-assisted alignment.

Does NOT auto-fix widths — that requires structural understanding
(table columns, nested boxes) which only a human or LLM can judge.

Usage:
    python symbol_fix.py [path ...]
    - No args      → scan cwd for *.md
    - File arg     → process that file
    - Dir arg      → scan that dir for *.md
    - --dry-run    → report without writing
    - --check      → report only, exit 1 if issues found
"""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

from ascii_align import char_cols, display_width

# ---------------------------------------------------------------------------
# Symbol mapping table — Unicode w2 → ASCII stable
# ---------------------------------------------------------------------------
# Order matters: longer sequences first to avoid partial matches.

SYMBOL_MAP = [
    # Multi-char sequences (must come before single-char)
    ("─►", "──>"),
    ("─▶", "──>"),
    ("─→", "──>"),
    ("◄─", "<──"),
    ("←─", "<──"),
    # Arrows
    ("→", "-->"),
    ("←", "<--"),
    ("↔", "<->"),
    ("►", "->"),
    ("▶", "->"),
    ("▸", "->"),
    ("◄", "<-"),
    ("↑", "^ "),
    ("↓", "v "),
    ("▲", "^ "),
    ("▼", "v "),
    ("↕", "| "),
    # Math / Logic
    ("≤", "<="),
    ("≥", ">="),
    ("≠", "!="),
    ("≈", "~="),
    ("±", "+-"),
    ("×", "x "),
    ("÷", "/ "),
    ("∈", "in"),
    ("∧", "&&"),
    ("∨", "||"),
    ("∞", "oo"),
    ("√", "V "),
    # Geometric / Decorative
    ("●", "* "),
    ("○", "o "),
    ("■", "# "),
    ("□", "[]"),
    ("◆", "* "),
    ("◇", "<>"),
    ("★", "* "),
    ("☆", "* "),
    # Check / Cross
    ("✓", "v "),
    ("✔", "v "),
    ("✗", "x "),
    ("✘", "x "),
    # Punctuation
    ("·", ". "),
    ("•", "* "),
    ("§", "S."),
    ("²", "^2"),
    ("‖", "||"),
    ("█", "##"),
]

# Box drawing chars — these are LEGAL inside boxes (w1)
_BOX_DRAWING = set(range(0x2500, 0x2580))
_BOX_EXTRA = {0x2571, 0x2572}  # ╱ ╲

# ---------------------------------------------------------------------------
# Detection
# ---------------------------------------------------------------------------

def is_legal(ch: str) -> bool:
    """True if character is safe inside a box (predictable width)."""
    cp = ord(ch)
    if cp <= 0x7F:
        return True
    if cp in _BOX_DRAWING or cp in _BOX_EXTRA:
        return True
    eaw = unicodedata.east_asian_width(ch)
    if eaw in ("F", "W"):  # CJK / fullwidth — known w2
        return True
    if ch in "°–":  # Calibrated w1 exceptions
        return True
    return False


def find_illegal(line: str) -> list[tuple[int, str, str]]:
    """Return list of (position, char, name) for illegal chars in line."""
    result = []
    for i, ch in enumerate(line):
        if not is_legal(ch):
            name = unicodedata.name(ch, f"U+{ord(ch):04X}")
            result.append((i, ch, name))
    return result

# ---------------------------------------------------------------------------
# Replacement
# ---------------------------------------------------------------------------

def replace_symbols(line: str) -> str:
    """Replace all illegal Unicode symbols with ASCII equivalents."""
    for old, new in SYMBOL_MAP:
        if old in line:
            line = line.replace(old, new)
    return line

# ---------------------------------------------------------------------------
# Width diagnostic
# ---------------------------------------------------------------------------

_RIGHT_BORDER = set("│┐┘┤")


def _has_right_border(line: str) -> bool:
    s = line.rstrip()
    return bool(s) and s[-1] in _RIGHT_BORDER


def _is_hrule(line: str) -> bool:
    s = line.rstrip()
    if len(s) < 3:
        return False
    return s[-1] in _RIGHT_BORDER and all(
        c in "─┌└├┬┴┼┐┘┤═╔╗╚╝║╦╩╣╠╬ " for c in s
    )


def _is_tree_trunk(line: str) -> bool:
    s = line.rstrip()
    if not s or s[-1] != "│":
        return False
    return s[:-1].strip() == "" or s.strip() == "│"


def width_diagnostic(block_lines: list[str]) -> list[str]:
    """Generate width diagnostic for bordered lines in a code block.

    Returns list of diagnostic messages (empty if all OK).
    """
    diags = []

    # Find groups of bordered lines
    groups: list[list[int]] = []
    current: list[int] = []
    for i, line in enumerate(block_lines):
        s = line.rstrip()
        if not s or _is_tree_trunk(line):
            if current:
                groups.append(current)
                current = []
            continue
        if _has_right_border(line):
            # Split on width jump
            if current:
                prev_w = display_width(block_lines[current[-1]])
                this_w = display_width(line)
                if abs(prev_w - this_w) > 3:
                    groups.append(current)
                    current = []
            current.append(i)
        else:
            if current:
                groups.append(current)
                current = []
    if current:
        groups.append(current)

    for group in groups:
        # Find target from hrule
        hrule_widths = []
        for idx in group:
            if _is_hrule(block_lines[idx]):
                hrule_widths.append(display_width(block_lines[idx]))

        if not hrule_widths:
            continue

        target = max(hrule_widths)

        # Check each non-hrule line
        mismatches = []
        for idx in group:
            if _is_hrule(block_lines[idx]):
                continue
            w = display_width(block_lines[idx])
            if w != target:
                diff = w - target
                sign = "+" if diff > 0 else ""
                mismatches.append(f"    L{idx+1}: w={w} ({sign}{diff})")

        if mismatches:
            diags.append(f"  Group L{group[0]+1}-L{group[-1]+1} target={target}:")
            diags.extend(mismatches)

    return diags

# ---------------------------------------------------------------------------
# Process a single file
# ---------------------------------------------------------------------------

def process_file(path: Path, dry_run: bool = False, check: bool = False) -> dict:
    """Process one markdown file. Returns stats dict."""
    text = path.read_text(encoding="utf-8")
    stats = {"path": str(path), "replacements": 0, "width_issues": 0,
             "issues": [], "diags": []}

    pattern = re.compile(r"(```+)\n(.*?)\1", re.DOTALL)
    new_text = text
    offset = 0

    for m in pattern.finditer(text):
        block = m.group(2)
        block_start = m.start(2)
        lines = block.split("\n")

        # --- Stage 1: Symbol replacement ---
        new_lines = []
        for i, line in enumerate(lines):
            illegals = find_illegal(line)
            if illegals:
                new_line = replace_symbols(line)
                for _, ch, name in illegals:
                    stats["replacements"] += 1
                    stats["issues"].append(
                        f"  Replace: {ch} ({name}) on block L{i+1}"
                    )
                new_lines.append(new_line)
            else:
                new_lines.append(line)

        # --- Stage 2: Width diagnostic (report only) ---
        diags = width_diagnostic(new_lines)
        if diags:
            stats["width_issues"] += len([d for d in diags if d.startswith("    ")])
            stats["diags"].extend(diags)

        new_block = "\n".join(new_lines)
        if new_block != block:
            new_text = (
                new_text[: block_start + offset]
                + new_block
                + new_text[block_start + offset + len(block):]
            )
            offset += len(new_block) - len(block)

    changed = new_text != text
    if changed and not dry_run and not check:
        path.write_text(new_text, encoding="utf-8", newline="\n")

    return stats

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def resolve_paths(args: list[str]) -> list[Path]:
    if not args:
        args = ["."]
    paths = []
    for a in args:
        p = Path(a)
        if p.is_file() and p.suffix == ".md":
            paths.append(p)
        elif p.is_dir():
            paths.extend(sorted(p.glob("*.md")))
    return paths


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv
    check = "--check" in sys.argv

    paths = resolve_paths(args)
    if not paths:
        print("No .md files found.")
        sys.exit(0)

    total_replacements = 0
    total_width_issues = 0
    files_with_issues = 0

    for path in paths:
        stats = process_file(path, dry_run=dry_run, check=check)
        has_issues = stats["replacements"] > 0 or stats["width_issues"] > 0
        if has_issues:
            files_with_issues += 1
            total_replacements += stats["replacements"]
            total_width_issues += stats["width_issues"]

            if stats["replacements"] > 0:
                action = "Would replace" if (dry_run or check) else "Replaced"
                print(f"{action}: {stats['path']} ({stats['replacements']} symbols)")
                for issue in stats["issues"]:
                    print(issue)

            if stats["diags"]:
                print(f"⚠ Width: {stats['path']}")
                for d in stats["diags"]:
                    print(d)
        else:
            print(f"OK: {stats['path']}")

    print(f"\nSummary: {files_with_issues} files, "
          f"{total_replacements} symbols replaced, "
          f"{total_width_issues} width issues (manual fix needed)")

    if check and (total_replacements + total_width_issues) > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
