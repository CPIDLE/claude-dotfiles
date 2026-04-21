"""Mask non-structural text runs with █, preserving column width.

Rules:
- Structural chars (Unicode box-drawing U+2500-U+257F + arrows) → keep as-is
- Whitespace → keep (maintains alignment)
- Text chars (letters/digits/CJK/ASCII symbols) → replace with █, 1 per column
- Text runs bridged by ≤2 consecutive spaces merge into one span
  (internal spaces within the span also become █)

Column width uses East Asian Width: F/W=2, others=1.

Ported from AsciiArtViewer_v0/scripts/skeleton_denoiser/mask_text.py
(2026-04-22 skeleton denoiser pipeline).
"""
from __future__ import annotations
import unicodedata


BOX_DRAWING_LO, BOX_DRAWING_HI = 0x2500, 0x257F
ARROW_LO, ARROW_HI = 0x2190, 0x21FF
ARROW_EXTRAS = frozenset('▶◀▲▼')
ASCII_ARROW_CHARS = frozenset('v^<>')


def is_structural(c: str) -> bool:
    if not c:
        return False
    code = ord(c)
    if BOX_DRAWING_LO <= code <= BOX_DRAWING_HI:
        return True
    if ARROW_LO <= code <= ARROW_HI:
        return True
    if c in ARROW_EXTRAS:
        return True
    return False


def _is_structural_or_space(c: str) -> bool:
    return not c or c == ' ' or is_structural(c)


def _is_isolated_arrow(line: str, i: int) -> bool:
    c = line[i]
    if c not in ASCII_ARROW_CHARS:
        return False
    left = line[i - 1] if i > 0 else ''
    right = line[i + 1] if i + 1 < len(line) else ''
    return _is_structural_or_space(left) and _is_structural_or_space(right)


def char_cols(c: str) -> int:
    if not c or ord(c) < 0x20:
        return 0
    eaw = unicodedata.east_asian_width(c)
    return 2 if eaw in ('F', 'W') else 1


def mask_text(line: str, bridge_spaces: int = 2) -> str:
    n = len(line)
    if n == 0:
        return line

    classes = []
    for i, c in enumerate(line):
        if c == ' ':
            classes.append('_')
        elif is_structural(c) or _is_isolated_arrow(line, i):
            classes.append('S')
        else:
            classes.append('T')

    out = []
    i = 0
    while i < n:
        cls = classes[i]
        if cls == 'T':
            j = i + 1
            while j < n:
                if classes[j] == 'T':
                    j += 1
                elif classes[j] == '_':
                    k = j
                    while k < n and classes[k] == '_':
                        k += 1
                    if k < n and classes[k] == 'T' and (k - j) <= bridge_spaces:
                        j = k + 1
                    else:
                        break
                else:
                    break
            span = line[i:j]
            cols = sum(char_cols(ch) for ch in span)
            out.append('█' * cols)
            i = j
        else:
            out.append(line[i])
            i += 1
    return ''.join(out)


def mask_block(block: str, bridge_spaces: int = 2) -> str:
    return '\n'.join(mask_text(ln, bridge_spaces) for ln in block.split('\n'))
