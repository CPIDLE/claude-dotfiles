---
name: ascii-align
description: >
  Scan Markdown files for ASCII-art code blocks and fix right-border alignment
  based on actual CJK glyph widths (Sarasa Mono TC). Two-step pipeline:
  rule-based engine + Claude subagent for structural fixes.
  Trigger when: /ascii-align, ASCII 對齊, 邊框對齊, box alignment.
argument-hint: "[path/to/file.md | path/to/dir]"
---

# ASCII Align — CJK-aware Box-Drawing Alignment

Fix right-border alignment in ASCII-art code blocks inside `.md` files,
using **pre-computed glyph widths** from Sarasa Mono TC (lookup table, no runtime font dependency).

## How to Use

### Quick (rule-based only)

```bash
python "SKILL_DIR/scripts/ascii_align.py" [path ...]
```

- No argument → scan current directory for `*.md`
- File argument → process that single file
- Directory argument → scan that directory for `*.md`
- `--dry-run` / `--check` / `-n` → report without writing
- `--prompt` → dry-run + generate LLM fix prompt for residual issues

### Full Pipeline (rule-based + LLM fix)

Run the 3-step pipeline for best results:

**Step 1** — Rule-based pass:
```bash
python "SKILL_DIR/scripts/ascii_align.py" <path>
```

**Step 1+2 combined** — Rule-based align + subagent prompt generation:
```bash
python "SKILL_DIR/scripts/ascii_align.py" --prompt <path>
```
Aligns the file (writes changes) AND outputs a structured prompt for any
residual issues. Spawn a subagent with that prompt directly.
If `--prompt` is not used, craft a manual prompt that MUST include:
- Display width rules (see table below)
- Relative alignment rules (same column, not absolute numbers)
- Specific line numbers and what's wrong
- The file path to read and edit

**Step 3** — Re-align (fix any width errors from LLM):
```bash
python "SKILL_DIR/scripts/ascii_align.py" <path>
```

## Width Rules (Sarasa Mono TC)

| Category | Examples | Cols | Source |
|----------|----------|------|--------|
| ASCII | `A-Z 0-9 +-=` | 1 | default |
| Box-drawing | `─│├└┐┘┤┌┬┴┼` | 1 | sarasa_widths.py override |
| CJK / fullwidth | `中（）【】` | 2 | EAW F/W |
| Arrows | `→←↑↓↔` | 2 | sarasa_widths.py override |
| Geometric | `▼▲●○■□◆` | 2 | sarasa_widths.py override |
| EM dash / ellipsis | `—…` | 2 | sarasa_widths.py override |

Width is resolved by: override table → EAW → default 1.

## Rule-Based Alignment Logic

### Step 1: Connect (majority width)
1. Find code blocks (```` ``` ```` to ```` ``` ````) containing right-border chars (`│┐┘┤`)
2. Group contiguous bordered lines; `└┘` terminates the group
3. Compute majority width (most common display width in the group)
4. Expand/shrink all lines to majority width

### Step 2: Shrink (spread > 5)
If the spread (majority - min width) exceeds 5, the majority is likely wrong
(massive trailing padding). Use min width instead — typically the `└┘` bottom
line which has no trailing-space ambiguity.

### What Rule-Based Handles
- Connecting broken `└┘` / `┌┐` to group width
- Fixing hrule `─` fill counts
- Padding content lines to uniform width
- Inner box alignment (nested `┌─┐` / `└─┘`)

### What Rule-Based Cannot Handle (→ Step 2 LLM)
- **Off-by-1 width**: majority has 1 extra trailing space (detected by `--check` as `off-by-1` warning, needs semantic judgment to fix)
- **Inner box spacing**: side-by-side boxes with wrong inter-box gap
- **Branch connector displacement**: `│` after `┌─┼─┐` at wrong columns
- **Content displacement**: nested box content with massive leading whitespace

## Subagent Prompt Guidelines

When spawning a Claude subagent for Step 2, include:

```
Font: Sarasa Mono TC.
Display width: box-drawing (─│├┐┘┤┌┬┴┼) = 1 col,
arrows (▼▲→←) = 2 cols, geometric (●○■□◆) = 2 cols.

Rules:
- Every line in a box group must have identical display width
- Only adjust spacing. Never change text content.
- ▼/→ must start at same column as │ above it
- Junction (┬┴┼) must align vertically with │ in content lines
```

Then describe the **specific issues** with line numbers. Do NOT use generic prompts — precision is critical.

## Output

```
Fixed: example.md
  L70-L91: 15 lines aligned to w=69
  ⚠ L85: w=113 expected w=69
Skipped: README.md (no bordered blocks)

Summary: 2 files changed, 3 blocks fixed, 1 warning
```

## Workflow

1. Parse `$ARGUMENTS` for target path(s); default to `.`
2. Run `ascii_align.py --prompt` (Step 1 — rule-based align + generate subagent prompt if residuals exist)
3. If prompt output exists → spawn Claude subagent with that prompt (Step 2)
4. Re-run `ascii_align.py` (Step 3 — re-align after LLM)
5. Report final results
