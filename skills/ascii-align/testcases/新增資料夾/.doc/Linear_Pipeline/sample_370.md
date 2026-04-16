## Sample 370

**Source**: `Reporter_v1\WORKSPACE\a01\06_personal-rag_v2.md` L49

```
├── PKB/
│   ├── CLAUDE.md
│   ├── scripts/
│   │   ├── api_server.py              # FastAPI RAG API
│   │   ├── phase1_vault_backup.py     # Phase 1：備份
│   │   ├── phase1m_mail_ingest.py     # Phase 1m：郵件匯入
│   │   ├── phase1m_zip_extract.py     # ZIP 解壓
│   │   ├── phase2_embed.py            # Phase 2：Gemini embedding
│   │   ├── phase2_qdrant.py           # Qdrant 查詢層
│   │   ├── phase2m_mail_embed.py      # 郵件 embedding
│   │   ├── phase3_preprocess.py       # Phase 3：圖片預處理
│   │   ├── phase3_batch_api.py        # 批次 Gemini API
│   │   ├── phase3_synthesize.py       # 知識合成
│   │   ├── reembed_ollama_qdrant.py   # bge-m3 re-embedding
│   │   ├── qdrant_check.py            # 驗證腳本
│   │   └── check_quota.py             # API 配額檢查
│   ├── raw_phase3/                    # Phase 3 合成知識
│   │   ├── customers/（24 batches）
│   │   ├── products/（12 files）
│   │   └── templates/（18 templates）
│   └── templates/                     # 文件模板（18 類）
├── reviews/                           # 7 份審核報告 + Q1 回顧
├── tests/                             # API + collection + embedding 測試
├── README.md
└── PKB_API_GUIDE.md
```

