#!/usr/bin/env python3
"""gen_prompt.py — Generate fix prompt for misaligned ASCII-art in Markdown files.

Pipeline:
  1. symbol_fix — replace illegal Unicode with ASCII equivalents (in-memory)
  2. Width analysis — find per-group width mismatches
  3. Assemble file-specific prompt (Input + Issues only)

Shared rules/symbols/task are written ONCE to _RULES.prompt.txt in each output
directory, not repeated per file.  Agent usage:
    Read _RULES.prompt.txt + sample_XXX.prompt.txt → fix → write back

Usage:
    python gen_prompt.py <file.md> [<file2.md> ...]
    Output: _RULES.prompt.txt (once per dir) + <file>.prompt.txt per file
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Ensure scripts/ is on path when invoked from other directories
sys.path.insert(0, str(Path(__file__).parent))

from symbol_fix import replace_symbols, find_illegal, width_diagnostic
from ascii_align import display_width

# ---------------------------------------------------------------------------
# Shared rules file (written once per output directory)
# ---------------------------------------------------------------------------

RULES_FILENAME = "_RULES.prompt.txt"

_RULES_CONTENT = """\
# ASCII Art Fix — Shared Rules

## Character Width Rules (Sarasa Mono TC)

| Category | Examples | Width |
|----------|----------|-------|
| ASCII printable | A-Z, 0-9, punctuation | 1 |
| Box drawing | `─│┌┐└┘├┤┬┴┼═║┏┓┗┛╞╘╪┊╱╲` | 1 |
| CJK characters | Chinese/Japanese/Korean hanzi | 2 |
| Full-width brackets | `（）` | 2 |
| Degree / EN dash | `°` `–` | 1 |
| Other Unicode | `→×▼●★✓` (forbidden, already replaced) | 2 |

**Rule:** every `│...│` content row must have the same display width as the
horizontal rule lines (`┌──┐` / `└──┘` / `├──┤`) in the same box.

## Forbidden Symbols (already replaced in each input file)

| Was | Now | Reason |
|-----|-----|--------|
| `→` `←` | `-->` `<--` | arrows are w2 in Sarasa Mono TC |
| `↑` `↓` | `^` `v` | vertical arrows w2 |
| `▼` `▲` | `v` `^` | solid triangles w2 |
| `×` | `x` | multiplication sign w2 |
| `●` `○` | `*` `o` | circles w2 |
| `✓` `✗` | `OK` `NG` | check/cross w2 |
| `·` `•` | `.` `*` | middle dots w2 |

Do NOT reintroduce any forbidden symbol in the output.

## Task

Rewrite the ASCII art in the accompanying file so that every `│...│` content
row has **identical display width** matching its surrounding horizontal rule lines:

- CJK characters (Chinese/Japanese/Korean) = 2 columns each
- Box-drawing characters (`─│┌┐` etc.) = 1 column each
- ASCII characters = 1 column each
- Trailing spaces before the right border `│` must be adjusted to pad to target width

Preserve all structure and content; only fix spacing/padding.
Do NOT introduce any forbidden Unicode symbol.

Output: the corrected art as a single fenced code block. No explanation.
""".strip()

# ---------------------------------------------------------------------------
# Code block extraction
# ---------------------------------------------------------------------------

def _extract_blocks(text: str) -> list[tuple[int, str, str | None]]:
    """Return list of (char_offset, block_content, aa_type_or_None)."""
    results = []
    pattern = re.compile(r"(```+)\n(.*?)\1", re.DOTALL)
    lines = text.split("\n")
    # Build offset map: line_index → char offset of start of that line
    offsets = []
    pos = 0
    for ln in lines:
        offsets.append(pos)
        pos += len(ln) + 1  # +1 for \n

    for m in pattern.finditer(text):
        content = m.group(2)
        start = m.start()
        # Find the line just before the opening fence
        line_before = text[:start].rstrip("\n").split("\n")[-1].strip()
        aa_match = re.search(r"<!--\s*aa:\s*(\w+)\s*-->", line_before)
        aa_type = aa_match.group(1) if aa_match else None
        results.append((start, content, aa_type))
    return results

# ---------------------------------------------------------------------------
# Symbol fix + width analysis (in-memory)
# ---------------------------------------------------------------------------

def _apply_symbol_fix(content: str) -> tuple[str, list[str]]:
    """Return (fixed_content, replacement_notes)."""
    lines = content.split("\n")
    fixed = []
    notes = []
    for i, line in enumerate(lines):
        illegals = find_illegal(line)
        if illegals:
            new_line = replace_symbols(line)
            for _, ch, name in illegals:
                notes.append(f"  L{i+1}: `{ch}` ({name})")
            fixed.append(new_line)
        else:
            fixed.append(line)
    return "\n".join(fixed), notes


def _width_issues(content: str) -> list[str]:
    """Return width_diagnostic lines for cleaned content."""
    return width_diagnostic(content.split("\n"))


_TREE_BRANCH_RE = re.compile(r"[├└]──")
_RIGHT_BORDER_CHARS = set("│┐┘┤")


def _is_tree_trunk(line: str) -> bool:
    """True for lines like '    │' — tree connector, not a box border."""
    s = line.rstrip()
    return bool(s) and s[-1] == "│" and s[:-1].strip() == ""


def _is_complex_block(lines: list[str], aa_type: str | None) -> bool:
    """Return True if the block is structurally complex (needs extra care)."""
    if aa_type == "layout":
        return True

    non_blank = [l for l in lines if l.strip()]
    if not non_blank:
        return False

    tree_lines = sum(1 for l in non_blank if _TREE_BRANCH_RE.search(l))
    # Exclude tree-trunk lines (│ with only spaces before) from bordered count
    box_bordered = sum(
        1 for l in non_blank
        if l.rstrip() and l.rstrip()[-1] in _RIGHT_BORDER_CHARS
        and not _is_tree_trunk(l)
    )

    # Tree-heavy diagram (≥25% of non-blank lines are branch/fork patterns)
    if tree_lines >= 4 and tree_lines / len(non_blank) >= 0.25:
        return True

    # Dominant tree/branch structure (more branch lines than actual box lines)
    if tree_lines >= 4 and tree_lines >= box_bordered:
        return True

    # Mostly free-form (< 40% of non-blank lines are proper box lines)
    if len(non_blank) >= 10 and box_bordered < len(non_blank) * 0.4:
        return True

    return False


_COMPLEX_WARNING = (
    "⚠ **Complex diagram** — auto-detected as structurally complex "
    "(branching tree, mixed layout, or free-form flow without traditional box borders). "
    "Apply extra care: preserve all structural intent, fix only clear "
    "alignment errors, and do NOT simplify or restructure the diagram."
)

# ---------------------------------------------------------------------------
# Prompt assembly — file-specific part only (Input + Issues)
# ---------------------------------------------------------------------------

def gen_file_prompt(filepath: Path) -> str:
    """Return the file-specific prompt section (Input + Issues only)."""
    text = filepath.read_text(encoding="utf-8")
    blocks = _extract_blocks(text)

    if not blocks:
        return f"# No code blocks found in {filepath.name}\n"

    parts: list[str] = []
    parts.append(f"# {filepath.name}\n")

    multi = len(blocks) > 1

    for idx, (_, content, aa_type) in enumerate(blocks):
        label = f"Block {idx + 1}" if multi else "Code Block"
        type_note = f" (type: `{aa_type}`)" if aa_type else ""

        fixed_content, sym_notes = _apply_symbol_fix(content)
        width_notes = _width_issues(fixed_content)

        if _is_complex_block(fixed_content.split("\n"), aa_type):
            parts.append(_COMPLEX_WARNING)
            parts.append("")

        parts.append(f"## Input — {label}{type_note}")
        parts.append("")
        parts.append("```")
        parts.append(fixed_content)
        parts.append("```")
        parts.append("")

        has_sym = bool(sym_notes)
        has_width = bool(width_notes)

        if has_sym or has_width:
            parts.append(f"## Issues — {label}")
            parts.append("")
            if has_sym:
                parts.append("**Symbol replacements applied:**")
                parts.extend(sym_notes)
                parts.append("")
            if has_width:
                parts.append("**Width mismatches (need fixing):**")
                parts.extend(width_notes)
                parts.append("")
        else:
            parts.append(
                f"*({label}: no automatic issues detected — "
                "verify border alignment visually)*"
            )
            parts.append("")

    return "\n".join(parts)

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    args = sys.argv[1:]
    if not args:
        print("Usage: python gen_prompt.py <file.md> [<file2.md> ...]")
        sys.exit(1)

    paths: list[Path] = []
    for arg in args:
        p = Path(arg)
        if not p.exists():
            print(f"ERROR: not found: {p}", file=sys.stderr)
            continue
        if p.suffix.lower() != ".md":
            print(f"SKIP (not .md): {p}", file=sys.stderr)
            continue
        paths.append(p)

    if not paths:
        return

    # Write _RULES.prompt.txt once per output directory
    dirs_written: set[Path] = set()
    for p in paths:
        d = p.parent
        if d not in dirs_written:
            rules_out = d / RULES_FILENAME
            rules_out.write_text(_RULES_CONTENT, encoding="utf-8", newline="\n")
            print(f"RULES {rules_out}")
            dirs_written.add(d)

    # Write per-file prompt (Input + Issues only)
    for p in paths:
        prompt = gen_file_prompt(p)
        out = p.with_suffix(".prompt.txt")
        out.write_text(prompt, encoding="utf-8", newline="\n")
        print(f"OK  {out}")


if __name__ == "__main__":
    main()
