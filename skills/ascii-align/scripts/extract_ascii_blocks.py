#!/usr/bin/env python3
"""
Extract ASCII art fenced code blocks from a Markdown file.

Usage: python extract_ascii_blocks.py <file.md>

For each fenced code block containing box-drawing chars (┌┐└┘│─):
  - Writes _<stem>_<start>_<end>.md to same directory as input file
  - start/end are 1-based line numbers, inclusive of the ``` fence lines
  - If the line immediately above the opening fence is <!-- aa: TYPE -->,
    it is prepended to the output file so ascii_align.py sees the type hint

Prints JSON to stdout:
  [{"start": S, "end": E, "filename": "/abs/path/_stem_S_E.md"}, ...]

Exit 0 on success (even if zero blocks found). Exit 1 on error.
"""
import json
import re
import sys
from pathlib import Path

BOX_CHARS = frozenset('┌┐└┘│─')
ANNOTATION_RE = re.compile(r'<!--\s*aa:\s*\w+\s*-->')


def _leading_ticks(line: str) -> int:
    s = line.lstrip()
    count = 0
    for c in s:
        if c == '`':
            count += 1
        else:
            break
    return count


def _is_closing_fence(line: str, open_ticks: int) -> bool:
    s = line.strip()
    n = _leading_ticks(line)
    return n >= open_ticks and s == '`' * n


def has_box_drawing(lines: list[str]) -> bool:
    return any(any(c in BOX_CHARS for c in ln) for ln in lines)


def extract_blocks(filepath: Path) -> list[dict]:
    raw = filepath.read_text(encoding='utf-8')
    lines = raw.splitlines(keepends=True)
    results = []
    i = 0
    n = len(lines)

    while i < n:
        ticks = _leading_ticks(lines[i])
        if ticks < 3:
            i += 1
            continue

        # Found an opening fence at line i (0-based)
        fence_open_idx = i
        open_ticks = ticks

        # Scan for closing fence
        j = fence_open_idx + 1
        block_lines = []
        fence_close_idx = None
        while j < n:
            if _is_closing_fence(lines[j], open_ticks):
                fence_close_idx = j
                break
            block_lines.append(lines[j])
            j += 1

        if fence_close_idx is None:
            i += 1
            continue

        if has_box_drawing(block_lines):
            start = fence_open_idx + 1   # 1-based
            end = fence_close_idx + 1    # 1-based

            # Check for annotation on the line immediately above the opening fence
            annotation = None
            if fence_open_idx > 0:
                prev = lines[fence_open_idx - 1].strip()
                if ANNOTATION_RE.fullmatch(prev):
                    annotation = prev

            # Build output content
            out_parts = []
            if annotation:
                out_parts.append(annotation + '\n')
            out_parts.append(lines[fence_open_idx])
            out_parts.extend(block_lines)
            out_parts.append(lines[fence_close_idx])

            stem = filepath.stem
            out_name = f'_{stem}_{start}_{end}.md'
            out_path = filepath.parent / out_name
            out_path.write_text(''.join(out_parts), encoding='utf-8')

            results.append({
                'start': start,
                'end': end,
                'filename': str(out_path.resolve()),
            })

        i = fence_close_idx + 1

    return results


def main() -> None:
    if len(sys.argv) < 2:
        print('Usage: extract_ascii_blocks.py <file.md>', file=sys.stderr)
        sys.exit(1)

    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f'File not found: {filepath}', file=sys.stderr)
        sys.exit(1)

    blocks = extract_blocks(filepath)
    print(json.dumps(blocks, ensure_ascii=False, indent=None))


if __name__ == '__main__':
    main()
