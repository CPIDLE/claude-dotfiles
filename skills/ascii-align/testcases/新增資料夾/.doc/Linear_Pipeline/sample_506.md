## Sample 506

**Source**: `Reporter_v1\WORKSPACE\a04\06_personal-rag_v2.md` L64

```
personal-rag_v2/
├── README.md
├── PKB_專案說明_v2_0316.md
├── PKB_API_GUIDE.md
├── CHANGELOG.md
├── test_gemini_embed.py
└── PKB/
    ├── MANIFEST.csv                   # Phase 1 輸出（14,975 檔案）
    ├── images_index.csv               # Phase 2 輸出（圖片標籤）
    ├── vault/                         # 原始資料備份（唯讀）
    │   ├── docs/                      # PPTX, PDF, DOCX, XLSX
    │   ├── images/                    # JPG, PNG
    │   ├── videos/                    # MP4
    │   └── embedded_images/           # 文件內嵌圖片
    ├── db/
    │   ├── chroma/                    # ChromaDB legacy (唯讀)
    │   └── phase2_state.db            # SQLite 進度追蹤
    ├── scripts/
    │   ├── phase1_vault_backup.py     # 掃描+去重+備份
    │   ├── phase2_embed.py            # orchestrator
    │   ├── phase2_extractors.py       # 檔案萃取
    │   ├── phase2_gemini.py           # Gemini API 封裝
    │   ├── phase2_qdrant.py           # Qdrant 操作
    │   ├── phase2m_mail_embed.py      # 郵件嵌入
    │   ├── reembed_ollama_qdrant.py   # Re-embedding
    │   ├── phase3_batch_api.py        # API 服務
    │   └── qdrant_check.py            # 資料驗證
    └── templates/                     # 報告模板 (Phase 3)
```

---

