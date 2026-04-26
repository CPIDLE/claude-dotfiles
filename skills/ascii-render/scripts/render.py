"""ascii-render v0.1 — Sarasa Mono TC ASCII art -> PNG.

Self-contained skill. Imports width / symbol tables from the sibling
`ascii-align` skill so width rules stay canonical across both skills.

Pipeline:
  scan *.md  ->  find ``` blocks containing box-drawing chars
              ->  optional symbol normalize (--normalize)
              ->  optional align lint (--check / --strict)
              ->  save extract to <out>/<stem>_L<line>.md
              ->  render polished PNG to <out>/<stem>_L<line>.png
              ->  emit <out>/_index.md
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

SKILL_ROOT = Path.home() / ".claude" / "skills"
ASCII_ALIGN = SKILL_ROOT / "ascii-align" / "scripts"
if not ASCII_ALIGN.exists():
    sys.exit(f"ERROR: requires ascii-align skill at {ASCII_ALIGN}")
sys.path.insert(0, str(ASCII_ALIGN))

from ascii_align import char_cols  # noqa: E402

VERSION = "ascii-render v0.1"

FONT_REG = "C:/Windows/Fonts/SarasaMonoTC-Regular.ttf"
SIZE = 28
LINE_PAD = 6
PAD = 90
PANEL_PAD = 44
FOOTER_GAP = 28

BG_OUTER = (240, 243, 248)
BG_PANEL = (255, 255, 255)
PANEL_BORDER = (225, 230, 240)
TEXT = (40, 50, 70)
ACCENT_BOX = (74, 144, 226)
ACCENT_ARROW = (160, 108, 213)
FOOTER = (130, 145, 165)
DRIFT_RED = (200, 60, 60)

BOX = set("─│┌┐└┘├┤┬┴┼")
ARROW_CHARS = set(">v^<")


def find_blocks(md_path: Path) -> list[tuple[int, str]]:
    lines = md_path.read_text(encoding="utf-8").splitlines()
    out: list[tuple[int, str]] = []
    in_block, start, buf = False, 0, []
    for i, ln in enumerate(lines, start=1):
        if ln.strip().startswith("```"):
            if not in_block:
                in_block, start, buf = True, i + 1, []
            else:
                content = "\n".join(buf)
                if any(ch in content for ch in BOX):
                    out.append((start, content))
                in_block = False
        elif in_block:
            buf.append(ln)
    return out


def _normalize_block(content: str) -> str:
    from symbol_fix import replace_symbols
    return "\n".join(replace_symbols(ln) for ln in content.splitlines())


def _check_drift(md_path: Path) -> int:
    """Run ascii-align --check; return drift count (0 if clean, >0 if drift)."""
    result = subprocess.run(
        [sys.executable, str(ASCII_ALIGN / "ascii_align.py"), "--check", str(md_path)],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        return 0
    # ascii-align --check exits non-zero on drift; count "drift" markers in output
    out = (result.stdout or "") + (result.stderr or "")
    return max(1, out.lower().count("drift"))


def render(
    ascii_src: str,
    source_name: str,
    line_no: int,
    out_png: Path,
    drift: int = 0,
) -> None:
    font = ImageFont.truetype(FONT_REG, SIZE)
    footer_font = ImageFont.truetype(FONT_REG, max(14, SIZE - 12))
    cell_px = int(round(font.getlength("M")))

    lines = ascii_src.rstrip("\n").splitlines() or [""]
    cell_h = SIZE + LINE_PAD
    max_cells = max(sum(char_cols(c) for c in ln) for ln in lines)
    text_w = max_cells * cell_px
    text_h = cell_h * len(lines)
    footer_h = 36

    panel_w = text_w + 2 * PANEL_PAD
    panel_h = text_h + 2 * PANEL_PAD + footer_h
    canvas_w = panel_w + 2 * PAD
    canvas_h = panel_h + 2 * PAD

    canvas = Image.new("RGB", (canvas_w, canvas_h), BG_OUTER)

    grad_mask = Image.new("L", (canvas_w, canvas_h), 0)
    gd = ImageDraw.Draw(grad_mask)
    cx, cy = canvas_w // 2, canvas_h // 2
    rmax = max(canvas_w, canvas_h) // 2
    for r in range(rmax, 0, -8):
        v = int(20 * (r / rmax))
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=v)
    grad_mask = grad_mask.filter(ImageFilter.GaussianBlur(40))
    dark = Image.new("RGB", (canvas_w, canvas_h), (210, 218, 230))
    canvas = Image.composite(dark, canvas, grad_mask)

    shadow = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle(
        [PAD + 6, PAD + 10, PAD + panel_w + 6, PAD + panel_h + 10],
        radius=18, fill=(0, 0, 0, 60))
    shadow = shadow.filter(ImageFilter.GaussianBlur(8))
    canvas = canvas.convert("RGBA")
    canvas.alpha_composite(shadow)
    canvas = canvas.convert("RGB")

    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle(
        [PAD, PAD, PAD + panel_w, PAD + panel_h],
        radius=18, fill=BG_PANEL, outline=PANEL_BORDER, width=1)

    cur_y = PAD + PANEL_PAD
    for r, line in enumerate(lines):
        y = cur_y + r * cell_h
        x = PAD + PANEL_PAD
        for ch in line:
            if ch in BOX:
                color = ACCENT_BOX
            elif ch in ARROW_CHARS:
                color = ACCENT_ARROW
            else:
                color = TEXT
            d.text((x, y), ch, font=font, fill=color)
            x += char_cols(ch) * cell_px

    footer_text = f"{source_name} . L{line_no}  ({VERSION})"
    fw = int(footer_font.getlength(footer_text))
    d.text((PAD + panel_w - PANEL_PAD - fw,
            PAD + panel_h - FOOTER_GAP),
           footer_text, font=footer_font, fill=FOOTER)

    if drift:
        drift_text = f"ALIGN: {drift} drift"
        d.text((PAD + PANEL_PAD,
                PAD + panel_h - FOOTER_GAP),
               drift_text, font=footer_font, fill=DRIFT_RED)

    canvas.save(out_png)


def _resolve_targets(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    if path.is_dir():
        return sorted(path.glob("*.md"))
    sys.exit(f"ERROR: not a file or directory: {path}")


def run(input_path: Path, out_dir: Path, normalize: bool, check: bool, strict: bool) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    mds = _resolve_targets(input_path)

    targets: list[tuple[Path, int, str, int]] = []
    total_drift = 0
    for md in mds:
        md_drift = _check_drift(md) if check else 0
        if md_drift:
            print(f"  ALIGN WARN {md.name}  ({md_drift} drift)", file=sys.stderr)
            total_drift += md_drift
        for start, content in find_blocks(md):
            if normalize:
                content = _normalize_block(content)
            targets.append((md, start, content, md_drift))

    print(f"{VERSION}  blocks: {len(targets)}  check={check} strict={strict} normalize={normalize}")

    if check and total_drift and strict:
        print(f"ALIGN FAIL: {total_drift} drift; not rendering (--strict)")
        return 1
    if check and total_drift == 0:
        print("  ALIGN OK")

    index = [f"# Render Index ({VERSION})\n",
             "| Source | Line | Lines | PNG |",
             "|--------|------|-------|-----|"]

    for md, start, content, md_drift in targets:
        stem = md.stem
        out_png = out_dir / f"{stem}_L{start}.png"
        render(content, md.name, start, out_png, drift=md_drift)
        n = content.count("\n") + 1
        print(f"  {stem}_L{start}  {n} lines  -> {out_png.name}")
        index.append(f"| {md.name} | L{start} | {n} | "
                     f"![{stem}_L{start}](./{out_png.name}) |")

    (out_dir / "_index.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    print(f"\nindex -> {out_dir/'_index.md'}")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(prog="ascii-render", description=__doc__)
    ap.add_argument("path", type=Path, help="Markdown file or directory")
    ap.add_argument("--normalize", action="store_true",
                    help="Normalize symbols (→ → -->) before rendering")
    ap.add_argument("--check", action="store_true",
                    help="Run ascii-align --check; annotate footer on drift")
    ap.add_argument("--strict", action="store_true",
                    help="With --check: exit 1 on any drift, do not render")
    ap.add_argument("--out", type=Path, default=None,
                    help="Output directory (default: <input_dir>/rendered/)")
    args = ap.parse_args()

    base = args.path if args.path.is_dir() else args.path.parent
    out_dir = args.out or (base / ".render")
    sys.exit(run(args.path, out_dir, args.normalize, args.check, args.strict))


if __name__ == "__main__":
    main()
