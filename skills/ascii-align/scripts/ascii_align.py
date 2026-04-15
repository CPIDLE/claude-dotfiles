#!/usr/bin/env python3
"""ascii_align.py — Fix right-border alignment in ASCII-art code blocks.

Uses actual glyph widths from Sarasa Mono TC (fontTools) instead of
unicodedata.east_asian_width, which misclassifies arrows and geometric
symbols as narrow when the font renders them full-width.

Usage:
    python ascii_align.py [path ...]
    - No args   → scan cwd for *.md
    - File arg  → process that file
    - Dir arg   → scan that dir for *.md
"""

from __future__ import annotations

import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

from sarasa_widths import WIDE_OVERRIDES, NARROW_OVERRIDES

# ---------------------------------------------------------------------------
# Width engine — lookup table, no fontTools needed at runtime
# ---------------------------------------------------------------------------

_cache: dict[int, int] = {}

RIGHT_BORDER = set("│┐┘┤")
HORIZONTAL_CORNERS = set("┐┘")
HORIZONTAL_RULE = "─"
# Left-side chars that start a horizontal rule line (paired with ┤ on the right)
HORIZONTAL_LEFT = set("├┬┴┼")


def char_cols(c: str) -> int:
    """Return display column count for a single character.

    Priority: override table → EAW → default 1.
    The override table captures Sarasa Mono TC glyphs that disagree with EAW.
    """
    cp = ord(c)
    if cp in _cache:
        return _cache[cp]

    if cp in WIDE_OVERRIDES:
        cols = 2
    elif cp in NARROW_OVERRIDES:
        cols = 1
    elif unicodedata.east_asian_width(c) in ("F", "W"):
        cols = 2
    else:
        cols = 1

    _cache[cp] = cols
    return cols


def display_width(s: str) -> int:
    """Return total display column width of string *s*."""
    return sum(char_cols(c) for c in s)


# ---------------------------------------------------------------------------
# Box detection & alignment
# ---------------------------------------------------------------------------

def _is_bordered(line: str) -> bool:
    """True if line ends with a right-border character (ignoring trailing whitespace)."""
    stripped = line.rstrip()
    return bool(stripped) and stripped[-1] in RIGHT_BORDER


def _is_tree_trunk(line: str) -> bool:
    """Heuristic: a standalone │ not part of a box border.

    A line is a tree trunk if the only non-whitespace character is a trailing │.
    E.g. "                │" is a tree trunk, "  │ content │" is not.
    """
    stripped = line.rstrip()
    if not stripped or stripped[-1] != "│":
        return False
    return stripped[:-1].strip() == ""


def _find_box_groups(block_lines: list[str]) -> list[list[int]]:
    """Find groups of contiguous bordered lines (excluding tree trunks).

    Returns list of groups, where each group is a list of line indices
    within the block.
    """
    groups: list[list[int]] = []
    current: list[int] = []

    for i, line in enumerate(block_lines):
        if _is_bordered(line) and not _is_tree_trunk(line):
            stripped = line.rstrip()
            starts_with_bottom = stripped.lstrip()[0] == "└" if stripped.lstrip() else False
            ends_with_bottom = stripped[-1] == "┘"
            current.append(i)
            # Box bottom terminates the group — don't absorb lines after it.
            if ends_with_bottom or starts_with_bottom:
                groups.append(current)
                current = []
        else:
            if current:
                groups.append(current)
                current = []
    if current:
        groups.append(current)

    # Filter out groups that are too small or don't have structural variety
    # (a real box should have at least a top/bottom + content, or corners)
    return [g for g in groups if len(g) >= 2]


def _is_hrule_line(content: str, border: str) -> bool:
    """Detect if a line is a horizontal-rule line.

    A horizontal-rule line is one where:
    - border is ┐ or ┘ (always hrule), OR
    - border is ┤ and the content (stripped) is entirely made of ─ and
      box-drawing junction chars (├┬┴┼─┌┐└┘│┤), with ─ being dominant.
    """
    if border in HORIZONTAL_CORNERS:
        return True
    if border != "┤":
        return False
    # For ┤: check if content is a horizontal rule (├───┬───)
    clean = content.strip()
    if not clean:
        return False
    # Must start with a left-side junction or ─
    if clean[0] not in HORIZONTAL_LEFT and clean[0] != HORIZONTAL_RULE:
        return False
    # All chars must be box-drawing or ─
    hrule_chars = set("─├┬┴┼┌┐└┘│┤")
    return all(c in hrule_chars for c in clean)


def _align_group(block_lines: list[str], group: list[int]) -> list[str]:
    """Align a single box group to uniform display width.

    Two-step strategy:
      Step 1 (connect): expand short lines to majority width so all borders
             connect (└┘ matches ┌┐, etc.).
      Step 2 (shrink):  compute the minimum width that fits all content
             (meat + 1 space + border), then shrink the whole group to that
             width.  Only the trailing gap between the last meaningful
             character and the right border is adjusted — content to the
             left is never touched.

    Returns the modified block_lines (mutated in place).
    """
    # Parse each line
    parsed: list[tuple[str, str, bool]] = []
    for i in group:
        stripped = block_lines[i].rstrip()
        border = stripped[-1]
        content = stripped[:-1]
        hrule = _is_hrule_line(content, border)
        parsed.append((content, border, hrule))

    # --- Step 1: connect — pick target width --------------------------------
    line_widths: list[int] = []
    for idx in range(len(parsed)):
        line_widths.append(display_width(block_lines[group[idx]].rstrip()))

    width_counts = Counter(line_widths)
    majority_w = width_counts.most_common(1)[0][0]
    min_w = min(line_widths)
    spread = majority_w - min_w

    # Large spread (>5) means most content lines have excessive trailing
    # padding — shrink to the minimum (typically the └┘ bottom line, which
    # has no trailing-space ambiguity).  Small spread is usually an off-by-
    # one in the └┘ hrule fill — majority is more reliable.
    target_w = min_w if spread > 5 else majority_w

    # Rebuild each line — only adjust right-side gap
    for idx, i in enumerate(group):
        content, border, hrule = parsed[idx]
        border_w = char_cols(border)

        cur_w = display_width(block_lines[group[idx]].rstrip())

        if cur_w == target_w:
            continue  # already correct width, don't touch

        if hrule:
            # Hrule: find structural prefix (everything before trailing ─),
            # then fill ─ to reach target width.
            content_clean = content.rstrip()
            prefix = content_clean.rstrip(HORIZONTAL_RULE)
            prefix_w = display_width(prefix)
            fill_count = target_w - prefix_w - border_w
            if fill_count < 1:
                fill_count = 1
            new_line = prefix + (HORIZONTAL_RULE * fill_count) + border
        else:
            # Content: preserve everything left of the trailing gap.
            # Only adjust the spaces between last meaningful char and border.
            content_meat = content.rstrip()
            meat_w = display_width(content_meat)
            gap = target_w - meat_w - border_w
            if gap < 1:
                gap = 1
            new_line = content_meat + (" " * gap) + border

        if new_line != block_lines[i].rstrip():
            block_lines[i] = new_line

    return block_lines


# ---------------------------------------------------------------------------
# Inner box alignment
# ---------------------------------------------------------------------------

def _col_at(line: str, char_idx: int) -> int:
    """Display column where character at char_idx starts."""
    return sum(char_cols(line[i]) for i in range(char_idx))


def _char_idx_at_col(line: str, target_col: int) -> int | None:
    """Find character index whose display column == target_col. None if no match."""
    col = 0
    for i, c in enumerate(line):
        if col == target_col:
            return i
        col += char_cols(c)
        if col > target_col:
            return None
    return None


def _find_inner_boxes(block_lines: list[str]) -> list[tuple[int, int, int]]:
    """Find inner box headers (┌...┐ enclosed within another box's │...│ line).

    A ┌...┐ is "inner" only if:
    1. The line has a │ at a lower column (enclosing box's left border)
    2. No ┬ between ┌ and ┐ (otherwise it's a multi-column table header)

    Returns list of (left_col, right_col, line_idx) where left_col/right_col
    are the display columns of ┌ and ┐ respectively.
    """
    results = []
    for i, line in enumerate(block_lines):
        col = 0
        has_leading_pipe = False
        for ci, c in enumerate(line):
            if c == "│":
                has_leading_pipe = True
            if c == "┌" and has_leading_pipe:
                left_col = col
                # Scan forward for matching ┐, reject if ┬ found (table header)
                right_col = col + char_cols(c)
                has_junction = False
                for cj in range(ci + 1, len(line)):
                    if line[cj] == "┬":
                        has_junction = True
                        break
                    if line[cj] == "┐":
                        if not has_junction:
                            results.append((left_col, right_col, i))
                        break
                    right_col += char_cols(line[cj])
                # No ┐ found → malformed header, skip
            col += char_cols(c)
    return results


def _align_inner_boxes(block_lines: list[str]) -> bool:
    """Align inner boxes: parse structure → content decides width → redraw.

    Iteratively processes one box at a time, re-scanning after each fix
    because modifying one inner box can shift column positions of others
    on the same line.
    """
    changed = False
    max_iter = 20
    for _iteration in range(max_iter):
        inner_boxes = _find_inner_boxes(block_lines)
        if not inner_boxes:
            break
        any_fixed = False
        for left_col, header_right_col, header_idx in inner_boxes:
            if _align_one_inner_box(block_lines, left_col, header_right_col, header_idx):
                any_fixed = True
                changed = True
                break  # re-scan — positions may have shifted
        if not any_fixed:
            break  # all boxes aligned
    else:
        print(f"WARNING: inner box iteration limit ({max_iter}) reached", file=sys.stderr)
    return changed


def _align_one_inner_box(
    block_lines: list[str], left_col: int, header_right_col: int, header_idx: int
) -> bool:
    """Process a single inner box. Returns True if any changes made."""
    changed = False

    # --- Phase 1: Collect box structure ---
    content_info: list[tuple[int, int, int, str, int]] = []
    footer_idx: int | None = None
    footer_left_ci: int | None = None
    footer_right_ci: int | None = None

    for li in range(header_idx + 1, len(block_lines)):
        line = block_lines[li]
        left_ci = _char_idx_at_col(line, left_col)
        if left_ci is None or left_ci >= len(line):
            break
        lchar = line[left_ci]

        if lchar == "└":
            scan_col = left_col + char_cols(lchar)
            for cj in range(left_ci + 1, len(line)):
                if line[cj] == "┘":
                    footer_idx = li
                    footer_left_ci = left_ci
                    footer_right_ci = cj
                    break
                scan_col += char_cols(line[cj])
            break

        if lchar != "│":
            break

        # Find right │
        scan_col = left_col + char_cols(lchar)
        right_ci = None
        for cj in range(left_ci + 1, len(line)):
            if line[cj] == "│":
                right_ci = cj
                break
            scan_col += char_cols(line[cj])

        if right_ci is None:
            break

        inner_text = line[left_ci + 1 : right_ci]
        cs = inner_text.rstrip()
        cw = display_width(cs)
        content_info.append((li, left_ci, right_ci, cs, cw))

    if not content_info:
        return False

    # --- Phase 2: Compute target box width ---
    # Desired width based on content
    max_content_w = max(cw for _, _, _, _, cw in content_info)
    desired_inner_space = max_content_w + 1
    desired_right_col = left_col + char_cols("│") + desired_inner_space

    # Constraint: don't expand beyond available gap on any line.
    # The gap is the space between the current inner right │ and the next
    # non-space character (typically outer mid │). Expansion must not push it.
    max_expansion = 999
    # Check header line
    hline = block_lines[header_idx]
    h_left_ci = _char_idx_at_col(hline, left_col)
    if h_left_ci is not None:
        for cj in range(h_left_ci + 1, len(hline)):
            if hline[cj] == "┐":
                after_corner = hline[cj + 1:]
                gap_spaces = len(after_corner) - len(after_corner.lstrip(" "))
                avail = gap_spaces - 1  # keep at least 1 space
                if avail < max_expansion:
                    max_expansion = avail
                break
    # Check content lines
    for li, left_ci, right_ci, cs, cw in content_info:
        line = block_lines[li]
        after = line[right_ci + 1:]
        gap_spaces = len(after) - len(after.lstrip(" "))
        avail = gap_spaces - 1
        if avail < max_expansion:
            max_expansion = avail
    # Check footer
    if footer_idx is not None and footer_right_ci is not None:
        fline = block_lines[footer_idx]
        after_f = fline[footer_right_ci + 1:]
        gap_spaces = len(after_f) - len(after_f.lstrip(" "))
        avail = gap_spaces - 1
        if avail < max_expansion:
            max_expansion = avail

    # Never shrink: respect existing box width (max of header and all content lines)
    existing_max_right = header_right_col
    for li, left_ci, right_ci, cs, cw in content_info:
        actual_right = _col_at(block_lines[li], right_ci)
        if actual_right > existing_max_right:
            existing_max_right = actual_right
    if footer_idx is not None and footer_right_ci is not None:
        actual_foot_right = _col_at(block_lines[footer_idx], footer_right_ci)
        if actual_foot_right > existing_max_right:
            existing_max_right = actual_foot_right

    # Target = max(content-based, existing) → never shrink
    desired_right_col = max(desired_right_col, existing_max_right)

    # Limit expansion beyond existing to available gap
    current_right_col = existing_max_right
    expansion_needed = desired_right_col - current_right_col
    if expansion_needed > 0 and max_expansion < expansion_needed:
        if max_expansion <= 0:
            new_right_col = current_right_col
        else:
            new_right_col = current_right_col + max_expansion
    else:
        new_right_col = desired_right_col

    inner_space = new_right_col - left_col - char_cols("│")

    if new_right_col == header_right_col:
        all_ok = True
        for li, left_ci, right_ci, cs, cw in content_info:
            actual_right = _col_at(block_lines[li], right_ci)
            if actual_right != new_right_col:
                all_ok = False
                break
        # Also check footer
        if all_ok and footer_idx is not None and footer_right_ci is not None:
            actual_foot = _col_at(block_lines[footer_idx], footer_right_ci)
            if actual_foot != new_right_col:
                all_ok = False
        if all_ok:
            return False

    # --- Phase 3: Redraw header ---
    hline = block_lines[header_idx]
    h_left_ci = _char_idx_at_col(hline, left_col)
    if h_left_ci is not None:
        h_right_ci = None
        for cj in range(h_left_ci + 1, len(hline)):
            if hline[cj] == "┐":
                h_right_ci = cj
                break
        if h_right_ci is not None:
            orig_w = display_width(hline.rstrip())
            before_h = hline[:h_left_ci]
            after_h = hline[h_right_ci + 1:]

            header_inner = hline[h_left_ci + 1 : h_right_ci]
            label_part = header_inner.rstrip(HORIZONTAL_RULE)
            label_w = display_width(label_part)
            fill = new_right_col - left_col - char_cols("┌") - label_w
            if fill < 1:
                fill = 1
            new_header = "┌" + label_part + (HORIZONTAL_RULE * fill) + "┐"

            new_h_core = before_h + new_header
            after_h_content = after_h.lstrip(" ")
            after_h_w = display_width(after_h_content)
            h_gap = orig_w - display_width(new_h_core) - after_h_w
            if h_gap < 1:
                h_gap = 1
            new_hline = new_h_core + (" " * h_gap) + after_h_content
            if new_hline != hline.rstrip():
                block_lines[header_idx] = new_hline
                changed = True

    # --- Phase 4: Redraw content lines ---
    for li, left_ci, right_ci, cs, cw in content_info:
        line = block_lines[li]
        orig_w = display_width(line.rstrip())

        before = line[:left_ci]
        after = line[right_ci + 1:]

        pad = inner_space - cw
        if pad < 0:
            continue  # content overflows — skip this line
        new_inner = "│" + cs + (" " * pad) + "│"

        new_core = before + new_inner
        after_content = after.lstrip(" ")
        after_w = display_width(after_content)
        gap = orig_w - display_width(new_core) - after_w
        if gap < 1:
            gap = 1
        new_line = new_core + (" " * gap) + after_content
        if new_line != line.rstrip():
            block_lines[li] = new_line
            changed = True

    # --- Phase 5: Redraw footer ---
    if footer_idx is not None and footer_left_ci is not None and footer_right_ci is not None:
        fline = block_lines[footer_idx]
        orig_w = display_width(fline.rstrip())
        before_f = fline[:footer_left_ci]
        after_f = fline[footer_right_ci + 1:]

        f_fill = new_right_col - left_col - char_cols("└")
        if f_fill < 1:
            f_fill = 1
        new_footer = "└" + (HORIZONTAL_RULE * f_fill) + "┘"

        new_f_core = before_f + new_footer
        after_f_content = after_f.lstrip(" ")
        after_f_w = display_width(after_f_content)
        f_gap = orig_w - display_width(new_f_core) - after_f_w
        if f_gap < 1:
            f_gap = 1
        new_fline = new_f_core + (" " * f_gap) + after_f_content
        if new_fline != fline.rstrip():
            block_lines[footer_idx] = new_fline
            changed = True

    return changed


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------

def _verify_inner_boxes(block_lines: list[str], line_offset: int) -> list[str]:
    """Verify all inner boxes have consistent border columns. Returns warnings."""
    warnings: list[str] = []
    inner_boxes = _find_inner_boxes(block_lines)

    for left_col, right_col, header_idx in inner_boxes:
        expected_right = right_col
        for li in range(header_idx + 1, len(block_lines)):
            line = block_lines[li]
            left_ci = _char_idx_at_col(line, left_col)
            if left_ci is None or left_ci >= len(line):
                break
            lchar = line[left_ci]
            if lchar not in "│└":
                break

            target_char = "┘" if lchar == "└" else "│"
            scan_col = left_col + char_cols(lchar)
            for cj in range(left_ci + 1, len(line)):
                if line[cj] == target_char:
                    if scan_col != expected_right:
                        actual_line = line_offset + li + 1
                        warnings.append(
                            f"  ⚠ L{actual_line}: inner {target_char}@{scan_col} "
                            f"expected @{expected_right}"
                        )
                    break
                scan_col += char_cols(line[cj])

            if lchar == "└":
                break

    return warnings


def _verify_group_widths(
    block_lines: list[str], groups: list[list[int]], line_offset: int
) -> list[str]:
    """Verify that all lines within each box group have the same display width."""
    warnings: list[str] = []
    for group in groups:
        widths: dict[int, list[int]] = {}
        for i in group:
            w = display_width(block_lines[i].rstrip())
            widths.setdefault(w, []).append(i)
        if len(widths) > 1:
            main_w = max(widths, key=lambda w: len(widths[w]))
            for w, idxs in widths.items():
                if w != main_w:
                    for idx in idxs:
                        warnings.append(
                            f"  ⚠ L{line_offset + idx + 1}: w={w} expected w={main_w}"
                        )
    return warnings


def _check_off_by_1(
    block_lines: list[str], groups: list[list[int]], line_offset: int
) -> list[str]:
    """Detect off-by-1: majority width = bottom hrule width + 1.

    Must be called on ORIGINAL lines before alignment, since alignment
    equalizes all widths. Only fires when spread <= 5 (rule engine picks
    majority), because spread > 5 already shrinks to min.
    """
    warnings: list[str] = []
    for group in groups:
        widths = [display_width(block_lines[i].rstrip()) for i in group]
        width_counts = Counter(widths)
        majority_w = width_counts.most_common(1)[0][0]
        min_w = min(widths)
        spread = majority_w - min_w

        if spread > 5 or spread == 0:
            continue

        # Bottom lines (┘) have no trailing-space ambiguity
        bottom_ws = []
        for i in group:
            stripped = block_lines[i].rstrip()
            if stripped and stripped[-1] == "┘":
                bottom_ws.append(display_width(stripped))

        if not bottom_ws:
            continue

        bottom_w = min(bottom_ws)
        if majority_w - bottom_w == 1:
            first = line_offset + group[0] + 1
            last = line_offset + group[-1] + 1
            warnings.append(
                f"  ⚠ L{first}-L{last}: off-by-1 "
                f"(group w={majority_w}, bottom w={bottom_w})"
            )
    return warnings


def _print_llm_prompt(filepath: Path, warnings: list[str]) -> None:
    """Print a structured prompt for Claude subagent to fix residual issues."""
    abs_path = filepath.resolve()
    print(f"=== LLM FIX PROMPT for {filepath} ===")
    print(
        "Font: Sarasa Mono TC.\n"
        "Display width: box-drawing (─│├┐┘┤┌┬┴┼) = 1 col,\n"
        "arrows (▼▲→←) = 2 cols, geometric (●○■□◆) = 2 cols.\n"
        "\n"
        "Rules:\n"
        "- Every line in a box group must have identical display width\n"
        "- Only adjust spacing. Never change text content.\n"
        "- ▼/→ must start at same column as │ above it\n"
        "- Junction (┬┴┼) must align vertically with │ in content lines\n"
        "\n"
        "Issues found:"
    )
    for w in warnings:
        print(w)
    print(f"\nFile to fix: {abs_path}")
    print("Read the file, fix the issues above, then save.")
    print("===")


# ---------------------------------------------------------------------------
# File processing
# ---------------------------------------------------------------------------

# CommonMark: fence must start with 0-3 spaces of indentation
_FENCE_RE = re.compile(r"^ {0,3}```")


def process_file(filepath: Path, *, dry_run: bool = False) -> tuple[list[str], list[str], bool]:
    """Process a single .md file. Returns (changes, warnings, has_boxes)."""
    text = filepath.read_text(encoding="utf-8")
    lines = text.split("\n")

    changes: list[str] = []
    all_warnings: list[str] = []
    has_boxes = False
    in_block = False
    block_start = -1

    # Collect all code blocks first
    blocks: list[tuple[int, int]] = []  # (start, end) inclusive of fences
    for i, line in enumerate(lines):
        if _FENCE_RE.match(line):  # match raw line, not stripped
            if not in_block:
                in_block = True
                block_start = i
            else:
                blocks.append((block_start, i))
                in_block = False

    modified = False
    for bstart, bend in blocks:
        # Extract inner lines (excluding fences)
        inner_start = bstart + 1
        inner_end = bend  # exclusive
        if inner_start >= inner_end:
            continue

        block_lines = lines[inner_start:inner_end]

        # Check if block has any bordered lines
        has_borders = any(_is_bordered(l) for l in block_lines)
        if not has_borders:
            continue
        has_boxes = True

        groups = _find_box_groups(block_lines)
        if not groups:
            continue

        # Snapshot for comparison
        original = [l for l in block_lines]

        # Pre-alignment: detect off-by-1 on original widths
        off_by_1 = _check_off_by_1(block_lines, groups, inner_start)

        # Phase 1: align inner boxes first (adjusts content within lines)
        _align_inner_boxes(block_lines)

        # Phase 2: align outer box borders
        # Re-detect groups after inner box changes (line widths may have changed)
        groups = _find_box_groups(block_lines)
        for group in groups:
            _align_group(block_lines, group)

        # Phase 3: verify alignment
        warnings = _verify_inner_boxes(block_lines, inner_start)
        warnings += _verify_group_widths(block_lines, groups, inner_start)

        # Check if anything changed
        if block_lines != original:
            # Write back
            lines[inner_start:inner_end] = block_lines
            for group in groups:
                first_line = inner_start + group[0] + 1
                last_line = inner_start + group[-1] + 1
                count = len(group)
                w = display_width(block_lines[group[0]].rstrip())
                changes.append(f"  L{first_line}-L{last_line}: {count} lines aligned to w={w}")
            all_warnings.extend(warnings)
            modified = True

        # Off-by-1 warnings apply regardless of whether alignment changed lines
        all_warnings.extend(off_by_1)

    if modified and not dry_run:
        filepath.write_text("\n".join(lines), encoding="utf-8")

    return changes, all_warnings, has_boxes


def main() -> None:

    # Parse flags
    dry_run = False
    prompt_mode = False
    raw_args = sys.argv[1:]
    args: list[str] = []
    for a in raw_args:
        if a in ("--dry-run", "--check", "-n"):
            dry_run = True
        elif a == "--prompt":
            prompt_mode = True
        else:
            args.append(a)

    # Collect target files
    targets: list[Path] = []

    if not args:
        args = ["."]

    for arg in args:
        p = Path(arg)
        if p.is_file():
            targets.append(p)
        elif p.is_dir():
            targets.extend(sorted(p.glob("*.md")))
        else:
            print(f"WARNING: {arg} not found, skipping", file=sys.stderr)

    if not targets:
        print("No .md files found.")
        return

    total_changed = 0
    total_blocks = 0
    total_warnings = 0
    file_warnings: list[tuple[Path, list[str]]] = []

    for fp in targets:
        changes, warnings, has_boxes = process_file(fp, dry_run=dry_run)
        if changes or warnings:
            total_changed += 1
            total_blocks += len(changes)
            total_warnings += len(warnings)
            print(f"Fixed: {fp}")
            for c in changes:
                print(c)
            for w in warnings:
                print(w)
            if warnings:
                file_warnings.append((fp, warnings))
        elif has_boxes:
            print(f"OK: {fp} (already aligned)")
        else:
            print(f"Skipped: {fp} (no bordered blocks)")

    print()
    prefix = "(dry-run) " if dry_run else ""
    summary = f"{prefix}Summary: {total_changed} files changed, {total_blocks} blocks fixed"
    if total_warnings:
        summary += f", {total_warnings} warnings"
    print(summary)

    if prompt_mode and file_warnings:
        print()
        for fp, warnings in file_warnings:
            _print_llm_prompt(fp, warnings)


if __name__ == "__main__":
    main()
