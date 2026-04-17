## Sample 307

**Source**: `personal-rag_v2\reviews\RETROSPECTIVE_2026-04-01_slides_v2.md` L84

```
瀏覽器 ──> FastAPI (port 8000)
              │
              ├── /chat ─────────> Gemini Function Calling
              │                    ├── doc_search()
              │                    ├── img_search()
              │                    ├── img_context()
              │                    └── generate_image()
              │
              ├── /docs/search ──> ChromaDB pkb_docs (7,388 docs)
              ├── /images/search > ChromaDB pkb_images (73,200 images)
              │
              └── chat.html ────> 單頁 Chat UI（拖拉上傳、Lightbox）
                                  Gemini embedding-001 (3072d)
```

---

