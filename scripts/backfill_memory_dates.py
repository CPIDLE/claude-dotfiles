"""Backfill created/updated dates into memory frontmatter and normalize to nested metadata.

Usage:
    python backfill_memory_dates.py --dry-run
    python backfill_memory_dates.py --apply
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path

MEMORY_DIR = Path.home() / ".claude" / "projects" / "E--github-claude-dotfiles" / "memory"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
BODY_DATE_RE = re.compile(r"(?<![-\w])(20\d\d-\d\d-\d\d)(?![-\w])")

METADATA_KEYS = {"type", "originSessionId", "sessionId"}


def parse_frontmatter(text: str) -> tuple[dict, str, str] | None:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    raw = m.group(1)
    body = text[m.end():]
    return parse_yaml_simple(raw), raw, body


def parse_yaml_simple(raw: str) -> dict:
    """Parse a flat OR singly-nested frontmatter. Returns dict where 'metadata' is a sub-dict if present."""
    result: dict = {}
    current_section: str | None = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        if line.startswith("  ") and current_section:
            k, _, v = line.strip().partition(":")
            result[current_section][k.strip()] = v.strip()
            continue
        current_section = None
        k, _, v = line.partition(":")
        k = k.strip()
        v = v.strip()
        if not v:
            result[k] = {}
            current_section = k
        else:
            result[k] = v
    return result


def emit_frontmatter(data: dict) -> str:
    lines = ["---"]
    for key in ("name", "description"):
        if key in data:
            lines.append(f"{key}: {data[key]}")
    if "metadata" in data and isinstance(data["metadata"], dict):
        lines.append("metadata:")
        for k in ("type", "created", "updated", "originSessionId", "sessionId"):
            if k in data["metadata"]:
                lines.append(f"  {k}: {data['metadata'][k]}")
        for k, v in data["metadata"].items():
            if k not in {"type", "created", "updated", "originSessionId", "sessionId"}:
                lines.append(f"  {k}: {v}")
    for k, v in data.items():
        if k in {"name", "description", "metadata"}:
            continue
        lines.append(f"{k}: {v}")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def normalize(data: dict) -> dict:
    """Move flat metadata keys under 'metadata' sub-dict."""
    out = dict(data)
    existing = out.get("metadata")
    md: dict = existing if isinstance(existing, dict) else {}
    for k in list(out.keys()):
        if k in METADATA_KEYS:
            md.setdefault(k, out.pop(k))
    out["metadata"] = md
    return out


def earliest_body_date(body: str) -> date | None:
    dates = []
    for s in BODY_DATE_RE.findall(body):
        try:
            dates.append(datetime.strptime(s, "%Y-%m-%d").date())
        except ValueError:
            pass
    return min(dates) if dates else None


def process(path: Path, apply: bool) -> str:
    text = path.read_text(encoding="utf-8")
    parsed = parse_frontmatter(text)
    if parsed is None:
        return f"SKIP (no frontmatter): {path.name}"
    data, _, body = parsed
    data = normalize(data)
    md = data["metadata"]

    mtime_date = datetime.fromtimestamp(path.stat().st_mtime).date()
    created = md.get("created") or mtime_date.isoformat()
    updated = md.get("updated") or mtime_date.isoformat()

    md["created"] = created
    md["updated"] = updated

    new_fm = emit_frontmatter(data)
    new_text = new_fm + body.lstrip("\n") if body.startswith("\n") else new_fm + body

    if new_text == text:
        return f"unchanged: {path.name}"

    if apply:
        path.write_text(new_text, encoding="utf-8", newline="\n")
        return f"WROTE   {path.name}  created={created} updated={updated}"
    return f"WOULD   {path.name}  created={created} updated={updated}"


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    files = sorted(p for p in MEMORY_DIR.glob("*.md") if p.name != "MEMORY.md")
    for p in files:
        print(process(p, apply=args.apply))
    print(f"\nTotal: {len(files)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
