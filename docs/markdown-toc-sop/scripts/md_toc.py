#!/usr/bin/env python3
"""Generate / refresh a clickable table of contents for a long Markdown file.

Why not rely on auto-generated heading anchors: renderers disagree on how
non-ASCII headings are slugified, and some preview panes cancel in-page
navigation entirely (see markdown-toc-sop.md). This script writes explicit
`<a id="...">` anchors into the headings and links to them, so the anchor
targets are stable ASCII regardless of renderer.

Usage:
    python md_toc.py FILE [--max-level 3] [--title 目錄] [--plain] [--dry-run]

Re-running is safe: the TOC block is delimited by HTML comments and gets
replaced, and headings that already carry an anchor keep their existing id
(so links you pasted elsewhere keep working).
"""

import argparse
import re
import sys
from pathlib import Path

TOC_START = "<!-- TOC -->"
TOC_END = "<!-- /TOC -->"

ANCHOR_RE = re.compile(r'\s*<a id="([A-Za-z0-9_-]+)"></a>\s*$')
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")


def slugify(text):
    """ASCII slug from a heading. Returns '' when nothing usable remains."""
    text = re.sub(r"[*`~_]", "", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  # [label](url) -> label
    text = re.sub(r"<[^>]+>", "", text)  # strip inline html
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def split_toc_block(lines):
    """Return (before, after) with any existing TOC block removed."""
    try:
        i = lines.index(TOC_START)
        j = lines.index(TOC_END)
    except ValueError:
        return lines, None
    if j < i:
        raise SystemExit("錯誤：TOC 標記順序顛倒，請手動修掉再跑")
    return lines[:i] + lines[j + 1:], i


def collect_headings(lines, max_level, h3_under=None):
    """Yield (index, level, text, existing_id) for headings outside code fences.

    h3_under: list of substrings. When given, a heading deeper than h2 is kept
    only if the h2 it sits under contains one of them — lets a long file list
    every section but expand sub-sections in just the parts worth expanding.
    """
    in_fence = False
    out = []
    parent = ""
    for idx, line in enumerate(lines):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING_RE.match(line)
        if not m:
            continue
        level = len(m.group(1))
        text = m.group(2)
        if level == 2:
            parent = ANCHOR_RE.sub("", text)
        if level < 2 or level > max_level:
            continue
        if level > 2 and h3_under and not any(k in parent for k in h3_under):
            continue
        anchor = ANCHOR_RE.search(text)
        existing = anchor.group(1) if anchor else None
        if anchor:
            text = text[: anchor.start()].rstrip()
        out.append([idx, level, text, existing])
    return out


def assign_ids(headings):
    used = {h[3] for h in headings if h[3]}
    counter = 0
    for h in headings:
        if h[3]:
            continue
        base = slugify(h[2]) or "sec"
        candidate = base
        while candidate in used:
            counter += 1
            candidate = f"{base}-{counter}"
        used.add(candidate)
        h[3] = candidate
    return headings


def escape_text(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_toc(headings, title, plain):
    top = min(h[1] for h in headings)
    out = [TOC_START, "", f"{'#' * top} {title}", ""]
    for _, level, text, aid in headings:
        indent = "  " * (level - top)
        label = re.sub(r"\*\*", "", text)
        if plain:
            label = label.replace("[", r"\[").replace("]", r"\]")
            out.append(f"{indent}- [{label}](#{aid})")
        else:
            out.append(
                f'{indent}- <a href="#{aid}" '
                f"onclick=\"document.getElementById('{aid}').scrollIntoView();"
                f'return false;">{escape_text(label)}</a>'
            )
    out += ["", TOC_END]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--max-level", type=int, default=3,
                    help="最深納入目錄的標題層級（預設 3）")
    ap.add_argument("--title", default="目錄")
    ap.add_argument("--h3-under", default="",
                    help="逗號分隔的 h2 標題關鍵字；只有這些章節底下的次級標題會進目錄")
    ap.add_argument("--plain", action="store_true",
                    help="只產純 Markdown 連結，不加 onclick fallback")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    path = Path(args.file)
    lines = path.read_text(encoding="utf-8").split("\n")

    body, insert_at = split_toc_block(lines)
    h3_under = [s.strip() for s in args.h3_under.split(",") if s.strip()]
    headings = collect_headings(body, args.max_level, h3_under)
    if not headings:
        raise SystemExit("找不到任何 h2~h{} 標題，沒東西可做目錄".format(args.max_level))
    headings = assign_ids(headings)

    for idx, level, text, aid in headings:
        body[idx] = f'{"#" * level} {text} <a id="{aid}"></a>'

    if insert_at is None:
        insert_at = headings[0][0]
        # keep a blank line between the TOC block and what follows
        toc = render_toc(headings, args.title, args.plain) + ["", "---", ""]
    else:
        toc = render_toc(headings, args.title, args.plain)

    new = body[:insert_at] + toc + body[insert_at:]
    text_out = re.sub(r"\n{3,}", "\n\n", "\n".join(new))

    if args.dry_run:
        print("\n".join(toc))
        print(f"\n(dry-run) {len(headings)} 個標題，未寫檔", file=sys.stderr)
        return
    path.write_text(text_out, encoding="utf-8")
    print(f"OK: {path.name} — {len(headings)} 個標題，目錄已更新")


if __name__ == "__main__":
    main()
