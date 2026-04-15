#!/usr/bin/env python3
"""collect_samples.py — Collect ASCII box-drawing code blocks from .md files.

Scans a directory tree for Markdown files, extracts fenced code blocks that
contain box-drawing characters, and writes them to a single sample file
for ascii-align testing.

Usage:
    python collect_samples.py [scan_dir] [-o output_path]

    scan_dir     Directory to scan (default: E:/github)
    -o path      Output file (default: ../testcases/Ascii_sample.md)
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

BOX_CHARS = set("┌┐└┘│─├┤┬┴┼")
FENCE_RE = re.compile(r"^ {0,3}```")
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", ".tox"}


def _has_box_chars(lines: list[str]) -> bool:
    return any(c in BOX_CHARS for line in lines for c in line)


def extract_blocks(filepath: Path) -> list[tuple[int, list[str], str]]:
    """Extract fenced code blocks containing box-drawing chars.

    Returns list of (start_line_1based, block_lines_including_fences, fence_info).
    """
    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeDecodeError):
        return []

    lines = text.split("\n")
    blocks: list[tuple[int, list[str], str]] = []
    in_block = False
    block_start = -1
    fence_info = ""

    for i, line in enumerate(lines):
        if FENCE_RE.match(line):
            if not in_block:
                in_block = True
                block_start = i
                fence_info = line.strip()
            else:
                block_lines = lines[block_start : i + 1]
                inner = lines[block_start + 1 : i]
                if _has_box_chars(inner):
                    blocks.append((block_start + 1, block_lines, fence_info))
                in_block = False
                fence_info = ""

    return blocks


def collect(
    scan_dir: Path, exclude: Path | None = None
) -> list[tuple[Path, int, list[str]]]:
    """Walk scan_dir, return all (filepath, start_line, block_lines)."""
    results: list[tuple[Path, int, list[str]]] = []
    exclude_resolved = exclude.resolve() if exclude else None

    print("  Listing .md files...", end="", flush=True)
    md_files = sorted(
        f
        for f in scan_dir.rglob("*.md")
        if not any(part in SKIP_DIRS for part in f.parts)
        and (exclude_resolved is None or f.resolve() != exclude_resolved)
    )
    print(f" {len(md_files)} files")

    for i, fp in enumerate(md_files, 1):
        if i % 5000 == 0:
            print(f"  Scanned {i}/{len(md_files)} files, {len(results)} blocks so far",
                  flush=True)
        for start_line, block_lines, _fence in extract_blocks(fp):
            results.append((fp, start_line, block_lines))

    return results


def write_sample(
    results: list[tuple[Path, int, list[str]]],
    output: Path,
    scan_dir: Path,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = [
        "# ASCII Box-Drawing Samples",
        "",
        f"Auto-collected from `{scan_dir}`.",
        f"Total: **{len(results)}** code blocks from "
        f"**{len({str(fp) for fp, _, _ in results})}** files.",
        "",
        "---",
        "",
    ]

    for idx, (fp, start_line, block_lines) in enumerate(results, 1):
        try:
            rel = fp.relative_to(scan_dir)
        except ValueError:
            rel = fp
        lines.append(f"## Sample {idx:03d}")
        lines.append("")
        lines.append(f"**Source**: `{rel}` L{start_line}")
        lines.append("")
        lines.extend(block_lines)
        lines.append("")
        lines.append("---")
        lines.append("")

    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect ASCII box-drawing samples")
    parser.add_argument(
        "scan_dir",
        nargs="?",
        default="E:/github",
        help="Directory to scan (default: E:/github)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output file (default: <skill>/testcases/Ascii_sample.md)",
    )
    args = parser.parse_args()

    scan_dir = Path(args.scan_dir).resolve()
    if args.output:
        output = Path(args.output).resolve()
    else:
        script_dir = Path(__file__).resolve().parent
        output = script_dir.parent / "testcases" / "Ascii_sample.md"

    if not scan_dir.is_dir():
        print(f"Error: {scan_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning: {scan_dir}")
    results = collect(scan_dir, exclude=output)
    print(f"Found: {len(results)} blocks from {len({str(fp) for fp, _, _ in results})} files")

    write_sample(results, output, scan_dir)
    print(f"Written: {output}")


if __name__ == "__main__":
    main()
