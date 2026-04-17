## Sample 342

**Source**: `Reporter_v0\request_02\report.md` L570

```
.doc/
├── .claude/
│   ├── settings.local.json
│   └── skills/
│       ├── doc-ingest.md
│       └── doc-report.md
│
├── # 既有腳本 (Stage 2-3)
├── _extract.py / _extract_batch.py / _extract_one.py
├── _build_index.py
│
├── # Phase 2: doc-ingest
├── _scan.py / _classify_rules.py / _copy_files.py
├── _quality_report.py / _deploy.py
│
├── # Phase 2: doc-report
├── _search_index.py / _find_related.py
├── _calc_throughput.py / _report_init.py
│
├── _index.json          ← 搜尋索引 (7,338 筆)
├── _分類建議.md          ← 分類結構說明
├── CLAUDE.md            ← 知識庫使用指引
│
├── 00_公司簡介/  ... 50_安全認證/    ← 產品技術 (1,229 files)
├── 60_客戶_封測/ ... 65_客戶_其他/   ← 客戶專案 (6,673 files)
├── 70_業務報價/  ... 95_工程開發/    ← 業務工程 (3,394 files)
└── _OLD/ _其他/ _專利/ _情報/ _影片/ ← 雜項 (1,729 files)
```

---

