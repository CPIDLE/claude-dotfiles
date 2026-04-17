## Sample 324

**Source**: `Reporter_v0\.data\文件知識庫建置流程與Skill設計文件.md` L396

```
$TARGET_DIR/
├── .claude/settings.local.json    ← Claude Code 權限設定
├── CLAUDE.md                      ← 知識庫使用指引
├── _extract.py                    ← 主控萃取腳本
├── _extract_batch.py              ← 批次萃取引擎
├── _extract_one.py                ← 單檔萃取（備用）
├── _build_index.py                ← 索引建置腳本
├── _scan.py                       ← 來源掃描（Phase 2 新增）
├── _classify_rules.py             ← 分類引擎（Phase 2 新增）
├── _copy_files.py                 ← 檔案複製（Phase 2 新增）
├── _quality_report.py             ← 品質報告（Phase 2 新增）
├── _deploy.py                     ← 部署設定（Phase 2 新增）
├── _index.json                    ← 全文搜尋索引
├── _分類建議.md                   ← 分類結構說明
├── _extract_errors.log            ← 萃取錯誤記錄
├── 00_分類A/                      ← 分類資料夾
│   ├── 文件.pdf
│   └── 文件.pdf.txt
├── 01_分類B/
│   └── ...
└── ...
```

---

