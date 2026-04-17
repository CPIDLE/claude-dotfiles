#!/usr/bin/env python3
"""
Inject a fixed ASCII art block back into the original Markdown file.

Usage: python inject_ascii_block.py <original.md> <block.md> <start> <end>

  original.md  — the file to update in-place
  block.md     — the fixed block file (p_ or x_ file from the pipeline)
  start        — 1-based line number of the opening ``` fence in original.md
  end          — 1-based line number of the closing ``` fence in original.md

The block.md may start with a <!-- aa: TYPE --> annotation line; that line is
skipped — only the ``` fence and its content are injected. The annotation line
in the original file is left untouched.

Writes original.md in-place. Exit 0 on success, 1 on error.
"""
import re
import sys
from pathlib import Path

ANNOTATION_RE = re.compile(r'<!--\s*aa:\s*\w+\s*-->')


def read_block_lines(block_path: Path) -> list[str]:
    """Return lines of block.md, excluding any leading annotation line."""
    lines = block_path.read_text(encoding='utf-8').splitlines(keepends=True)
    if lines and ANNOTATION_RE.fullmatch(lines[0].strip()):
        lines = lines[1:]
    return lines


def main() -> None:
    if len(sys.argv) != 5:
        print(
            'Usage: inject_ascii_block.py <original.md> <block.md> <start> <end>',
            file=sys.stderr,
        )
        sys.exit(1)

    original_path = Path(sys.argv[1])
    block_path = Path(sys.argv[2])
    start = int(sys.argv[3])  # 1-based, inclusive
    end = int(sys.argv[4])    # 1-based, inclusive

    if not original_path.exists():
        print(f'File not found: {original_path}', file=sys.stderr)
        sys.exit(1)
    if not block_path.exists():
        print(f'File not found: {block_path}', file=sys.stderr)
        sys.exit(1)

    original_lines = original_path.read_text(encoding='utf-8').splitlines(keepends=True)
    block_lines = read_block_lines(block_path)

    # Ensure last line of original has a newline so splice is clean
    before = original_lines[:start - 1]          # lines before the block
    after = original_lines[end:]                  # lines after the block

    new_content = ''.join(before + block_lines + after)
    original_path.write_text(new_content, encoding='utf-8')
    print(f'Injected {len(block_lines)} lines into {original_path} (L{start}-L{end})')


if __name__ == '__main__':
    main()
