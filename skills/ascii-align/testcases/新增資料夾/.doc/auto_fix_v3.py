#!/usr/bin/env python3
"""auto_fix_v3.py — Sliding-window box alignment fixer.

Two-pass approach:
  Pass 1 (3-line window): Fix │ positions using hrule ┐/┘ from adjacent lines
  Pass 2 (5-line window): Fix connector chains (┬→│→v) using wider context

Uses nearest-match pairing instead of majority vote to handle nested boxes.
"""

import sys
import glob

sys.path.insert(0, "E:/github/claude-dotfiles/skills/ascii-align/scripts")
from ascii_align import char_cols


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_borders(line: str) -> list[tuple[str, int]]:
    """Return [(char, display_col), ...] for box-drawing chars."""
    col = 0
    borders = []
    for ch in line:
        if ch in "│┐┘┤┴┬┼├┌└":
            borders.append((ch, col))
        col += char_cols(ch)
    return borders


def find_char_pos(line: str, target_ch: str, target_col: int) -> int:
    """Find the character index in `line` where `target_ch` sits at display `target_col`."""
    col = 0
    for i, ch in enumerate(line):
        if ch == target_ch and col == target_col:
            return i
        col += char_cols(ch)
    return -1


def count_trailing_spaces(line: str, before_pos: int) -> int:
    """Count spaces immediately before character position `before_pos`."""
    n = 0
    for j in range(before_pos - 1, -1, -1):
        if line[j] == " ":
            n += 1
        else:
            break
    return n


def count_trailing_dashes(line: str, before_pos: int) -> int:
    """Count ─ immediately before character position `before_pos`."""
    n = 0
    for j in range(before_pos - 1, -1, -1):
        if line[j] == "─":
            n += 1
        else:
            break
    return n


# ---------------------------------------------------------------------------
# Pass 1: 3-line window — fix │ to match adjacent ┐/┘
# ---------------------------------------------------------------------------

def pass1_window_fix(lines: list[str], bs: int, be: int) -> int:
    """Fix content │ positions using hrule ┐/┘ from prev/next lines."""
    changes = 0

    for idx in range(bs, be):
        raw = lines[idx].rstrip("\n")
        curr_borders = get_borders(raw)
        curr_pipes = [(ch, col) for ch, col in curr_borders if ch == "│" and col > 2]
        if not curr_pipes:
            continue

        # Collect target columns from nearby lines (┐/┘ positions)
        # Use ±5 window to handle boxes with many content lines
        targets = set()
        for look in range(max(bs, idx - 5), min(be, idx + 6)):
            if look == idx:
                continue
            adj_raw = lines[look].rstrip("\n")
            for ch, col in get_borders(adj_raw):
                if ch in "┐┘":
                    targets.add(col)

        if not targets:
            continue

        # For each │, find nearest target (within ±3)
        for pipe_ch, pipe_col in curr_pipes:
            best = min(targets, key=lambda t: abs(t - pipe_col), default=None)
            if best is None or best == pipe_col or abs(best - pipe_col) > 3:
                continue

            diff = pipe_col - best  # positive = shrink, negative = grow
            char_pos = find_char_pos(raw, "│", pipe_col)
            if char_pos < 0:
                continue

            if diff > 0:
                # Remove trailing spaces before │
                sp = count_trailing_spaces(raw, char_pos)
                remove = min(diff, sp)
                if remove > 0:
                    raw = raw[: char_pos - remove] + raw[char_pos:]
                    lines[idx] = raw + "\n"
                    changes += 1
            elif diff < 0:
                # Add trailing spaces before │
                raw = raw[:char_pos] + " " * (-diff) + raw[char_pos:]
                lines[idx] = raw + "\n"
                changes += 1

    return changes


# ---------------------------------------------------------------------------
# Pass 2: 5-line window — fix ┐/┘ to match content │ (expand hrule)
# ---------------------------------------------------------------------------

def pass2_hrule_expand(lines: list[str], bs: int, be: int) -> int:
    """Expand ┐/┘ when content │ is wider and can't be shrunk."""
    changes = 0

    for idx in range(bs, be):
        raw = lines[idx].rstrip("\n")
        curr_borders = get_borders(raw)
        corners = [(ch, col) for ch, col in curr_borders if ch in "┐┘"]
        if not corners:
            continue

        # Check if any nearby │ is further right than this corner
        for corner_ch, corner_col in corners:
            max_pipe = corner_col
            for look in range(max(bs, idx - 4), min(be, idx + 5)):
                if look == idx:
                    continue
                adj_raw = lines[look].rstrip("\n")
                for bch, bcol in get_borders(adj_raw):
                    if bch == "│" and bcol > corner_col and bcol <= corner_col + 3:
                        max_pipe = max(max_pipe, bcol)

            if max_pipe > corner_col:
                expand = max_pipe - corner_col
                char_pos = find_char_pos(raw, corner_ch, corner_col)
                if char_pos >= 0:
                    raw = raw[:char_pos] + "─" * expand + raw[char_pos:]
                    lines[idx] = raw + "\n"
                    changes += 1

    return changes


# ---------------------------------------------------------------------------
# Pass 3: connector chain (┬→│→v) — 5-line window
# ---------------------------------------------------------------------------

def pass3_connector_chain(lines: list[str], bs: int, be: int) -> int:
    """Fix v positions to match ┬/┼ above."""
    changes = 0

    for idx in range(bs, be):
        raw = lines[idx].rstrip("\n")

        # Find v arrows
        col = 0
        v_positions = []
        for ci, ch in enumerate(raw):
            if ch == "v" and (ci == 0 or raw[ci - 1] == " "):
                v_positions.append((col, ci))
            col += char_cols(ch)

        if not v_positions:
            continue

        # Find ┬/┼/│ targets from lines above (up to 4 lines)
        above_targets = set()
        for look in range(idx - 1, max(bs - 1, idx - 5), -1):
            adj_raw = lines[look].rstrip("\n")
            for bch, bcol in get_borders(adj_raw):
                if bch in "┬┼│":
                    above_targets.add(bcol)
            if above_targets:
                break  # use nearest line with borders

        if not above_targets:
            continue

        for v_col, v_ci in v_positions:
            best = min(above_targets, key=lambda t: abs(t - v_col), default=None)
            if best is None or best == v_col or abs(best - v_col) > 3:
                continue

            diff = v_col - best
            if diff > 0:
                # Remove spaces before v
                sp = count_trailing_spaces(raw, v_ci)
                remove = min(diff, sp)
                if remove > 0:
                    raw = raw[: v_ci - remove] + raw[v_ci:]
                    lines[idx] = raw + "\n"
                    changes += 1
                    # Recalculate positions after edit
                    break  # re-process this line on next iteration

    return changes


# ---------------------------------------------------------------------------
# Main: iterative convergence
# ---------------------------------------------------------------------------

def fix_file(path: str) -> int:
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    # Find code blocks
    in_block = False
    block_ranges = []
    block_start = -1
    for idx in range(len(lines)):
        raw = lines[idx].rstrip("\n")
        if raw.strip().startswith("```"):
            if not in_block:
                in_block = True
                block_start = idx + 1
            else:
                in_block = False
                block_ranges.append((block_start, idx))

    total_changes = 0
    for bs, be in block_ranges:
        for _iteration in range(10):
            c1 = pass1_window_fix(lines, bs, be)
            c2 = pass2_hrule_expand(lines, bs, be)
            c3 = pass3_connector_chain(lines, bs, be)
            round_changes = c1 + c2 + c3
            total_changes += round_changes
            if round_changes == 0:
                break

    if total_changes > 0:
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(lines)

    return total_changes


# ---------------------------------------------------------------------------
# Box-aware fix (v3.1): identify boxes, then fix within each box
# ---------------------------------------------------------------------------

def identify_boxes(lines: list[str], bs: int, be: int) -> list[tuple[int, int, int, int]]:
    """Identify boxes by matching ┌ to └ at the same left col.

    Returns [(top_idx, bot_idx, left_col, right_col), ...] sorted by nesting
    (outermost first).
    """
    border_map = {}
    for idx in range(bs, be):
        raw = lines[idx].rstrip("\n")
        col = 0
        borders = []
        for ch in raw:
            if ch in "│┐┘┤┴┬┼├┌└":
                borders.append((ch, col))
            col += char_cols(ch)
        border_map[idx] = borders

    # Find all ┌ positions
    opens = []  # (idx, left_col, right_col)
    for idx in range(bs, be):
        for ch, col in border_map[idx]:
            if ch == "┌":
                # Find matching ┐ on same line
                right = None
                for ch2, col2 in border_map[idx]:
                    if ch2 == "┐" and col2 > col:
                        right = col2
                        break
                if right is not None:
                    opens.append((idx, col, right))

    # Match each ┌ to └ at same left col
    boxes = []
    for top_idx, left_col, right_col in opens:
        for bot_idx in range(top_idx + 1, be):
            for ch, col in border_map[bot_idx]:
                if ch == "└" and col == left_col:
                    # Found matching └. Get its right col (┘)
                    bot_right = None
                    for ch2, col2 in border_map[bot_idx]:
                        if ch2 == "┘" and col2 >= left_col:
                            bot_right = col2
                            break
                    boxes.append((top_idx, bot_idx, left_col, right_col))
                    break
            else:
                continue
            break

    # Sort: outermost (widest) first
    boxes.sort(key=lambda b: -(b[3] - b[2]))
    return boxes


def fix_box_content(lines: list[str], top_idx: int, bot_idx: int,
                    left_col: int, right_col: int) -> int:
    """Fix │ positions within a single identified box."""
    changes = 0

    for idx in range(top_idx + 1, bot_idx):
        raw = lines[idx].rstrip("\n")
        borders = get_borders(raw)

        # Find the │ that belongs to THIS box's right border
        # It should be the one nearest to right_col
        candidates = [(ch, col) for ch, col in borders
                      if ch == "│" and abs(col - right_col) <= 3 and col > left_col]

        if not candidates:
            continue

        # Pick the one nearest to right_col
        best_ch, best_col = min(candidates, key=lambda x: abs(x[1] - right_col))

        if best_col == right_col:
            continue

        diff = best_col - right_col
        char_pos = find_char_pos(raw, "│", best_col)
        if char_pos < 0:
            continue

        if diff > 0:
            # Remove trailing spaces before │
            sp = count_trailing_spaces(raw, char_pos)
            remove = min(diff, sp)
            if remove > 0:
                raw = raw[: char_pos - remove] + raw[char_pos:]
                lines[idx] = raw + "\n"
                changes += 1
        elif diff < 0:
            # Add trailing spaces before │
            raw = raw[:char_pos] + " " * (-diff) + raw[char_pos:]
            lines[idx] = raw + "\n"
            changes += 1

    # Also fix bottom hrule ┘ if it doesn't match
    bot_raw = lines[bot_idx].rstrip("\n")
    bot_borders = get_borders(bot_raw)
    bot_rights = [(ch, col) for ch, col in bot_borders
                  if ch == "┘" and abs(col - right_col) <= 3]
    if bot_rights:
        bot_ch, bot_col = min(bot_rights, key=lambda x: abs(x[1] - right_col))
        if bot_col != right_col:
            diff = bot_col - right_col
            char_pos = find_char_pos(bot_raw, "┘", bot_col)
            if char_pos >= 0:
                if diff > 0:
                    dashes = count_trailing_dashes(bot_raw, char_pos)
                    remove = min(diff, dashes)
                    if remove > 0:
                        bot_raw = bot_raw[: char_pos - remove] + bot_raw[char_pos:]
                        lines[bot_idx] = bot_raw + "\n"
                        changes += 1
                elif diff < 0:
                    bot_raw = bot_raw[:char_pos] + "─" * (-diff) + bot_raw[char_pos:]
                    lines[bot_idx] = bot_raw + "\n"
                    changes += 1

    return changes


def fix_file_v31(path: str) -> int:
    """Box-aware fix: identify boxes, then fix each box's content."""
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    in_block = False
    block_ranges = []
    block_start = -1
    for idx in range(len(lines)):
        raw = lines[idx].rstrip("\n")
        if raw.strip().startswith("```"):
            if not in_block:
                in_block = True
                block_start = idx + 1
            else:
                in_block = False
                block_ranges.append((block_start, idx))

    total_changes = 0
    for bs, be in block_ranges:
        for _iteration in range(10):
            boxes = identify_boxes(lines, bs, be)
            round_changes = 0
            for top, bot, lcol, rcol in boxes:
                round_changes += fix_box_content(lines, top, bot, lcol, rcol)
            # Also run pass3 for v alignment
            round_changes += pass3_connector_chain(lines, bs, be)
            total_changes += round_changes
            if round_changes == 0:
                break

    if total_changes > 0:
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(lines)

    return total_changes


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="*", default=[])
    parser.add_argument("--v31", action="store_true", help="Use box-aware v3.1")
    args = parser.parse_args()

    paths = args.files if args.files else sorted(glob.glob("**/*.md", recursive=True))
    fixer = fix_file_v31 if args.v31 else fix_file
    total = 0
    for p in paths:
        n = fixer(p)
        if n:
            print(f"  {p}: {n} changes")
            total += n
    print(f"Total: {total} changes")
