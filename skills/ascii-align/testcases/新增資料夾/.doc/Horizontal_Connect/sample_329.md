## Sample 329

**Source**: `Reporter_v0\.data\文件知識庫建置流程與Skill設計文件.md` L726

```
.doc/
├── .claude/
│   ├── settings.local.json         <-- Claude Code 權限設定
│   └── skills/
│       ├── doc-ingest.md           <-- Skill A prompt
│       └── doc-report.md           <-- Skill B prompt
│
├── # 既有腳本 (Stage 2-3)
├── _extract.py                     <-- 文字萃取主控
├── _extract_batch.py               <-- 批次萃取引擎
├── _extract_one.py                 <-- 單檔萃取
├── _build_index.py                 <-- 索引建置
│
├── # Phase 2 新增: doc-ingest
├── _scan.py                        <-- 來源掃描
├── _classify_rules.py              <-- 三層分類引擎
├── _copy_files.py                  <-- 檔案複製
├── _quality_report.py              <-- 品質報告
├── _deploy.py                      <-- 部署設定
│
├── # Phase 2 新增: doc-report
├── _search_index.py                <-- 索引搜尋（同義詞+評分）
├── _find_related.py                <-- 關聯文件搜尋
├── _calc_throughput.py             <-- 工程計算
├── _report_init.py                 <-- 報告骨架產出
│
├── # 資料與設定
├── _index.json                     <-- 搜尋索引 (7,338 筆)
├── _extract_errors.log             <-- 錯誤記錄
├── _分類建議.md                    <-- 分類結構說明
├── CLAUDE.md                       <-- 知識庫使用指引
│
├── # 25 個分類資料夾
├── 00_公司簡介/                    <-- 36 files
├── 01_產品型錄/                    <-- 62 files
├── 02_軟體系統/                    <-- 73 files
├── 10_車型規格/                    <-- 118 files
├── 20_搬運方案/                    <-- 63 files
├── 30_周邊設備/                    <-- 430 files
├── 40_系統整合/                    <-- 107 files
├── 50_安全認證/                    <-- 340 files
├── 60_客戶_封測/                   <-- 3,935 files (最大)
├── 61_客戶_晶圓代工/              <-- 748 files
├── 62_客戶_記憶體/                 <-- 526 files
├── 63_客戶_面板光電/              <-- 55 files
├── 64_客戶_系統整合/              <-- 657 files
├── 65_客戶_其他/                   <-- 752 files
├── 70_業務報價/                    <-- 277 files
├── 75_進度報告/                    <-- 33 files
├── 80_設計規範/                    <-- 10 files
├── 85_研究資料/                    <-- 324 files
├── 90_開發計畫/                    <-- 1,578 files
├── 91_場地需求/                    <-- 52 files
├── 95_工程開發/                    <-- 1,120 files
├── _OLD/                           <-- 49 files
├── _其他/                          <-- 工具腳本暫存區
├── _專利/                          <-- 4 files
├── _情報/                          <-- 18 files
└── _影片/                          <-- 51 files
```

