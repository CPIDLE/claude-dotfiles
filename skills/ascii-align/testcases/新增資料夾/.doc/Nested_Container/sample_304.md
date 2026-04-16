## Sample 304

**Source**: `personal-rag_v2\reviews\RETROSPECTIVE_2026-04-01.md` L177

```
資料源                    Phase 1              Phase 2                    Phase 3/4           API
F:\機器人專案\06_AGV    ┌───────────┐     ┌──────────────────┐      ┌──────────────┐    ┌──────────┐
 14,975 files ────────>│ Vault      │────>│ Extractors       │─────>│ Synthesis    │    │ FastAPI  │
                       │ SHA256 dedup│    │ PPTX/PDF/DOCX/   │      │ GYRO_context │    │ :8000    │
mail_index.db ─────────│ MANIFEST   │     │ XLSX/DOC/PPT/IMG/│      │ Templates    │    │          │
 31,990 emails         └────────────┘     │ Video            │      └──────────────┘    │ /search  │
                                          ├──────────────────┤                          │ /deep-   │
                                          │ Gemini 3072d     │┐                    │  query        │
                                          │ Ollama bge-m3    ││                    │ /stats        │
                                          │ 1024d            ││                       └────┬───────┘
                                          └──────────────────┘│                         │
                                                                v                            v
                                          ┌──────────────────────────────────────────────────────┐
                                          │              Qdrant Docker (qdrant-pkb)              │
                                          │              localhost:6333 | D:/PKB_db/             │
                                          ├──────────────────────────────────────────────────────┤
                                          │ pkb_docs          520,771 pts  3072d  Gemini         │
                                          │ pkb_images        289,932 pts  3072d  Gemini         │
                                          │ pkb_mail          162,446 pts  3072d  Gemini         │
                                          │ pkb_docs_ollama   520,771 pts  1024d  bge-m3         │
                                          │ pkb_images_ollama 289,932 pts  1024d  bge-m3         │
                                          │ pkb_mail_ollama   162,446 pts  1024d  bge-m3         │
                                          │                                                      │
                                          │ Total: ~1.95M vectors | RAM: ~380 MB | on_disk=True  │
                                          └──────────────────────────────────────────────────────┘
```

