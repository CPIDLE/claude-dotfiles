## Sample 310

**Source**: `Reporter_v0\.data\doc-ingest_詳細實作設計.md` L27

```
/doc-ingest <SOURCE_DIR> [TARGET_DIR]
    │
    v 
┌──────────────────────────────────────────────────────────┐
│                    doc-ingest Skill                      │
│                                                          │
│  Step 1: 環境檢查     ───>  _preflight_report.md         │
│  Step 2: 來源掃描     ───>  _scan_report.md              │
│  Step 3: 分類規劃     ───>  _分類建議.md                 │
│  Step 4: 檔案複製     ───>  分類資料夾結構               │
│  Step 5: 文字萃取     ───>  *.txt + _extract_errors.log  │
│  Step 6: 建立索引     ───>  _index.json                  │
│  Step 7: 品質報告     ───>  _quality_report.md           │
│  Step 8: 部署設定     ───>  CLAUDE.md + settings.json    │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

