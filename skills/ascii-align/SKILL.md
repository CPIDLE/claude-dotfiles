---
name: ascii-align
description: >
  Fix ASCII-art box-drawing alignment in Markdown files using Sarasa Mono TC
  glyph widths. Per-block pipeline: auto-fix hrules -> check -> PASS (inject
  back) or FAIL (annotate + Claude manual fix -> re-check -> inject or report).
  Trigger when: /ascii-align, ASCII 對齊, 邊框對齊, box alignment.
argument-hint: "[path/to/file.md | path/to/dir]"
---

# ASCII Align — CJK-aware Box-Drawing Alignment

Fix right-border alignment in ASCII-art code blocks inside `.md` files,
using **pre-computed glyph widths** from Sarasa Mono TC (lookup table, no runtime font dependency).

## How to Use

### Automated (via `/ascii-align`)

Invoke as a slash command — handles extract → auto-fix → check → inject per block automatically. See **Workflow** section below.

### Manual / Advanced

```bash
# Lint only (no writes)
python "SKILL_DIR/scripts/ascii_align.py" --check <path>

# Auto-fix hrules in-place
python "SKILL_DIR/scripts/ascii_align.py" <path>

# Auto-fix + generate LLM diagnostic prompt
python "SKILL_DIR/scripts/ascii_align.py" --prompt <path>

# Extract blocks from a file to temp files
python "SKILL_DIR/scripts/extract_ascii_blocks.py" <file.md>

# Inject fixed block back into original file
python "SKILL_DIR/scripts/inject_ascii_block.py" <original.md> <block.md> <start> <end>
```

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

`SKILL_DIR` = directory containing this SKILL.md (installed: `~/.claude/skills/ascii-align`)

### Per-Block Pipeline

Parse `$ARGUMENTS` for target `.md` file(s); default to `*.md` in cwd.

For each target file, run `extract_ascii_blocks.py` to get JSON list of blocks.
Process **each block** (by `start`/`end` line numbers) as follows:

```
1. _<stem>_<start>_<end>.md already created by extract script

2. python SKILL_DIR/scripts/ascii_align.py  _<stem>_<start>_<end>.md
   (auto-fix hrules in-place)

3. rename: _<stem>_<start>_<end>.md  ->  v_<stem>_<start>_<end>.md

4. python SKILL_DIR/scripts/ascii_align.py --check  v_<stem>_<start>_<end>.md

   PASS:
     rename v_... -> p_<stem>_<start>_<end>.md
     python SKILL_DIR/scripts/inject_ascii_block.py <original> p_... <start> <end>
     delete p_<stem>_<start>_<end>.md

   FAIL:
     rename v_... -> x_<stem>_<start>_<end>.md
     write --check output to x_<stem>_<start>_<end>.txt

     Claude reads x_.md  +  x_.txt  and edits x_.md in-place to fix alignment

     python SKILL_DIR/scripts/ascii_align.py --check  x_<stem>_<start>_<end>.md

     PASS:
       python SKILL_DIR/scripts/inject_ascii_block.py <original> x_... <start> <end>
       delete x_.md  and  x_.txt

     FAIL:
       report failure (print x_.txt content, list specific lines)
       delete x_.md  and  x_.txt
```

### Notes

- Process blocks in **reverse line order** (last block first) so earlier block
  line numbers stay valid if block content length ever changes.
- Temp files live in the **same directory** as the original file.
- The `<!-- aa: TYPE -->` annotation line is preserved in the original;
  `inject_ascii_block.py` replaces only the fenced code block lines.

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
