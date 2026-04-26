---
name: ascii-render
description: >
  Render ASCII-art code blocks in Markdown files to polished PNG images
  using Sarasa Mono TC font (drop shadow, rounded white panel, color-coded
  box/arrow/text). Use when the user wants to visualize ASCII diagrams,
  produce report-ready images, or preview alignment results.
  Trigger when: /ascii-render, render ASCII, ASCII 渲染, 產 PNG, 視覺化 ASCII.
argument-hint: "[file.md | dir] [--normalize] [--check] [--strict]"
---

# ascii-render

把 Markdown 中含 box-drawing (`─│┌┐└┘├┤┬┴┼`) 的 fenced code block 渲染成 PNG。
**只做視覺輸出**，對齊檢查/修復交給 `/ascii-align`。

預設輸出到 **原檔同層** 的 `.render/` 資料夾，檔名 `<stem>_L<line>.png`（line = block 起始行號）。不產生中間 `.md` 檔。

## 用法

```bash
# 單檔 / 目錄
python ~/.claude/skills/ascii-render/scripts/render.py <file.md | dir>

# 渲染前先 normalize 符號（→ → -->、▼ → v 等寬度守恆替代）
python ~/.claude/skills/ascii-render/scripts/render.py <path> --normalize

# 渲染前呼叫 ascii-align --check，drift 數印到 footer
python ~/.claude/skills/ascii-render/scripts/render.py <path> --check

# 任何 drift 就 exit 1，不產 PNG
python ~/.claude/skills/ascii-render/scripts/render.py <path> --check --strict

# 自訂輸出目錄（預設 <input_dir>/.render/）
python ~/.claude/skills/ascii-render/scripts/render.py <path> --out <dir>
```

## 安裝相依

```bash
pip install -r ~/.claude/skills/ascii-render/requirements.txt
```

字型：`C:/Windows/Fonts/SarasaMonoTC-Regular.ttf`（Windows）。其他平台需自行裝 Sarasa Mono TC 並改 `render.py::FONT_REG`。

## 跨 skill 相依

依賴 `~/.claude/skills/ascii-align/scripts/`：
- `ascii_align.char_cols` — Sarasa Mono TC 寬度查表
- `symbol_fix.replace_symbols` — `--normalize` 模式
- `ascii_align.py --check` — `--check` / `--strict` 模式

## Width 規則

見 `~/.claude/CLAUDE.md` "ASCII Art Diagrams（Sarasa Mono TC）" 章節，與 `/ascii-align` 共用同一份白名單與符號替代表。
