---
name: ascii-align
description: >
  Scan Markdown files for ASCII-art code blocks and fix right-border alignment
  based on actual CJK glyph widths (Sarasa Mono TC). Two-step pipeline:
  linter (hrule fix + diagnostics) + Claude subagent for structural fixes.
  Trigger when: /ascii-align, ASCII 對齊, 邊框對齊, box alignment.
argument-hint: "[path/to/file.md | path/to/dir]"
---

# ASCII Align — CJK-aware Box-Drawing Alignment

Fix right-border alignment in ASCII-art code blocks inside `.md` files,
using **pre-computed glyph widths** from Sarasa Mono TC (lookup table, no runtime font dependency).

## How to Use

### Quick (linter only)

```bash
python "SKILL_DIR/scripts/ascii_align.py" [path ...]
```

- No argument → scan current directory for `*.md`
- File argument → process that single file
- Directory argument → scan that directory for `*.md`
- `--dry-run` / `--check` / `-n` → report without writing
- `--prompt` → apply safe fixes + generate rich diagnostic prompt for LLM subagent

### Full Pipeline (linter + LLM fix)

Run the 3-step pipeline for best results:

**Step 1** — Linter pass (hrule fix + diagnostics):
```bash
python "SKILL_DIR/scripts/ascii_align.py" --prompt <path>
```
Applies safe fixes (hrule `─` fill only) AND outputs a structured diagnostic
prompt for any remaining issues. Spawn a subagent with that prompt directly.

**Step 2** — Claude subagent fixes ALL structural issues guided by the diagnostic prompt.

**Step 3** — Verify:
```bash
python "SKILL_DIR/scripts/ascii_align.py" --check <path>
```
Pure verification. Reports any remaining issues without writing.
If warnings remain, retry Step 2 with the new warnings (max 1 retry).

## Width Rules (Sarasa Mono TC)

| Category | Examples | Cols | Source |
|----------|----------|------|--------|
| ASCII | `A-Z 0-9 +-=` | 1 | default |
| Box-drawing (all) | `─│├└┐┘┤┌┬┴┼═║━┃┏┓┗┛╞╘╪┊╱╲` | 1 | EAW=A but font w1 |
| CJK / fullwidth | `中（）【】` | 2 | EAW F/W |
| Arrows | `→←↑↓↔↕` | 2 | sarasa_widths.py override |
| Geometric | `▼▲►◄▶▸●○■□◆◇★☆` | 2 | sarasa_widths.py override |
| Check/cross | `✓✗✔✘` | 2 | sarasa_widths.py override |
| Math | `×÷±≤≥≠∞√≈∈∀∃∧∨` | 2 | sarasa_widths.py override |
| Greek | `Δαβθμπσ` (all Α-ω) | 2 | sarasa_widths.py override |
| Latin-1 punct | `· § ² ‖ •` | 2 | sarasa_widths.py override |
| EM dash / ellipsis | `—…` | 2 | sarasa_widths.py override |
| Block elements | `█` | 2 | sarasa_widths.py override |
| Confirmed w1 | `° – ╱ ╲` | 1 | EAW=A, calibrated narrow |

Width is resolved by: override table → EAW → default 1.

**Rule of thumb**: all EAW=Ambiguous characters render as **2 cols** in Sarasa Mono TC,
except Box Drawing (U+2500-257F) and a few Latin-1 (`°` `–`) which are w1.

## Symbol Mapping (Width-Stable Replacements)

When generating ASCII art inside `┌─┐`/`└─┘` bordered blocks, **prefer ASCII
equivalents** over Unicode to guarantee consistent alignment. Content outside
boxes (prose, comments with `←`) can keep Unicode for readability.

### Arrows (highest impact — 2000+ occurrences)

| Avoid | w | Use instead | w | Notes |
|-------|---|-------------|---|-------|
| `→` | 2 | `-->` | 3 | most common problem (1400+ uses) |
| `←` | 2 | `<--` | 3 | |
| `►` `▶` `▸` | 2 | `->` or `> ` | 2 | |
| `◄` | 2 | `<-` or `< ` | 2 | |
| `▲` | 2 | `^ ` | 2 | |
| `▼` | 2 | `v ` | 2 | 394 occurrences |
| `↔` | 2 | `<->` | 3 | |
| `↑` | 2 | `^ ` | 2 | |
| `↓` | 2 | `v ` | 2 | |

### Math / Logic

| Avoid | w | Use instead | w |
|-------|---|-------------|---|
| `×` | 2 | `x ` | 2 |
| `÷` | 2 | `/ ` | 2 |
| `±` | 2 | `+-` | 2 |
| `≤` | 2 | `<=` | 2 |
| `≥` | 2 | `>=` | 2 |
| `≠` | 2 | `!=` | 2 |
| `≈` | 2 | `~=` | 2 |
| `∈` | 2 | `in` | 2 |
| `∧` | 2 | `&&` | 2 |
| `∨` | 2 | `\|\|` | 2 |

### Symbols / Decorative

| Avoid | w | Use instead | w |
|-------|---|-------------|---|
| `·` | 2 | `. ` | 2 |
| `•` | 2 | `* ` | 2 |
| `●` | 2 | `* ` | 2 |
| `○` | 2 | `o ` | 2 |
| `■` | 2 | `# ` | 2 |
| `★` | 2 | `* ` | 2 |
| `✓` | 2 | `OK` or `v ` | 2 |
| `✗` | 2 | `NG` or `x ` | 2 |
| `§` | 2 | `S.` | 2 |
| `²` | 2 | `^2` | 2 |
| Greek `α` etc. | 2 | spell out or `a ` | 2 |

### Safe to use (confirmed w1 in Sarasa Mono TC)

These can appear inside boxes without alignment issues:
- All Box Drawing: `─│┌┐└┘├┤┬┴┼═║━┃┏┓┗┛╞╘╪┊╱╲`
- Degree: `°`
- EN dash: `–`

## Type Annotation & Auto-Detection

Each code block gets a **type** that determines the alignment strategy:

| Type | Detection | Linter Strategy |
|------|-----------|-----------------|
| `single` | Default (one box) | Hrule fill |
| `nested` | Via `<!-- aa: nested -->` | Hrule fill |
| `parallel` | ≥2 `│...│` segments per line with gap | Hrule fill |
| `flow` | Arrow chars (→↓) on non-border lines | Hrule fill |
| `layout` | Via `<!-- aa: layout -->` | Hrule fill |
| `table` | Lines with `┼` junctions | Skip entirely |

**Annotation** (highest priority): `<!-- aa: TYPE -->` above the code fence.
**Auto-detect** (fallback): heuristics based on block content.

All types get hrule fill only from the linter. Content padding, inner box
alignment, and structural fixes are the LLM subagent's responsibility.

## Linter Capabilities

### What the Linter Handles (safe, automatic)
- Detecting and classifying ASCII art blocks (type, groups, inner boxes)
- Computing display widths (Sarasa Mono TC glyph table)
- Fixing hrule `─` fill in `┌─┐`/`└─┘` lines
- Reporting all width mismatches, inner box misalignment, off-by-1 issues
- Generating rich diagnostic prompt for the LLM subagent

### What the LLM Subagent Handles (guided by diagnostics)
- **Content padding**: adjusting spaces between content and right border `│`
- **Inner box alignment**: nested `┌─┐`/`└─┘` border columns
- **Off-by-1 width**: majority has 1 extra trailing space (semantic judgment)
- **Parallel box spacing**: individual box width within side-by-side layouts
- **Branch connector alignment**: `│` columns after `┌─┼─┐`

## Diagnostic Prompt Format

The `--prompt` flag generates a structured diagnostic for each file with issues:

```
=== LLM FIX PROMPT for <filepath> ===

## Width Rules
[font and width rules]

## Principles
[alignment rules and conservative principle]

## Block N: L70-L91 (type: single)

### Group 1: L70-L85 (target_width: 69)
OK lines: L70, L71, L73, L74, L76-L84
Fix lines:
  - L72: w=70 (+1). "│  ┌──────────┐    │"
  - L85: w=113 (+44). "│  │ subitem  │    ... │"

### Inner box at L72 (┌@col 4, ┐@col 18)
Expected right border at col 18:
  L73: │@col 19 (+1)
  L75: ┘@col 19 (+1)

### Off-by-1
  ⚠ L70-L85: off-by-1 (group w=69, bottom w=68)

File to fix: <abs_path>
Verify: python ascii_align.py --check "<abs_path>"
===
```

## Workflow

1. Parse `$ARGUMENTS` for target path(s); default to `.`
2. Run `ascii_align.py --prompt` (Step 1 — hrule fix + diagnostic prompt)
3. If prompt output exists → spawn Claude subagent with that prompt (Step 2)
4. Run `ascii_align.py --check` (Step 3 — verify)
5. If warnings remain → retry Step 2 once with new warnings
6. Report final results

## Output

```
Fixed: example.md
  L70-L91: 15 lines aligned to w=69
Lint: another.md
  ⚠ L85: w=113 expected w=69
  ⚠ L72: inner │@19 expected @18
OK: clean.md (already aligned)
Skipped: README.md (no bordered blocks)

Summary: 1 files changed, 1 blocks fixed, 2 warnings
```
