#!/usr/bin/env python3
"""collect_samples.py — Collect ASCII box-drawing code blocks from .md files.

Scans a directory tree for Markdown files, extracts fenced code blocks that
contain box-drawing characters, and writes them to a dated sample file
for ascii-align testing.

Output is named Ascii_sample_YYYY-MM-DD.md and set to read-only after writing.
Incremental mode: if a previous dated sample exists, only scans files created
after that date.

Usage:
    python collect_samples.py [scan_dir] [-o output_path] [--full]

    scan_dir     Directory to scan (default: E:/github)
    -o path      Output file (overrides default dated filename)
    --full       Ignore previous sample date, do a full scan
"""

from __future__ import annotations

import argparse
import os
import re
import stat
import sys
from datetime import date, datetime
from pathlib import Path

BOX_CHARS = set("┌┐└┘│─├┤┬┴┼")
FENCE_RE = re.compile(r"^ {0,3}```")
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", ".tox"}
SAMPLE_RE = re.compile(r"^Ascii_sample_(\d{4}-\d{2}-\d{2})\.md$")


def _has_box_chars(lines: list[str]) -> bool:
    return any(c in BOX_CHARS for line in lines for c in line)


def _find_latest_sample(testcases_dir: Path) -> date | None:
    """Find the most recent Ascii_sample_YYYY-MM-DD.md and return its date."""
    if not testcases_dir.is_dir():
        return None
    latest: date | None = None
    for f in testcases_dir.iterdir():
        m = SAMPLE_RE.match(f.name)
        if m:
            d = date.fromisoformat(m.group(1))
            if latest is None or d > latest:
                latest = d
    return latest


def _file_ctime(fp: Path) -> datetime:
    """Return file creation time (birth time on Windows, ctime on Unix)."""
    return datetime.fromtimestamp(fp.stat().st_ctime)


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
    scan_dir: Path,
    exclude_dir: Path | None = None,
    after: date | None = None,
) -> list[tuple[Path, int, list[str]]]:
    """Walk scan_dir, return all (filepath, start_line, block_lines).

    If *after* is given, only process files created after that date.
    """
    results: list[tuple[Path, int, list[str]]] = []
    exclude_resolved = exclude_dir.resolve() if exclude_dir else None
    after_dt = datetime(after.year, after.month, after.day) if after else None

    print("  Listing .md files...", end="", flush=True)
    md_files = sorted(
        f
        for f in scan_dir.rglob("*.md")
        if not any(part in SKIP_DIRS for part in f.parts)
        and (exclude_resolved is None or not f.resolve().is_relative_to(exclude_resolved))
    )
    print(f" {len(md_files)} files")

    skipped = 0
    for i, fp in enumerate(md_files, 1):
        if i % 5000 == 0:
            print(
                f"  Scanned {i}/{len(md_files)} files, "
                f"{len(results)} blocks so far (skipped {skipped})",
                flush=True,
            )
        if after_dt is not None:
            try:
                if _file_ctime(fp) <= after_dt:
                    skipped += 1
                    continue
            except OSError:
                pass
        for start_line, block_lines, _fence in extract_blocks(fp):
            results.append((fp, start_line, block_lines))

    if skipped:
        print(f"  Skipped {skipped} files older than {after}")

    return results


def write_sample(
    results: list[tuple[Path, int, list[str]]],
    output: Path,
    scan_dir: Path,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)

    # If output exists and is read-only, make writable before overwriting
    if output.exists():
        output.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)

    lines: list[str] = [
        "# ASCII Box-Drawing Samples",
        "",
        f"Auto-collected from `{scan_dir}` on {date.today().isoformat()}.",
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

    # Set read-only
    output.chmod(stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)


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
        help="Output file (overrides default dated filename)",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Full scan — ignore previous sample date",
    )
    args = parser.parse_args()

    scan_dir = Path(args.scan_dir).resolve()
    script_dir = Path(__file__).resolve().parent
    testcases_dir = script_dir.parent / "testcases"

    if args.output:
        output = Path(args.output).resolve()
    else:
        today = date.today().isoformat()
        output = testcases_dir / f"Ascii_sample_{today}.md"

    if not scan_dir.is_dir():
        print(f"Error: {scan_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    # Guard: don't overwrite existing read-only sample unless --full
    if output.exists() and not args.full:
        if not os.access(output, os.W_OK):
            print(f"Already exists (read-only): {output}")
            print("Use --full to rescan and overwrite.")
            return

    # Determine incremental cutoff
    after: date | None = None
    if not args.full:
        after = _find_latest_sample(testcases_dir)
        if after:
            print(f"Incremental mode: only files created after {after}")
        else:
            print("No previous sample found — full scan")

    print(f"Scanning: {scan_dir}")
    results = collect(scan_dir, exclude_dir=testcases_dir, after=after)
    print(f"Found: {len(results)} blocks from {len({str(fp) for fp, _, _ in results})} files")

    if not results:
        print("No new samples found. Use --full to force a full scan.")
        return

    write_sample(results, output, scan_dir)
    print(f"Written: {output} (read-only)")


if __name__ == "__main__":
    main()
