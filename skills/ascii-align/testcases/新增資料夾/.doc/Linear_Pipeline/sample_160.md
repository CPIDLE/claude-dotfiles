## Sample 160

**Source**: `LineBot_Reporter_v1\docs\phase0-report.md` L56

```
LineBot_Reporter_v1/
├── docker-compose.yml          # 三服務架構
├── Caddyfile                   # 反向代理設定
├── .env.example                # 環境變數範本
├── .gitignore
├── reporter/                   # Reporter API 服務
│   ├── Dockerfile
│   ├── requirements.txt        # fastapi, uvicorn, pdfplumber, python-pptx, python-docx
│   ├── main.py                 # FastAPI：5 個 endpoint
│   ├── config.py               # 路徑/環境變數集中管理
│   ├── scripts/                # 13 個 Python 腳本（已參數化路徑）
│   │   ├── _build_index.py     # 索引建置
│   │   ├── _extract.py         # 文字萃取主控
│   │   ├── _extract_batch.py   # 批次萃取引擎
│   │   ├── _extract_one.py     # 單檔萃取
│   │   ├── _search_index.py    # 索引搜尋（同義詞展開+評分）
│   │   ├── _find_related.py    # 關聯文件搜尋
│   │   ├── _calc_throughput.py # 工程計算（瓶頸/流量/設備）
│   │   ├── _report_init.py     # 報告骨架產出
│   │   ├── _classify_rules.py  # 分類規則引擎
│   │   ├── _copy_files.py      # 檔案複製
│   │   ├── _scan.py            # 來源掃描
│   │   ├── _quality_report.py  # 品質報告
│   │   └── _setup.py           # 工具包安裝
│   └── templates/              # 10 個報告模板
├── workflows/                  # n8n workflow JSON
│   └── line-bot-gemini.json
├── images/                     # 靜態圖片（23 張）
├── n8n-data/                   # n8n 持久化資料
├── knowledge-base/             # 知識庫掛載點
└── docs/                       # 規劃文件
```

