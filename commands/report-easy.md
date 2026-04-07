使用者需求：$ARGUMENTS

請使用 **report-easy** skill 將指定的 ASCII Markdown 報告轉為印刷就緒的雙版 HTML（A4 直 + 橫）。

## 三階段流程

1. **圖表化** — 掃描來源 `.md`，將適合視覺化的段落轉為 D2 (`--layout=elk`) 圖；不適合 D2 的圖（圓餅、甘特、序列、ER、心智圖等）才用 Mermaid。把結果寫入 `<stem>_elk.md`，新圖存放於 `assets/*.d2` + `assets/*_elk.png`。
2. **產生 直 HTML** — 套用 skill 內建的 `template_直.html`（A4 portrait，已強化 img sizing）。
3. **產生 橫 HTML** — 套用 skill 內建的 `template_橫.html`（A4 landscape）。

## 用法

```
/report-easy <source.md>
```

直接呼叫腳本（自包含、無外部路徑依賴）：

```bash
python ~/.claude/skills/report-easy/scripts/build_html.py <source_elk.md>
```

## 注意事項

- 數值圖（log-log、誤差曲線、散布圖、表格圖）保留原 matplotlib PNG，不要強行 D2 化
- D2 reserved keywords (`start`, `end`, `near`, `far`, `mid`, `top`, `bottom`, `left`, `right`, `center`, `source`, `target`) 不可作為節點名稱
- 含 `$` 的標籤需 `\$` 跳脫並雙引號包住
- 完成後告知使用者 HTML 路徑、新增的 D2/PNG 清單
