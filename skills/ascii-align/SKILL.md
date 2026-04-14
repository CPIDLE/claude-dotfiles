---
name: ascii-align
description: >
  Scan Markdown files for ASCII-art code blocks and fix right-border alignment
  based on actual CJK glyph widths (Sarasa Mono TC). Adjusts padding so that
  box-drawing borders (│┐┘┤) line up correctly when rendered in a fixed-width
  CJK font. Trigger when: /ascii-align, ASCII 對齊, 邊框對齊, box alignment.
argument-hint: "[path/to/file.md | path/to/dir]"
---

# ASCII Align — CJK-aware Box-Drawing Alignment

Fix right-border alignment in ASCII-art code blocks inside `.md` files,
using **actual glyph widths** from Sarasa Mono TC (not `unicodedata.east_asian_width`).

## Dependency

```bash
pip install fonttools
```

## How to Use

Run the Python helper via Bash:

```bash
python "SKILL_DIR/scripts/ascii_align.py" [path ...]
```

- No argument → scan current directory for `*.md` (non-recursive)
- File argument → process that single file
- Directory argument → scan that directory for `*.md` (non-recursive)
- `--dry-run` / `--check` / `-n` → report changes without writing files

## Width Rules (Sarasa Mono TC)

| Category | Examples | Cols | Note |
|----------|----------|------|------|
| ASCII | `A-Z 0-9 +-=` | 1 | |
| Box-drawing | `─│├└┐┘┤┌┬┴┼` | 1 | EAW=A but font=half-width |
| CJK / fullwidth | `中（）【】` | 2 | |
| Arrows | `→←↑↓` | 2 | EAW=A but font=full-width |
| Geometric | `▼▲►◄●○` | 2 | EAW=A but font=full-width |

The script reads the font's `hmtx` table: advance width ≥ 750 → 2 cols, else fallback to EAW.

## Alignment Logic

1. Find code blocks (`` ``` `` to `` ``` ``) containing right-border chars (`│┐┘┤`)
2. Group lines that belong to the same box (contiguous bordered lines)
3. Target width = max(content display width across group) + border char width
4. `─┐` / `─┘` lines: horizontal rule runs directly into corner (no trailing space)
5. `│` / `┤` lines: pad content with spaces to reach target width
6. Verify all lines in the group have equal `display_width`

## Multi-Box Handling

When a single code block contains multiple independent boxes (separated by
non-bordered lines), each box is aligned independently — they are NOT merged.

## Tree Trunk Exclusion

Standalone `│` lines that are NOT part of a box border group (e.g., tree
diagrams like `│  Stage 1: ...`) are excluded from alignment.

## Output

```
Fixed: GYRO_決策版.md
  L70-L91: 15 lines aligned to w=69
  L111-L126: 11 lines aligned to w=52
Skipped: README.md (no bordered blocks)

Summary: 2 files changed, 3 blocks fixed
```

## Workflow

1. Parse `$ARGUMENTS` for target path(s); default to `.`
2. Run the script
3. Report results to the user
