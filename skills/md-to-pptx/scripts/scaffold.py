#!/usr/bin/env python3
"""scaffold.py — MD → create_pptx.js scaffold (Auto v0).

Reads a Markdown source and emits a PptxGenJS skeleton:
  - 1 titleSlide  per H1 (first one)
  - 1 sectionSlide per H2
  - 1 contentSlide per H3, with a comment summarizing what MD content sits under it
    (tables / cards / bullets / blockquotes / images / code) so cc or the user can
    fill in the helper calls afterwards.

Pagination, content rendering, and visual layouts are intentionally NOT generated —
this scaffold matches the V1 playbook idea that PPTX content is hand-orchestrated.

Usage:
  python scaffold.py <source.md> [--out out.js] [--helpers <path>] [--run]
"""
from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
from pathlib import Path


# ---------- MD parsing ----------

def parse_md(text: str) -> list[dict]:
    """Tokenize MD into a flat block list (h1/h2/h3, table, list, blockquote, image, code, paragraph)."""
    lines = text.splitlines()
    blocks: list[dict] = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()

        m = re.match(r"^(#{1,4}) +(.+)", line)
        if m:
            blocks.append({"type": f"h{len(m.group(1))}", "text": m.group(2).strip()})
            i += 1
            continue

        if stripped.startswith("|") and i + 1 < n and re.match(r"^\|[\s\-:|]+\|$", lines[i + 1].strip()):
            headers = [c.strip() for c in stripped.strip("|").split("|")]
            i += 2
            rows: list[list[str]] = []
            while i < n and lines[i].strip().startswith("|") and not re.match(r"^\|[\s\-:|]+\|$", lines[i].strip()):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            blocks.append({"type": "table", "headers": headers, "rows": rows})
            continue

        m = re.match(r"^!\[(.*?)\]\((.+?)\)\s*$", stripped)
        if m:
            blocks.append({"type": "image", "alt": m.group(1), "src": m.group(2)})
            i += 1
            continue

        if stripped.startswith("> "):
            quote = []
            while i < n and lines[i].lstrip().startswith(">"):
                quote.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            blocks.append({"type": "blockquote", "text": "\n".join(quote).strip()})
            continue

        if re.match(r"^[-*+] +", line):
            items = []
            while i < n and re.match(r"^[-*+] +", lines[i]):
                items.append(re.sub(r"^[-*+] +", "", lines[i]).strip())
                i += 1
                while i < n and lines[i].startswith(("  ", "\t")):
                    items[-1] += " " + lines[i].strip()
                    i += 1
            blocks.append({"type": "list", "items": items})
            continue

        if stripped.startswith("```"):
            i += 1
            code = []
            while i < n and not lines[i].lstrip().startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1
            blocks.append({"type": "code", "text": "\n".join(code)})
            continue

        if re.match(r"^-{3,}\s*$", stripped):
            i += 1
            continue

        if stripped:
            para = [stripped]
            i += 1
            while i < n and lines[i].strip() and not re.match(r"^(#{1,6} |[-*+] |!\[|\||> |```|-{3,}\s*$)", lines[i].lstrip()):
                para.append(lines[i].strip())
                i += 1
            blocks.append({"type": "paragraph", "text": " ".join(para)})
            continue

        i += 1
    return blocks


# ---------- Slide grouping + hint detection ----------

CARD_ITEM_RE = re.compile(r"^\*\*([^*]+)\*\*\s*[:：]?\s*(.*)$")


def detect_card_list(items: list[str]) -> bool:
    if not 3 <= len(items) <= 9:
        return False
    matches = sum(1 for it in items if CARD_ITEM_RE.match(it))
    return matches / len(items) >= 0.6


def summarize_block(b: dict) -> str:
    t = b["type"]
    if t == "table":
        return f"table ({len(b['rows'])}r × {len(b['headers'])}c)"
    if t == "list":
        return f"cards ({len(b['items'])} items)" if detect_card_list(b["items"]) else f"bullets ({len(b['items'])} items)"
    if t == "blockquote":
        return "infobox (blockquote)"
    if t == "image":
        return f"image: {Path(b['src']).name}"
    if t == "code":
        nlines = len(b["text"].splitlines())
        return f"code block ({nlines} lines)"
    if t == "paragraph":
        return f"paragraph ({len(b['text'])} chars)"
    return t


def short_section_label(h2_text: str, max_len: int = 14) -> str:
    """Strip leading 'N. ' numbering and trim — used as header-bar text."""
    t = re.sub(r"^\d+\.\s*", "", h2_text).strip()
    return t if len(t) <= max_len else t[:max_len] + "…"


def group_slides(blocks: list[dict]) -> list[dict]:
    """Walk blocks and group into slide entries (each content slide carries its raw blocks)."""
    slides: list[dict] = []
    h1 = None
    h1_intro: list[str] = []
    current_h2 = None
    current_h3 = None
    h3_blocks: list[dict] = []

    def flush_h3():
        if current_h3:
            slides.append({
                "kind": "content",
                "section": short_section_label(current_h2) if current_h2 else "",
                "title": current_h3,
                "hints": [summarize_block(b) for b in h3_blocks],
                "blocks": list(h3_blocks),
            })

    for b in blocks:
        t = b["type"]
        if t == "h1":
            if h1 is None:
                h1 = b["text"]
            continue
        if t == "h2":
            flush_h3()
            current_h3 = None
            h3_blocks = []
            current_h2 = b["text"]
            slides.append({"kind": "section", "title": current_h2})
            continue
        if t == "h3":
            flush_h3()
            current_h3 = b["text"]
            h3_blocks = []
            continue
        if current_h3 is None and current_h2 is None and h1 is not None:
            if t == "paragraph":
                h1_intro.append(b["text"])
            continue
        if current_h3 is not None:
            if t == "h4":
                h3_blocks.append({"type": "subheading", "text": b["text"]})
            else:
                h3_blocks.append(b)
    flush_h3()

    title_slide = {"kind": "title", "title": h1 or "Untitled", "intro": h1_intro}
    return [title_slide] + slides


# ---------- Content emission (auto-fill) ----------

CELL_BOLD_RE = re.compile(r"^\*\*(.+?)\*\*$")
EMPHASIS_RE = re.compile(r"\*\*([^*]+?)\*\*")
WARN_KEYWORDS = ("⚠", "注意", "警告", "重要", "更新", "Caveat", "Warning", "確認版", "重大", "釐清")
MERMAID_PREFIXES = ("graph ", "flowchart", "sequencediagram", "gantt", "classdiagram", "erdiagram", "pie", "mindmap", "statediagram", "journey")


def strip_inline_md(t: str) -> str:
    t = EMPHASIS_RE.sub(r"\1", t)
    t = re.sub(r"`([^`]+)`", r"\1", t)
    return t.strip()


def js_table_cell(text: str) -> str:
    text = text.strip()
    if not text:
        return js_str("")
    m = CELL_BOLD_RE.match(text)
    if m:
        return f"{{text: {js_str(strip_inline_md(m.group(1)))}, color: C.red, bold: true}}"
    return js_str(strip_inline_md(text))


def estimate_col_widths(headers: list[str], rows: list[list[str]], total_w: float = 9.2) -> list[float]:
    n = len(headers)
    if n == 0:
        return []
    max_chars = [len(strip_inline_md(headers[i])) for i in range(n)]
    for r in rows:
        for i in range(min(n, len(r))):
            max_chars[i] = max(max_chars[i], len(strip_inline_md(r[i])))
    max_chars = [max(c, 4) for c in max_chars]
    total = sum(max_chars)
    widths = [round(total_w * c / total, 2) for c in max_chars]
    diff = round(total_w - sum(widths), 2)
    widths[-1] = round(widths[-1] + diff, 2)
    return widths


def infobox_bg(text: str) -> str:
    if any(k in text for k in WARN_KEYWORDS):
        return "C.warnBg"
    return "C.infoBg"


def parse_card_item(item: str) -> dict | None:
    m = CARD_ITEM_RE.match(item)
    if not m:
        return None
    return {"title": strip_inline_md(m.group(1)), "desc": strip_inline_md(m.group(2))}


def is_mermaid_code(text: str) -> bool:
    first = text.lstrip().split("\n", 1)[0].strip().lower()
    return any(first.startswith(p) for p in MERMAID_PREFIXES)


def block_height(b: dict) -> float:
    t = b["type"]
    if t == "table":
        return 0.4 + 0.3 * len(b["rows"])
    if t == "list":
        if detect_card_list(b["items"]):
            return math.ceil(len(b["items"]) / 3) * 1.55
        h = 0.3
        for it in b["items"]:
            wraps = max(1, (len(strip_inline_md(it)) + 79) // 80)
            h += 0.28 * wraps
        return h
    if t == "blockquote":
        return 0.5 + 0.2 * (len(b["text"]) // 100)
    if t == "image":
        return 3.5
    if t == "code":
        if is_mermaid_code(b["text"]):
            return 1.5  # reserved for manual flowChain replacement
        return 0.4 + 0.18 * len(b["text"].splitlines())
    if t == "paragraph":
        return 0.3 + 0.2 * max(0, (len(b["text"]) - 60) // 80)
    if t == "subheading":
        return 0.35
    return 0.3


def emit_block(b: dict, y: float) -> tuple[list[str], float]:
    """Return (js_lines, new_y) for one MD block placed at `y`."""
    lines: list[str] = []
    t = b["type"]

    if t == "table":
        headers_js = "[" + ", ".join(js_str(strip_inline_md(h)) for h in b["headers"]) + "]"
        col_widths = estimate_col_widths(b["headers"], b["rows"])
        row_lines = []
        for r in b["rows"]:
            cells = [js_table_cell(c) for c in r]
            row_lines.append("    [" + ", ".join(cells) + "]")
        rows_js = "[\n" + ",\n".join(row_lines) + "\n  ]"
        opts = f"{{ y: {y:.2f}, colW: {json.dumps(col_widths)}, fontSize: 9 }}"
        lines.append(f"makeTable(s,\n  {headers_js},\n  {rows_js},\n  {opts}\n);")
        return lines, y + block_height(b) + 0.1

    if t == "list":
        if detect_card_list(b["items"]):
            cards = []
            for it in b["items"]:
                parsed = parse_card_item(it)
                if parsed:
                    cards.append(parsed)
                else:
                    cards.append({"title": "", "desc": strip_inline_md(it)})
            items_js = ",\n  ".join(
                f"{{ title: {js_str(c['title'])}, desc: {js_str(c['desc'])} }}" for c in cards
            )
            cols = 3 if len(cards) >= 3 else len(cards)
            lines.append(f"cardsGrid(s, [\n  {items_js}\n], {{ y: {y:.2f}, cols: {cols} }});")
        else:
            items_js = ", ".join(js_str(strip_inline_md(it)) for it in b["items"])
            lines.append(f"bulletList(s, [{items_js}], {{ y: {y:.2f} }});")
        return lines, y + block_height(b) + 0.15

    if t == "blockquote":
        text = strip_inline_md(b["text"].replace("\n", " "))
        bg = infobox_bg(text)
        lines.append(f"addInfoBox(s, {js_str(text)}, {{ y: {y:.2f}, bg: {bg} }});")
        return lines, y + block_height(b) + 0.1

    if t == "image":
        src = b["src"]
        caption = strip_inline_md(b["alt"])
        path_js = f"path.join(__dirname, {js_str(src)})"
        lines.append(f"imageWithCaption(s, {path_js}, {js_str(caption)}, {{ y: {y:.2f} }});")
        return lines, y + block_height(b) + 0.1

    if t == "code":
        if is_mermaid_code(b["text"]):
            snippet = b["text"][:50].replace("\n", " ")
            lines.append(f"// MERMAID PLACEHOLDER (y={y:.2f}, h=1.5) — replace with flowChain or addShape diagram")
            lines.append(f"//   preview: {snippet!r}")
            return lines, y + 1.5 + 0.1
        h = block_height(b)
        lines.append(
            f"s.addText({js_str(b['text'])}, {{ x: 0.4, y: {y:.2f}, w: 9.2, h: {h:.2f}, "
            f'fontSize: 8.5, fontFace: "Sarasa Mono TC", color: C.darkText, '
            f"fill: {{ color: C.tableAlt }}, margin: 6, valign: \"top\" }});"
        )
        return lines, y + h + 0.1

    if t == "paragraph":
        text = strip_inline_md(b["text"])
        lines.append(f"bulletList(s, [{js_str(text)}], {{ y: {y:.2f} }});")
        return lines, y + block_height(b) + 0.15

    if t == "subheading":
        text = strip_inline_md(b["text"])
        lines.append(
            f"s.addText({js_str(text)}, {{ x: 0.4, y: {y:.2f}, w: 9.2, h: 0.3, "
            f'fontSize: 13, fontFace: "Arial", color: C.darkText, bold: true, margin: 0 }});'
        )
        return lines, y + 0.4

    return lines, y


# ---------- Auto-split (shared by JS + HTML emitters so paginations match) ----------

PAGE_Y_BUDGET = 4.95


def split_content_slides(slides: list[dict]) -> list[dict]:
    """Take raw slides; for content slides, pack blocks into sub-slides by height budget.
    Returns a flat list where each entry is exactly one rendered slide."""
    final: list[dict] = []
    for sl in slides:
        if sl["kind"] != "content":
            final.append(sl)
            continue
        pages_blocks: list[list[dict]] = []
        cur: list[dict] = []
        y = 1.4
        for b in sl["blocks"]:
            bh = block_height(b)
            if bh > 0 and y + bh > PAGE_Y_BUDGET and cur:
                pages_blocks.append(cur)
                cur = []
                y = 1.4
            cur.append(b)
            y += bh + 0.1
        if cur:
            pages_blocks.append(cur)
        for i, blocks in enumerate(pages_blocks):
            suffix = "" if i == 0 else ("（續）" if i == 1 else f"（續 {i}）")
            final.append({
                "kind": "content",
                "section": sl["section"],
                "title": sl["title"] + suffix,
                "blocks": blocks,
                "hints": sl.get("hints", []) if i == 0 else [],
                "is_continuation": i > 0,
            })
    return final


# ---------- Marp MD emission (Stage 0: delegate to report-gyro's Marp pipeline) ----------

def serialize_block_md(b: dict) -> str:
    t = b["type"]
    if t == "table":
        lines = ["| " + " | ".join(b["headers"]) + " |",
                 "|" + "|".join("---" for _ in b["headers"]) + "|"]
        for r in b["rows"]:
            lines.append("| " + " | ".join(r) + " |")
        return "\n".join(lines)
    if t == "list":
        return "\n".join(f"- {it}" for it in b["items"])
    if t == "blockquote":
        return "\n".join(f"> {line}" for line in b["text"].split("\n"))
    if t == "image":
        return f"![{b['alt']}]({b['src']})"
    if t == "code":
        lang = "mermaid" if is_mermaid_code(b["text"]) else ""
        return f"```{lang}\n{b['text']}\n```"
    if t == "paragraph":
        return b["text"]
    if t == "subheading":
        return f"#### {b['text']}"
    return ""


def emit_marp_md(slides_final: list[dict], doc_title: str, doc_label: str) -> str:
    out = [
        "---",
        "marp: true",
        "theme: gyro",
        "paginate: true",
        f"title: {doc_title}",
        f"footer: {doc_label}",
        "---",
        "",
    ]
    current_section = ""
    first = True
    for sl in slides_final:
        if not first:
            out.append("\n---\n")
        first = False
        if sl["kind"] == "title":
            out.append("<!-- _class: cover -->")
            out.append("")
            out.append(f"# {sl['title']}")
            out.append("")
            out.append("TODO subtitle")
            out.append("")
            out.append("TODO YYYY/MM/DD · TODO tagline")
        elif sl["kind"] == "section":
            current_section = short_section_label(sl["title"])
            out.append("<!-- _class: section -->")
            out.append("")
            out.append(f"## {sl['title']}")
        elif sl["kind"] == "content":
            if current_section:
                out.append(f"<!-- _header: {current_section} -->")
                out.append("")
            out.append(f"### {sl['title']}")
            out.append("")
            for b in sl["blocks"]:
                out.append(serialize_block_md(b))
                out.append("")
    return "\n".join(out)


# ---------- (removed) custom slide-HTML emission — Stage 0 now uses Marp instead ----------



# ---------- JS emission ----------

def js_str(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


HEADER_TMPL = '''const pptxgen = require("pptxgenjs");
const path = require("path");
const {{ build }} = require({helpers_require});

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "GYRO Systems, Inc.";
pres.title = {title};

const {{ C, addFooter, addHeaderBar, addSlideTitle, contentSlide, sectionSlide, titleSlide, makeTable, addInfoBox, cardsGrid, bulletList, imageWithCaption, flowChain }} = build(pres, {{
  company: "GYRO SYSTEMS, INC.",
  docLabel: {doc_label},
}});

let s;
let pageNum = 0;
let currentSection = "";

'''

FOOTER_TMPL = '''pres.writeFile({{ fileName: path.join(__dirname, {out_pptx}) }}).then(f => console.log("PPTX created: " + f));
'''


def emit_js(slides: list[dict], helpers_path: Path, out_pptx_name: str, doc_label: str) -> str:
    out: list[str] = []
    title_slide = slides[0]
    out.append(HEADER_TMPL.format(
        helpers_require=js_str(str(helpers_path).replace("\\", "/")),
        title=js_str(title_slide["title"]),
        doc_label=js_str(doc_label),
    ))

    out.append("// ============================================================")
    out.append("// PAGE 1: Title")
    out.append("// ============================================================")
    out.append("titleSlide({")
    out.append(f"  title: {js_str(title_slide['title'])},")
    out.append(f"  subtitle: \"TODO subtitle\",")
    out.append(f"  date: \"TODO YYYY/MM/DD\",")
    out.append(f"  tagline: \"TODO one-line tagline\",")
    out.append("});")
    out.append("")

    page = 1
    for sl in slides[1:]:
        page += 1
        if sl["kind"] == "section":
            short = short_section_label(sl["title"])
            out.append("// ============================================================")
            out.append(f"// PAGE {page}: Section — {sl['title']}")
            out.append("// ============================================================")
            out.append(f"currentSection = {js_str(short)};")
            out.append(f"sectionSlide({js_str(sl['title'])}, \"\");  // TODO: optional subtitle")
            out.append("")
        elif sl["kind"] == "content":
            out.append("// ============================================================")
            tag = " (continuation)" if sl.get("is_continuation") else ""
            out.append(f"// PAGE {page}: {sl['title']}{tag}")
            if sl["hints"]:
                out.append("// MD hints: " + "; ".join(sl["hints"]))
            out.append("// ============================================================")
            section_expr = f"currentSection || {js_str(sl['section'])}" if sl["section"] else "currentSection"
            out.append(f"s = contentSlide({section_expr}, ++pageNum, {js_str(sl['title'])});")
            y = 1.4
            for b in sl["blocks"]:
                block_lines, y = emit_block(b, y)
                out.extend(block_lines)
            out.append("")

    out.append(FOOTER_TMPL.format(out_pptx=js_str(out_pptx_name)))
    return "\n".join(out)


# ---------- CLI ----------

def main() -> int:
    here = Path(__file__).resolve().parent
    default_helpers = (here.parent / "template" / "pptx_helpers.js").resolve()

    ap = argparse.ArgumentParser(description="MD → create_pptx.js (auto-fill, V1 playbook compliant).")
    ap.add_argument("md", help="path to source markdown")
    ap.add_argument("--out", default=None, help="output .js path (default: <stem>_create_pptx.js beside MD)")
    ap.add_argument("--helpers", default=str(default_helpers), help="path to pptx_helpers.js")
    ap.add_argument("--run", action="store_true", help="run `node <out>` after generation to emit .pptx")
    ap.add_argument("--skip-html", action="store_true",
                    help="skip Stage 0 (Marp HTML preview). NOT recommended — HTML is the visual baseline")
    ap.add_argument("--marp-theme",
                    default=str((here.parent.parent / "report-gyro" / "assets" / "gyro-marp-theme.css").resolve()),
                    help="path to GYRO Marp theme CSS (auto-detected via sibling report-gyro skill)")
    args = ap.parse_args()

    md_path = Path(args.md).resolve()
    if not md_path.exists():
        print(f"error: not found: {md_path}", file=sys.stderr)
        return 2
    out_path = Path(args.out).resolve() if args.out else md_path.with_name(md_path.stem + "_create_pptx.js")
    pptx_name = md_path.with_suffix(".pptx").name
    doc_label = md_path.stem
    helpers_abs = Path(args.helpers).resolve()
    if not helpers_abs.exists():
        print(f"error: helpers not found: {helpers_abs}", file=sys.stderr)
        return 2

    # Parse + group + auto-split (shared by both emitters so HTML preview matches PPTX)
    blocks = parse_md(md_path.read_text(encoding="utf-8"))
    slides_raw = group_slides(blocks)
    slides_final = split_content_slides(slides_raw)

    # Stage 0: produce Marp slide HTML using report-gyro's GYRO theme.
    # V1 playbook §0 — PPTX 樣式以 HTML 為視覺基準。每個 `---` 切點對應一張 PPTX slide。
    if not args.skip_html:
        marp_md_path = md_path.with_name(md_path.stem + "_marp.md")
        html_path = md_path.with_name(md_path.stem + "_slides.html")
        marp_md = emit_marp_md(slides_final, doc_title=md_path.stem, doc_label=doc_label)
        marp_md_path.write_text(marp_md, encoding="utf-8")
        print(f"[Stage 0a] MD -> Marp MD -> {marp_md_path}")

        theme = Path(args.marp_theme)
        if not theme.exists():
            print(f"  WARNING: GYRO theme not found at {theme} — Marp will use default theme", file=sys.stderr)
            theme_args: list[str] = []
        else:
            theme_args = ["--theme", str(theme)]
        marp_cmd = ["marp", str(marp_md_path), "--html", "--allow-local-files", *theme_args, "-o", str(html_path)]
        # Windows: marp installs as marp.cmd; use shell=True so PATH resolution works for both .cmd and POSIX
        r = subprocess.run(marp_cmd, capture_output=True, text=True, shell=(sys.platform == "win32"))
        if r.returncode == 0:
            print(f"[Stage 0b] Marp -> slide HTML -> {html_path}")
            print(f"  ** OPEN THIS HTML IN BROWSER FIRST — Marp's built-in nav (←→ / click) **")
        else:
            print(f"  WARNING: marp failed (exit {r.returncode}): {r.stderr.strip()[:200]}", file=sys.stderr)

    # Stage 1: PptxGenJS scaffold (uses identical slide split as HTML)
    js = emit_js(slides_final, helpers_abs, pptx_name, doc_label)
    out_path.write_text(js, encoding="utf-8")

    n_title = sum(1 for sl in slides_final if sl["kind"] == "title")
    n_section = sum(1 for sl in slides_final if sl["kind"] == "section")
    n_content = sum(1 for sl in slides_final if sl["kind"] == "content")
    n_cont = sum(1 for sl in slides_final if sl.get("is_continuation"))
    print(f"[Stage 1] MD -> JS: {len(slides_final)} slides ({n_title} title + {n_section} section + {n_content} content"
          f"{f' incl {n_cont} auto-continued' if n_cont else ''}) -> {out_path}")

    if args.run:
        env_node_path = subprocess.check_output(["npm", "root", "-g"], shell=True).decode().strip()
        import os
        env = os.environ.copy()
        env["NODE_PATH"] = env_node_path
        print(f"running: node {out_path}")
        r = subprocess.run(["node", str(out_path)], cwd=str(out_path.parent), env=env)
        return r.returncode
    return 0


if __name__ == "__main__":
    sys.exit(main())
