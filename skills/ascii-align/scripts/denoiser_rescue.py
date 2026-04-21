#!/usr/bin/env python3
"""denoiser_rescue.py — Deterministic skeleton rescue for ASCII art blocks.

Pipeline:
    raw_block
        -> apply SYMBOL_MAP (Unicode→ASCII width-preserving)
        -> mask_block      (text runs → █)
        -> fill_text       (original text runs placed back into █ slots)
        -> clean_block     (or None if cannot place all runs)

This is the deterministic production path from
AsciiArtViewer_v0/scripts/skeleton_denoiser/denoiser.py::denoise_block.
NO ML dependency — pure Python stdlib.

Use when the structural linter (ascii_align.py) fails:
- The block has Unicode symbols distorting widths → SYMBOL_MAP fixes them
- The block has clean borders but off-by-1 spacing inside → mask+fill
  redistributes padding to canonical slot widths
- Idempotent on already-clean blocks (safe to run blindly)

Usage:
    python denoiser_rescue.py <raw_block_file>
    python denoiser_rescue.py --stdin
"""
from __future__ import annotations
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from mask_text import mask_block, is_structural, char_cols, _is_isolated_arrow
from symbol_fix import SYMBOL_MAP


def apply_symbol_map(text: str) -> str:
    """Replace Unicode w2 symbols with width-preserving ASCII."""
    for src, dst in SYMBOL_MAP:
        text = text.replace(src, dst)
    return text


def _extract_text_runs(block: str) -> list[tuple[int, int, int, str]]:
    """Return [(row, col_start, col_end, text)] for each non-structural run.

    Uses the same bridging rule as mask_text so run boundaries line up with
    █ segments in the masked version.
    """
    runs: list[tuple[int, int, int, str]] = []
    for r, line in enumerate(block.split('\n')):
        n = len(line)
        col = 0
        i = 0
        while i < n:
            c = line[i]
            if c == ' ' or is_structural(c) or _is_isolated_arrow(line, i):
                col += char_cols(c)
                i += 1
                continue
            span_col_start = col
            j = i
            while j < n:
                ch = line[j]
                if ch == ' ':
                    k = j
                    while k < n and line[k] == ' ':
                        k += 1
                    if k < n and not (is_structural(line[k]) or _is_isolated_arrow(line, k)) \
                            and line[k] != ' ' and (k - j) <= 2:
                        j = k
                        continue
                    break
                elif is_structural(ch) or _is_isolated_arrow(line, j):
                    break
                else:
                    j += 1
            span = line[i:j]
            span_cols = sum(char_cols(ch) for ch in span)
            runs.append((r, span_col_start, span_col_start + span_cols, span))
            col += span_cols
            i = j
    return runs


def _find_skeleton_slots(masked_block: str) -> list[tuple[int, int, int]]:
    """Return [(row, col_start, col_end)] for each maximal █-run."""
    slots: list[tuple[int, int, int]] = []
    for r, line in enumerate(masked_block.split('\n')):
        n = len(line)
        col = 0
        i = 0
        while i < n:
            if line[i] == '█':
                start_col = col
                j = i
                while j < n and line[j] == '█':
                    col += 1
                    j += 1
                slots.append((r, start_col, col))
                i = j
            else:
                col += char_cols(line[i])
                i += 1
    return slots


def _pad_text_to_cols(text: str, target_cols: int) -> str:
    cur = sum(char_cols(c) for c in text)
    if cur >= target_cols:
        return text
    return text + ' ' * (target_cols - cur)


def fill_text(skeleton: str, text_runs: list[tuple[int, int, int, str]]) -> str | None:
    """Place each original text run into the skeleton's █-slots.

    Strategy: match each run in reading order to the next available slot whose
    width >= run width. Pad with spaces to fill any slack.
    Returns None if we can't match every run.
    """
    lines = [list(l) for l in skeleton.split('\n')]
    slots = _find_skeleton_slots(skeleton)
    if len(slots) < len(text_runs):
        return None

    slots_by_read = sorted(slots, key=lambda s: (s[0], s[1]))
    runs_by_read = sorted(text_runs, key=lambda t: (t[0], t[1]))

    used = [False] * len(slots_by_read)
    for run in runs_by_read:
        _, _, _, text = run
        text_cols = sum(char_cols(c) for c in text)
        picked = -1
        for si, slot in enumerate(slots_by_read):
            if used[si]:
                continue
            _, cs, ce = slot
            if ce - cs >= text_cols:
                picked = si
                break
        if picked < 0:
            return None
        used[picked] = True
        r, cs, ce = slots_by_read[picked]
        padded = _pad_text_to_cols(text, ce - cs)
        char_idx = 0
        cur_col = 0
        while char_idx < len(lines[r]) and cur_col < cs:
            cur_col += char_cols(lines[r][char_idx])
            char_idx += 1
        end_idx = char_idx
        occupied_cols = 0
        while end_idx < len(lines[r]) and occupied_cols < (ce - cs):
            occupied_cols += char_cols(lines[r][end_idx])
            end_idx += 1
        lines[r][char_idx:end_idx] = list(padded)
    return '\n'.join(''.join(l) for l in lines)


def rescue_block(raw: str) -> str | None:
    """Full deterministic rescue: raw → clean (or None if fill_text fails)."""
    normalized = apply_symbol_map(raw)
    masked = mask_block(normalized)
    text_runs = _extract_text_runs(normalized)
    return fill_text(masked, text_runs)


def main():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('file', nargs='?', help='Path to raw block text file')
    g.add_argument('--stdin', action='store_true', help='Read block from stdin')
    args = ap.parse_args()

    raw = sys.stdin.read() if args.stdin else Path(args.file).read_text(encoding='utf-8')
    out = rescue_block(raw.rstrip('\n'))
    if out is None:
        print('RESCUE FAILED (fill_text could not place all runs)', file=sys.stderr)
        sys.exit(1)
    print(out)


if __name__ == '__main__':
    main()
