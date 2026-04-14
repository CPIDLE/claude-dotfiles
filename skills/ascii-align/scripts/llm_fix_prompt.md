# ASCII Box Alignment — LLM Fix Prompt Template

## Usage

After running `ascii_align.py` (rule-based pass), generate this prompt for each
file that still has warnings or known residual issues. Feed it to Claude Code
or `/do deep`.

---

## Prompt Template

```
Fix the ASCII box-drawing alignment issues in the code block below.

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
   meaningful character and the right border (│┐┘┤). Hrule lines (─) lose
   1 dash.

2. **Inner box spacing**: Side-by-side inner boxes (┌─┐  ┌─┐) have wrong
   inter-box gap or the right box shifted. Fix: ensure consistent gap
   (typically 2-4 spaces) between ┘/┐ of left box and ┌/│ of right box,
   preserving total line width.

3. **Junction ─ count**: In lines like └──┬──┴──┬──┘, a segment between
   two junctions has 1 too many or too few ─. Fix: compare junction
   positions with the │ positions in adjacent content lines; adjust ─
   count so junctions align vertically with │ above/below.

4. **Branch connector displaced**: After ┌─────┼─────┐, the next line
   should show │ at each branch position. If │ are merged or shifted,
   restore them to align with the ┼ and the ┐ column above.

5. **Inner box content displaced**: Lines inside a nested box have massive
   leading whitespace pushing content right (line far wider than the box).
   Fix: remove the excess leading space so the content starts right after
   the inner box's left │, matching the ┌─┐ header and └─┘ footer width.

## Constraint

- Every line within the same box group MUST have identical display width.
- Only adjust spacing (trailing spaces, ─ fill counts). Never change text content.
- After fixing, the box should look visually correct in a monospace terminal.

## Diagnostics

{DIAGNOSTICS}

## File Content

{FILE_CONTENT}

Fix the issues described in the diagnostics. Output ONLY the corrected
code block content (between the ``` fences, not including the fences).
```

---

## Variable Substitution

- `{DIAGNOSTICS}`: Output of `ascii_align.py --check <file>`, plus any
  additional observations (e.g., "lines 17-19 are 113 cols wide, expected 63").
- `{FILE_CONTENT}`: Full content of the `.md` file.
