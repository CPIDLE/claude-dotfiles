## Sample 484

**Source**: `Reporter_v1\WORKSPACE\a04\00_REVIEW.md` L272

```
F:\機器人專案\06_AGV (來源目錄)
        │
        ▼ Phase 1: Vault Backup
phase1_vault_backup.py
  ├─ 掃描來源
  ├─ SHA256 去重
  └─ 複製至 PKB/vault/（唯讀）
        │
        ▼ → MANIFEST.csv (14,975 檔案)
        │
        ▼ Phase 2: Full Embedding (orchestrator)
phase2_embed.py
  ├─ phase2_extractors.py     (PPTX/PDF/DOCX/XLSX 萃取)
  ├─ phase2_gemini.py         (Vision 分析 + embedding)
  ├─ phase2_qdrant.py         (Qdrant 索引)
  ├─ phase2m_mail_embed.py    (郵件嵌入)
  ├─ reembed_ollama_qdrant.py (Ollama bge-m3 re-embed)
  └─ phase2_notify.py         (Email 進度通知)
        │
        ▼ → Qdrant (4 collections, 1M+ pts) + SQLite progress
        │
        ▼ Phase 3: API & Synthesis
phase3_batch_api.py
  ├─ API server（搜尋 / 深度查詢 / 郵件搜尋）
  ├─ 批次 pipeline
  └─ 日使用統計追蹤
phase3_synthesize.py
  └─ 報告生成
```

---

