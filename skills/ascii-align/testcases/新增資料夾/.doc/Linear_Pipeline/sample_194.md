## Sample 194

**Source**: `personal-rag_v1\README.md` L208

```
personal-rag_v1/
├── .doc/                # 文件知識庫 (7,388 份)
│   ├── _index.json      # 文件索引
│   ├── 00_公司簡介/     # ~ 65_客戶_其他 (27 分類)
│   └── ...
├── .image/              # 圖片知識庫 (~73,200 張)
│   ├── 00_其他/         # ~ 10_報告分析 (11 分類)
│   └── ...
├── api/                 # FastAPI 後端
│   ├── main.py          # App + 靜態檔 + kb-image endpoint
│   ├── schemas.py       # Pydantic models
│   ├── routers/
│   │   ├── chat.py      # Gemini function calling + RAG
│   │   ├── docs.py      # 文件搜尋 API
│   │   ├── images.py    # 圖片搜尋 API
│   │   └── context.py   # 圖片描述彙整 API
│   └── static/
│       └── chat.html    # Chat 前端 (單檔 HTML)
├── search/              # 語意搜尋模組
│   ├── config.py        # 共用設定
│   ├── embedder.py      # Gemini embedding 客戶端
│   ├── chunker.py       # 文字分塊
│   ├── db.py            # ChromaDB 封裝
│   ├── index_docs.py    # 文件索引 CLI
│   ├── index_images.py  # 圖片索引 CLI
│   ├── doc_search.py    # 文件搜尋 CLI
│   ├── img_search.py    # 圖片搜尋 CLI
│   ├── img_context.py   # Prompt 生成 CLI
│   └── monitor.py       # 進度監控 + email 通知
├── tests/               # 自動化測試 (103 tests)
├── .chroma/             # ChromaDB 存儲 (自動生成)
├── .env                 # API Key (不納入版控)
├── requirements-api.txt # Python 依賴
├── Dockerfile           # Docker 部署
├── flow.md              # 系統流程文件
├── test_report.md       # 測試報告
└── README.md
```

---

