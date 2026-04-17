#!/usr/bin/env python3
"""smart_fix.py — One-shot ASCII art box alignment fixer.

Reads a file, runs symbol_fix, identifies all boxes per code block,
expands hrules to fit widest content, pads narrow lines, writes result.

Usage:
    python smart_fix.py <file.md> [--dry-run]
"""
import sys, os, re

sys.path.insert(0, "E:/github/claude-dotfiles/skills/ascii-align/scripts")
from ascii_align import char_cols, display_width

# ── helpers ──────────────────────────────────────────────────────

def get_borders(line):
    col = 0; out = []
    for i, ch in enumerate(line):
        if ch in "│┐┘┤┴┬┼├┌└":
            out.append((ch, col, i))
        col += char_cols(ch)
    return out

def find_char_idx(line, target_ch, target_col):
    col = 0
    for i, ch in enumerate(line):
        if ch == target_ch and col == target_col:
            return i
        col += char_cols(ch)
    return -1

def line_display_width(line):
    return sum(char_cols(c) for c in line)

# ── box identification ──────���────────────────────────────────────

def identify_boxes(lines, bs, be):
    """Find (top, bot, lcol, rcol) for each ┌→└ paired box."""
    border_map = {i: get_borders(lines[i].rstrip("\n")) for i in range(bs, be)}
    
    opens = []
    for idx in range(bs, be):
        tops = [(ch, col) for ch, col, _ in border_map[idx] if ch == "┌"]
        rights = [(ch, col) for ch, col, _ in border_map[idx] if ch == "┐"]
        for lc in [c for _, c in tops]:
            candidates = [c for _, c in rights if c > lc]
            if candidates:
                opens.append((idx, lc, min(candidates)))
    
    boxes = []
    for top_i, lc, rc in opens:
        for bot_i in range(top_i + 1, be):
            if any(ch == "└" and col == lc for ch, col, _ in border_map.get(bot_i, [])):
                boxes.append((top_i, bot_i, lc, rc))
                break
    
    boxes.sort(key=lambda b: (b[2], b[0]))  # sort by left col, then top row
    return boxes

# ── per-box fix ────────��─────────────────────────────────────────

def fix_box(lines, top, bot, lcol, rcol):
    """Expand hrule and pad lines so all right borders align."""
    changes = 0
    
    # Find max right-border col across content lines
    max_right = rcol
    for idx in range(top + 1, bot):
        raw = lines[idx].rstrip("\n")
        for ch, col, _ in get_borders(raw):
            if ch in "│┐┘┤" and col > lcol and abs(col - rcol) <= 12:
                max_right = max(max_right, col)
    
    if max_right == rcol:
        return 0
    
    expand = max_right - rcol
    
    # Expand top hrule ┌─┐
    raw = lines[top].rstrip("\n")
    ci = find_char_idx(raw, "┐", rcol)
    if ci >= 0:
        raw = raw[:ci] + "─" * expand + raw[ci:]
        lines[top] = raw + "\n"
        changes += 1
    
    # Expand bottom hrule └─┘ (or └─┬─┘)
    raw = lines[bot].rstrip("\n")
    for target in ["┘", "┴"]:
        ci = find_char_idx(raw, target, rcol)
        if ci >= 0:
            raw = raw[:ci] + "─" * expand + raw[ci:]
            lines[bot] = raw + "\n"
            changes += 1
            break
    
    # Pad content lines
    for idx in range(top + 1, bot):
        raw = lines[idx].rstrip("\n")
        borders = get_borders(raw)
        # Find right │ belonging to this box
        candidates = [(ch, col, ci) for ch, col, ci in borders
                      if ch == "│" and col > lcol and abs(col - rcol) <= 1]
        if not candidates:
            continue
        best = candidates[-1]
        if best[1] < max_right:
            diff = max_right - best[1]
            ci = best[2]
            raw = raw[:ci] + " " * diff + raw[ci:]
            lines[idx] = raw + "\n"
            changes += 1
    
    return changes

# ── main ─────────────��───────────────────────────────────────────

def fix_file(path, dry_run=False):
    # Step 1: symbol_fix
    from pathlib import Path
    from symbol_fix import process_file as sf_process
    stats = sf_process(Path(path), dry_run=False, check=False)
    sym_count = stats.get("replacements", 0)
    
    # Step 2: read and fix boxes
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    
    in_block = False
    block_ranges = []
    block_start = -1
    for idx in range(len(lines)):
        if lines[idx].rstrip("\n").strip().startswith("```"):
            if not in_block:
                in_block = True
                block_start = idx + 1
            else:
                in_block = False
                block_ranges.append((block_start, idx))
    
    total = 0
    for bs, be in block_ranges:
        for iteration in range(10):
            boxes = identify_boxes(lines, bs, be)
            round_changes = 0
            # Fix inner boxes first (smaller width range)
            boxes.sort(key=lambda b: b[3] - b[2])
            for top, bot, lc, rc in boxes:
                round_changes += fix_box(lines, top, bot, lc, rc)
            total += round_changes
            if round_changes == 0:
                break
    
    if total > 0 and not dry_run:
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(lines)
    
    # Step 3: verify
    check_stats = sf_process(Path(path), dry_run=True, check=True)
    ok = check_stats.get("width_issues", 0) == 0
    
    print(f"{'[DRY] ' if dry_run else ''}{os.path.basename(path)}: {sym_count} symbols, {total} width fixes {'✓' if ok else '⚠ VERIFY NEEDED'}")
    return ok

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    
    for p in args.files:
        fix_file(p, args.dry_run)
