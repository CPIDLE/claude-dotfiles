## Sample 316

**Source**: `Reporter_v0\.data\README.md` L74

```
scripts/                    # 工具腳本 (14 支)
├── _setup.py               <-- 安裝腳本（從這裡開始）
├── _extract.py              <-- 文字萃取主控
├── _extract_batch.py        <-- 批次萃取引擎
├── _extract_one.py          <-- 單檔萃取
├── _build_index.py          <-- 索引建置
├── _scan.py                 <-- 來源掃描
├── _classify_rules.py       <-- 三層分類引擎
├── _copy_files.py           <-- 檔案複製
├── _quality_report.py       <-- 品質報告
├── _deploy.py               <-- 部署設定
├── _search_index.py         <-- 索引搜尋（同義詞展開+評分）
├── _find_related.py         <-- 關聯文件搜尋
├── _calc_throughput.py      <-- 工程計算（瓶頸/流量/設備）
└── _report_init.py          <-- 報告骨架產出

skills/                     # Claude Code Skill (2 支)
├── doc-ingest.md            <-- 知識庫建置 Skill
└── doc-report.md            <-- 需求報告 Skill

docs/                       # 設計文件 (4 份)
├── 文件知識庫建置流程與Skill設計文件.md  <-- 主設計文件 V1.3
├── doc-ingest_詳細實作設計.md
├── doc-report_詳細實作設計.md
└── _分類建議.md             <-- 分類結構範本
```

