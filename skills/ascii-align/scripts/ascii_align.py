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
ARROW_CHARS = set("→←↑↓▼▲↔↕")

# <!-- aa: TYPE --> annotation
_AA_RE = re.compile(r"<!--\s*aa:\s*(\w+)\s*-->")

# Valid annotation types
_AA_TYPES = {"single", "parallel", "nested", "flow", "layout", "table"}


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

    A horizontal-rule line is one where the content (before the border) is
    entirely made of box-drawing characters (┌└├─┬┴┼ etc.), with no spaces
    or text content.  Lines like ``│    ┌──────┐`` are NOT hrules — the │
    and spaces indicate it's a content line with an embedded box header.
    """
    if border not in RIGHT_BORDER:
        return False
    clean = content.strip()
    if not clean:
        return False
    # Must start with a box-drawing left-side or ─ character
    left_starts = HORIZONTAL_LEFT | {"┌", "└", HORIZONTAL_RULE}
    if clean[0] not in left_starts:
        return False
    # All chars in the stripped content must be box-drawing — no spaces or text.
    # Also reject if the content between leading indent and trailing border has
    # internal spaces (e.g. "┌───┤         " is NOT an hrule).
    hrule_chars = set("─├┬┴┼┌┐└┘│┤v")
    if not all(c in hrule_chars for c in clean):
        return False
    # Reject if the original content (after lstrip) has trailing spaces
    # before the border — that means the box-drawing part doesn't fill
    # to the border, so it's a content line with embedded structure.
    after_indent = content.lstrip()
    if after_indent != after_indent.rstrip():
        return False
    return True


def _align_group(
    block_lines: list[str],
    group: list[int],
    *,
    ref_width: int | None = None,
) -> list[str]:
    """Align hrule lines (┌─┐/└─┘) in a box group to uniform display width.

    Only adjusts ─ fill in horizontal rule lines. Content lines are left
    untouched — content padding is the LLM subagent's responsibility.

    If ref_width is given, use it as the target width instead of computing
    majority from the group. This is used when the group is a fragment
    (split by non-bordered lines) and the true box width is known from
    ┌┐/└┘ lines in other fragments.

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

    # Pick target width. Priority:
    # 1. ref_width (from global anchor, for fragment groups)
    # 2. Local hrule anchor width (┌┐/└┘ lines — no trailing-space ambiguity)
    # 3. min_w if spread > 5 (massive padding → trust min)
    # 4. majority_w (default)
    if ref_width is not None:
        target_w = ref_width
    else:
        # Check for local hrule anchors (┌┐/└┘)
        anchor_ws = [
            line_widths[idx]
            for idx, (_, border, hrule) in enumerate(parsed)
            if hrule and border in HORIZONTAL_CORNERS
        ]
        if anchor_ws:
            target_w = Counter(anchor_ws).most_common(1)[0][0]
        elif spread > 5:
            target_w = min_w
        else:
            target_w = majority_w

    # Rebuild each line — only adjust right-side gap
    for idx, i in enumerate(group):
        content, border, hrule = parsed[idx]
        border_w = char_cols(border)

        cur_w = display_width(block_lines[group[idx]].rstrip())

        if cur_w == target_w:
            continue  # already correct width, don't touch

        # Skip lines where the border belongs to an embedded box, not the
        # outer border.  E.g. "│    ┌────────┐" — the ┐ is the right-side
        # box's corner, not the outer box's border.
        # Also skips └...┘ / ┌...┐ corner pairs — these are ambiguous when
        # anchor and content widths disagree (off-by-1). Safer to report
        # via diagnostics and let LLM fix.
        if border == "┐" and "┌" in content:
            continue
        if border == "┘" and "└" in content:
            continue
        if border == "│" and ("┌" in content or "└" in content):
            continue

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
            # Content lines: skip — padding is LLM subagent's responsibility
            continue

        if new_line != block_lines[i].rstrip():
            block_lines[i] = new_line

    return block_lines


# ---------------------------------------------------------------------------
# Inner box detection
# ---------------------------------------------------------------------------

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
                            # Inner box must have enclosing right │ after ┐
                            has_enclosing_right = any(
                                line[ck] == "│"
                                for ck in range(cj + 1, len(line))
                            )
                            if has_enclosing_right:
                                results.append((left_col, right_col, i))
                        break
                    right_col += char_cols(line[cj])
                # No ┐ found → malformed header, skip
            col += char_cols(c)
    return results


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


def _read_annotation(lines: list[str], fence_line: int) -> str | None:
    """Read <!-- aa: TYPE --> annotation above a code fence line."""
    for i in range(fence_line - 1, max(fence_line - 4, -1), -1):
        m = _AA_RE.search(lines[i])
        if m:
            t = m.group(1).lower()
            return t if t in _AA_TYPES else None
    return None


def _detect_type(block_lines: list[str]) -> str:
    """Auto-detect ASCII art type from block content."""
    has_parallel = False
    has_arrows_outside = False
    has_junction = False

    for line in block_lines:
        # parallel: same line has ≥2 independent │...│ segments with gap
        segments = re.findall(r"│[^│]*│", line)
        if len(segments) >= 2:
            # Verify there's a gap (≥2 spaces) between segments
            for j in range(len(segments) - 1):
                end_pos = line.find(segments[j]) + len(segments[j])
                next_pos = line.find(segments[j + 1], end_pos)
                if next_pos > end_pos and line[end_pos:next_pos].strip() == "":
                    has_parallel = True
                    break

        # arrows on a line without box borders → flow connector
        stripped = line.strip()
        if any(c in ARROW_CHARS for c in stripped):
            if "│" not in stripped and "┌" not in stripped and "└" not in stripped:
                has_arrows_outside = True

        # table: needs ┼ (cross junction) — ┬/┴ alone could be branch connectors
        if "┼" in line:
            has_junction = True

    if has_junction:
        return "table"
    if has_parallel:
        return "parallel"
    if has_arrows_outside:
        return "flow"
    return "single"


def _check_off_by_1(
    block_lines: list[str], groups: list[list[int]], line_offset: int
) -> list[str]:
    """Detect off-by-1: majority width = bottom hrule width + 1.

    Must be called on ORIGINAL lines before alignment, since alignment
    equalizes all widths. Only fires when spread <= 5 (rule engine picks
    majority), because spread > 5 already shrinks to min.

    Skips groups that have hrule anchor lines (┌┐/└┘) — those are already
    corrected by _align_group's anchor priority logic.
    """
    warnings: list[str] = []
    for group in groups:
        # Skip groups with hrule anchors — _align_group already uses anchor width
        has_anchor = any(
            block_lines[i].rstrip()[-1] in HORIZONTAL_CORNERS
            and _is_hrule_line(block_lines[i].rstrip()[:-1], block_lines[i].rstrip()[-1])
            for i in group
            if block_lines[i].rstrip()
        )
        if has_anchor:
            continue

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


def _diagnose_file(filepath: Path) -> str | None:
    """Analyze a file and produce a rich diagnostic prompt for the LLM subagent.

    Returns the prompt string, or None if no issues found.
    Called AFTER hrule fixes have been written, so it sees the post-fix state.
    """
    text = filepath.read_text(encoding="utf-8")
    lines = text.split("\n")
    abs_path = filepath.resolve()

    # Collect code blocks
    in_block = False
    block_start = -1
    blocks: list[tuple[int, int]] = []
    for i, line in enumerate(lines):
        if _FENCE_RE.match(line):
            if not in_block:
                in_block = True
                block_start = i
            else:
                blocks.append((block_start, i))
                in_block = False

    block_reports: list[str] = []
    block_num = 0

    for bstart, bend in blocks:
        inner_start = bstart + 1
        inner_end = bend
        if inner_start >= inner_end:
            continue

        block_lines = lines[inner_start:inner_end]
        if not any(_is_bordered(l) for l in block_lines):
            continue

        groups = _find_box_groups(block_lines)
        if not groups:
            continue

        aa_type = _read_annotation(lines, bstart) or _detect_type(block_lines)
        if aa_type == "table":
            continue

        # Collect all issues for this block
        issues: list[str] = []

        # --- Group width analysis ---
        for gi, group in enumerate(groups):
            widths = [(i, display_width(block_lines[i].rstrip())) for i in group]
            width_counts = Counter(w for _, w in widths)
            target_w = width_counts.most_common(1)[0][0]

            # Check for hrule anchor override
            anchor_ws = []
            for i in group:
                stripped = block_lines[i].rstrip()
                if stripped and stripped[-1] in HORIZONTAL_CORNERS:
                    if _is_hrule_line(stripped[:-1], stripped[-1]):
                        anchor_ws.append(display_width(stripped))
            if anchor_ws:
                target_w = Counter(anchor_ws).most_common(1)[0][0]

            ok_lines = []
            fix_lines = []
            for i, w in widths:
                line_num = inner_start + i + 1
                if w == target_w:
                    ok_lines.append(f"L{line_num}")
                else:
                    diff = w - target_w
                    sign = f"+{diff}" if diff > 0 else str(diff)
                    content_preview = block_lines[i].rstrip()
                    if len(content_preview) > 72:
                        content_preview = content_preview[:69] + "..."
                    fix_lines.append(
                        f"  - L{line_num}: w={w} ({sign}). "
                        f'"{content_preview}"'
                    )

            if not fix_lines:
                continue

            g_first = inner_start + group[0] + 1
            g_last = inner_start + group[-1] + 1
            issues.append(
                f"### Group {gi + 1}: L{g_first}-L{g_last} "
                f"(target_width: {target_w})"
            )
            issues.append(f"OK lines: {', '.join(ok_lines)}")
            issues.append("Fix lines:")
            issues.extend(fix_lines)

        # --- Inner box analysis ---
        inner_boxes = _find_inner_boxes(block_lines)
        for left_col, right_col, header_idx in inner_boxes:
            misaligned: list[str] = []
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
                        if scan_col != right_col:
                            diff = scan_col - right_col
                            sign = f"+{diff}" if diff > 0 else str(diff)
                            line_num = inner_start + li + 1
                            misaligned.append(
                                f"  L{line_num}: {target_char}@col {scan_col} ({sign})"
                            )
                        break
                    scan_col += char_cols(line[cj])
                if lchar == "└":
                    break

            if misaligned:
                h_line_num = inner_start + header_idx + 1
                issues.append(
                    f"### Inner box at L{h_line_num} "
                    f"(┌@col {left_col}, ┐@col {right_col})"
                )
                issues.append(f"Expected right border at col {right_col}:")
                issues.extend(misaligned)

        # --- Off-by-1 analysis ---
        off1 = _check_off_by_1(block_lines, groups, inner_start)
        if off1:
            issues.append("### Off-by-1")
            issues.extend(off1)

        if not issues:
            continue

        block_num += 1
        b_first = inner_start + 1
        b_last = inner_end
        header = f"## Block {block_num}: L{b_first}-L{b_last} (type: {aa_type})"
        block_reports.append(header + "\n" + "\n".join(issues))

    if not block_reports:
        return None

    prompt_parts = [
        f"=== LLM FIX PROMPT for {filepath} ===",
        "",
        "## Width Rules",
        "Font: Sarasa Mono TC.",
        "- box-drawing (─│├┐┘┤┌┬┴┼) = 1 col",
        "- CJK / fullwidth (中（）【】) = 2 cols",
        "- arrows (→←↑↓↔▼▲) = 2 cols",
        "- geometric (●○■□◆) = 2 cols",
        "- EM dash/ellipsis (—…) = 2 cols",
        "- ASCII (A-Z 0-9 +-=) = 1 col",
        "",
        "## Principles",
        "- Every line in a box group MUST have identical display width",
        "- Only adjust spacing (spaces). Never change text content.",
        "- Vertical alignment: ▼/→ must start at same column as │ above",
        "- 寧可不改也不改壞 — if unsure, leave unchanged",
        "",
    ]
    prompt_parts.extend(
        ("\n\n".join(block_reports)).split("\n")
    )
    prompt_parts.extend([
        "",
        f"File to fix: {abs_path}",
        "Read the file, fix the issues above, then save.",
        f"Verify: python ascii_align.py --check \"{abs_path}\"",
        "===",
    ])
    return "\n".join(prompt_parts)


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

        # Determine alignment strategy from annotation or auto-detection
        aa_type = _read_annotation(lines, bstart) or _detect_type(block_lines)
        # table → skip entirely
        if aa_type == "table":
            continue
        # Snapshot for comparison
        original = [l for l in block_lines]

        # Pre-alignment: detect off-by-1 on original widths (report only)
        off_by_1 = _check_off_by_1(block_lines, groups, inner_start)

        # Align outer box borders (hrule fill only — content is LLM's job)

        # Compute global anchor width from ┌┐/└┘ hrule lines across ALL groups.
        # Fragment groups without their own ┌┐/└┘ will use this as ref_width.
        anchor_ws: list[int] = []
        for g in groups:
            for i in g:
                stripped = block_lines[i].rstrip()
                if stripped and stripped[-1] in HORIZONTAL_CORNERS:
                    content = stripped[:-1]
                    if _is_hrule_line(content, stripped[-1]):
                        anchor_ws.append(display_width(stripped))
        anchor_w: int | None = None
        if anchor_ws:
            anchor_counts = Counter(anchor_ws)
            anchor_w = anchor_counts.most_common(1)[0][0]

        for group in groups:
            # Check if this group has its own ┌┐/└┘ anchor
            has_own_anchor = any(
                block_lines[i].rstrip()[-1] in HORIZONTAL_CORNERS
                and _is_hrule_line(block_lines[i].rstrip()[:-1], block_lines[i].rstrip()[-1])
                for i in group
                if block_lines[i].rstrip()
            )
            rw = None if has_own_anchor else anchor_w
            _align_group(block_lines, group, ref_width=rw)

        # Verify alignment (always, regardless of whether changes were made)
        warnings = _verify_inner_boxes(block_lines, inner_start)
        warnings += _verify_group_widths(block_lines, groups, inner_start)
        all_warnings.extend(warnings)
        all_warnings.extend(off_by_1)

        # Check if anything changed
        if block_lines != original:
            lines[inner_start:inner_end] = block_lines
            for group in groups:
                first_line = inner_start + group[0] + 1
                last_line = inner_start + group[-1] + 1
                count = len(group)
                w = display_width(block_lines[group[0]].rstrip())
                changes.append(f"  L{first_line}-L{last_line}: {count} lines aligned to w={w}")
            modified = True

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

    # --prompt implies writing (not dry-run) so diagnostics see post-fix state
    if prompt_mode:
        dry_run = False

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
        if changes:
            total_changed += 1
            total_blocks += len(changes)
            print(f"Fixed: {fp}")
            for c in changes:
                print(c)
        if warnings:
            total_warnings += len(warnings)
            if not changes:
                print(f"Lint: {fp}")
            for w in warnings:
                print(w)
            file_warnings.append((fp, warnings))
        if not changes and not warnings:
            if has_boxes:
                print(f"OK: {fp} (already aligned)")
            else:
                print(f"Skipped: {fp} (no bordered blocks)")

    print()
    prefix = "(dry-run) " if dry_run else ""
    summary = f"{prefix}Summary: {total_changed} files changed, {total_blocks} blocks fixed"
    if total_warnings:
        summary += f", {total_warnings} warnings"
    print(summary)

    if prompt_mode:
        # Diagnostic pass: analyze all files for remaining issues (after hrule fixes)
        for fp in targets:
            prompt = _diagnose_file(fp)
            if prompt:
                print()
                print(prompt)


if __name__ == "__main__":
    main()
