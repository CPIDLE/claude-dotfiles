#!/usr/bin/env python3
"""llm_review.py — Generate LLM review prompts for ASCII-art fix verification.

Option C review: checks issues the programmatic width checker misses:
  1. Vertical connector column drift (│/v not aligned across rows or with junction)
  2. Structural corruption (box chars in unexpected positions)
  3. Parallel box connector/gap parity (────> width != inter-box gap)
  4. CJK label row alignment (spacing after CJK chars must account for display width)

Usage:
    python llm_review.py <file.md> [<file2.md> ...]
    Output: <file>.review.txt per file

The review agent reads <file>.review.txt, outputs PASS or FAIL + issues.
On FAIL, the pipeline appends issues to <file_base>.prompt.txt for the next fix round.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from symbol_fix import find_illegal
from ascii_align import display_width

# ---------------------------------------------------------------------------
# Code block extraction
# ---------------------------------------------------------------------------

_FENCE_RE = re.compile(r"(```+)\n(.*?)\1", re.DOTALL)


def _extract_blocks(text: str) -> list[str]:
    return [m.group(2) for m in _FENCE_RE.finditer(text)]


# ---------------------------------------------------------------------------
# Round detection from filename prefix
# ---------------------------------------------------------------------------

_ROUND_PREFIXES = {
    "vvvvvv_": 6,
    "vvvvv_":  5,
    "vvvv_":   4,
    "vvv_":    3,
    "vv_":     2,
    "v_":      1,
    "_":       1,   # fallback
}


def _detect_round(name: str) -> int:
    for prefix, rnd in _ROUND_PREFIXES.items():
        if name.startswith(prefix):
            return rnd
    return 1


# ---------------------------------------------------------------------------
# Review prompt content
# ---------------------------------------------------------------------------

_REVIEW_RULES = """\
# ASCII Art LLM Review — Structural Checks

The programmatic width check has already passed (every │...│ row matches its hrule width).
Your job: catch structural issues the width checker cannot detect.

## Character Width Reference (Sarasa Mono TC)

- ASCII characters: 1 column each
- Box drawing (─│┌┐└┘├┤┬┴┼ etc.): 1 column each
- CJK characters (Chinese/Japanese/Korean): 2 columns each
- Full-width brackets （）: 2 columns each
- Degree ° / EN dash –: 1 column each

**Display column** = sum of character widths from the start of the line (col 0).

---

## Rule A: Vertical Connector Column Consistency

For `│` and `v` used as FLOW CONNECTORS between boxes (not as box left/right borders):
- All connector characters in the same flow path must stay in the **same display column** across consecutive rows.
- A connector `│` or `v` must align with the `┬` or `┴` junction it connects to (same display column).
- A connector `v` pointing INTO a box must be within the box's column span (between left `│` col and right `│` col of that box).
- **Corner vs junction rule**: When a box top has a junction line like `┌─────┴───┴┐`, the `v` connectors
  exiting the box align with the box **corners** (`┌` col and `┐` col), NOT with the internal `┴` junctions.
  The corners define the flow exit points, not the internal structure.

## Rule B: Structural Corruption

Lines where box structure appears broken:
- Inner box content spilling OUTSIDE its expected right border column (text after closing `│`)
- Box-drawing characters (└┘┌┐├┤┬┴┼) appearing at positions not consistent with any box above/below
- Lines where display width jumps by more than 5 columns with no structural reason

## Rule C: Parallel Box Connector/Gap Parity

When boxes are side by side with a connector row (e.g. `│────>│`) and gap rows (e.g. `│    │`):
- The connector display width must **equal** the gap display width between those same borders.
- Example: hrule `┐    ┌` has 4-char gap → the connector between those borders must also be exactly 4 display columns.

## Rule D: CJK Label Row Alignment

Label rows (lines with CJK text OUTSIDE box borders, typically below closing `└─┘` lines):
- Spaces after CJK text must account for **display width** (each CJK char = 2 cols, but 1 raw byte in column count).
- Verify: box-drawing chars (└ ┘ │) in a label row must align with the same character's display column in the bordered rows above/below.
- Common error: using `N` ASCII spaces after CJK text when `N-1` spaces are needed (because CJK occupies 2 cols but the programmer counted 1).
- Example (WRONG): `    可平行          └` — `可平行` takes 6 display cols but only 3 raw chars, so 10 ASCII spaces after it places `└` at display col 20 instead of 19.
- Example (RIGHT): `    可平行         └` — 9 ASCII spaces puts `└` at display col 19.

---

## Output Format

**If all checks pass**, output exactly:
```
PASS
```

**If issues found**, output each issue on its own line, then a blank line, then corrected lines:
```
FAIL
- L<N>: <Rule letter>: <description of the problem with display column numbers>
- L<N>: <Rule letter>: <description>

Corrections:
L<N>: `<corrected line content>`
L<N>: `<corrected line content>`
```

Only flag **clear violations**. If you are unsure whether something is intentional design, output PASS.
Do not re-check widths (already verified). Do not flag style issues.
"""


def gen_review_prompt(filepath: Path) -> str:
    """Return the LLM review prompt for a single file."""
    text = filepath.read_text(encoding="utf-8")
    blocks = _extract_blocks(text)

    if not blocks:
        return f"# No code blocks found in {filepath.name}\n"

    rnd = _detect_round(filepath.name)
    parts: list[str] = [_REVIEW_RULES]
    parts.append(f"---\n\n## File: {filepath.name}  (Review round {rnd})\n")

    for idx, content in enumerate(blocks):
        label = f"Block {idx + 1}" if len(blocks) > 1 else "Code Block"
        lines = content.split("\n")

        # Annotate lines with display column widths for the review agent
        annotated: list[str] = []
        for i, line in enumerate(lines):
            # Find box-border chars and their display columns
            col = 0
            border_info: list[str] = []
            for ch in line:
                w = display_width(ch)
                if ch in "│┌┐└┘├┤┬┴┼":
                    border_info.append(f"{ch}@{col}")
                col += w
            note = f"  [{', '.join(border_info[:6])}]" if border_info else ""
            annotated.append(f"L{i+1:3d}: {line}{note}")

        parts.append(f"### {label}\n")
        parts.append("```")
        parts.append(content)
        parts.append("```\n")
        parts.append("**Border positions (display columns):**")
        parts.append("```")
        parts.extend(annotated)
        parts.append("```\n")

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    args = sys.argv[1:]
    if not args:
        print("Usage: python llm_review.py <file.md> [<file2.md> ...]")
        sys.exit(1)

    paths: list[Path] = []
    for a in args:
        p = Path(a)
        if p.is_file() and p.suffix == ".md":
            paths.append(p)
        elif p.is_dir():
            # Pick up v_, vv_, vvv_ files pending review
            for prefix in ("vvv_", "vv_", "v_"):
                paths.extend(sorted(p.glob(f"{prefix}sample_*.md")))
        else:
            print(f"SKIP: {a}", file=sys.stderr)

    if not paths:
        print("No files to review.")
        sys.exit(0)

    for p in paths:
        prompt = gen_review_prompt(p)
        out = p.with_name(
            re.sub(r"^(v+)_", "", p.name)  # strip v/vv/vvv prefix
        ).with_suffix(".review.txt")
        out.write_text(prompt, encoding="utf-8", newline="\n")
        print(f"OK  {out.name}")


if __name__ == "__main__":
    main()
