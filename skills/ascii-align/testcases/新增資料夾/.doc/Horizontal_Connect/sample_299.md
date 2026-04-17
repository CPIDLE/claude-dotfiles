## Sample 299

**Source**: `personal-rag_v2\README.md` L43

```
personal-rag_v2/
├── README.md                          本文件
├── PKB_專案說明_v2_0316.md            原始規格書
├── test_gemini_embed.py               API 驗證腳本
│
└── PKB/
    ├── .env                           API keys + SMTP 設定
    ├── .env.example                   環境變數範本
    ├── MANIFEST.csv                   Phase 1 產出（14,975 筆檔案索引）
    ├── images_index.csv               Phase 2 產出（圖片標籤 CSV）
    ├── embedded_images_pending.csv    文件內嵌圖片待處理清單
    │
    ├── vault/                         原始資料備份（唯讀）
    │   ├── docs/                      PPTX, PDF, DOCX, XLSX, DOC, PPT
    │   ├── images/                    JPG, PNG
    │   ├── videos/                    MP4
    │   └── embedded_images/           文件內嵌圖片（Phase 2 萃取）
    │
    ├── db/
    │   ├── chroma/                    ChromaDB 持久化資料（legacy，唯讀）
    │   └── phase2_state.db            Phase 2 進度追蹤 (SQLite)
    │   # Qdrant 儲存於 D:/PKB_db/qdrant_server/（Docker mount，NTFS）
    │
    ├── scripts/
    │   ├── phase1_vault_backup.py     Phase 1 主程式
    │   ├── phase2_embed.py            Phase 2 主程式（orchestrator）
    │   ├── phase2_extractors.py       檔案萃取器
    │   ├── phase2_gemini.py           Gemini API 封裝
    │   ├── phase2_chroma.py           ChromaDB 操作（legacy）
    │   ├── phase2_qdrant.py           Qdrant 查詢層（主力）
    │   ├── phase2_notify.py           Email 通知
    │   ├── phase2_state.py            進度追蹤 (SQLite)
    │   ├── reembed_ollama.py          Ollama bge-m3 re-embedding
    │   ├── migrate_chroma_to_qdrant.py  ChromaDB → Qdrant 遷移
    │   └── qdrant_check.py            Qdrant 資料驗證
    │
    ├── templates/                     報告模板（Phase 3）
    ├── sketch/                        草圖 SVG 輸出
    └── workspace/                     任務工作區
```

---

