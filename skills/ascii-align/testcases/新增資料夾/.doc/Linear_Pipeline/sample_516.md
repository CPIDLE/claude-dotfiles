## Sample 516

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\GYRO\00_GYRO_AI_AMHS_Support_Agent_整合報告.md` L213

```
F:\機器人專案\06_AGV (來源目錄)
        v 
┌──────────────────────────────────────────────┐
│ Phase 1: Vault Backup                        │
│   phase1_vault_backup.py                     │
│   ├─ 掃描來源                                │
│   ├─ SHA256 去重                             │
│   └─ 複製至 PKB/vault/（唯讀）               │
└──────────────────────────────────────────────┘
        v  MANIFEST.csv (14,975 檔案)
┌──────────────────────────────────────────────┐
│ Phase 2: Full Embedding                      │
│   phase2_embed.py (orchestrator)             │
│   ├─ phase2_extractors.py (多格式萃取)       │
│   ├─ phase2_gemini.py (Vision + embedding)   │
│   ├─ phase2_qdrant.py (Qdrant 索引)          │
│   ├─ phase2m_mail_embed.py (郵件嵌入)        │
│   ├─ reembed_ollama_qdrant.py (bge-m3)       │
│   └─ phase2_notify.py (Email 進度)           │
└──────────────────────────────────────────────┘
        v  Qdrant (4 collections, 1M+ pts)
┌──────────────────────────────────────────────┐
│ Phase 3: API & Synthesis                     │
│   ├─ phase3_batch_api.py (API server)        │
│   ├─ phase3_synthesize.py (報告生成)         │
│   └─ 日使用統計追蹤                          │
└──────────────────────────────────────────────┘
```

