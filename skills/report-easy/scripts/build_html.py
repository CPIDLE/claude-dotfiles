#!/usr/bin/env python3
"""
report-easy: build 直/橫 HTML from a markdown report.

Usage:
  python build_html.py <source.md> [title]

Outputs (in same dir as source.md):
  <stem>_直.html
  <stem>_橫.html

Templates are loaded from ../assets/ (relative to this script), so the
skill is fully portable — no absolute paths.
"""
import os, re, sys

def build(src_md: str, title: str | None = None) -> None:
    src_md = os.path.abspath(src_md)
    if not os.path.isfile(src_md):
        sys.exit(f"source not found: {src_md}")

    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets = os.path.join(skill_dir, "assets")

    md = open(src_md, encoding="utf-8").read()
    # Escape closing </script> inside markdown to avoid breaking the inline script tag
    md_escaped = md.replace("</script>", "<\\/script>")

    stem = os.path.splitext(os.path.basename(src_md))[0]
    out_dir = os.path.dirname(src_md)
    if not title:
        # First H1 if available
        m = re.search(r"^#\s+(.+)$", md, re.MULTILINE)
        title = m.group(1).strip() if m else stem

    # 直 版本暫時停用
    # for kind, suffix in [("直", "_直"), ("橫", "_橫")]:
    for kind, suffix in [("橫", "_橫")]:
        tpl_path = os.path.join(assets, f"template_{kind}.html")
        tpl = open(tpl_path, encoding="utf-8").read()
        out = (tpl
               .replace("{{TITLE}}", f"{title}（{kind}）")
               .replace("{{MARKDOWN_CONTENT}}", md_escaped))
        out_path = os.path.join(out_dir, f"{stem}{suffix}.html")
        open(out_path, "w", encoding="utf-8").write(out)
        print(out_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: build_html.py <source.md> [title]")
    build(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
