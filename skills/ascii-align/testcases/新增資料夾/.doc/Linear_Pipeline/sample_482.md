## Sample 482

**Source**: `Reporter_v1\WORKSPACE\a04\00_REVIEW.md` L181

```
檔案輸入 (PDF/PPTX/DOCX/MP4)
    │
    ▼
rag_loaders.py
  ├─ PDFLoader (pdfplumber)
  ├─ PPTXLoader (python-pptx)
  ├─ DOCXLoader (python-docx)
  └─ VideoLoader (ffmpeg + Whisper)
    │
    ▼
rag_core.py (RAGEngine)
  ├─ Chunking (size=800, overlap=100)
  ├─ Embedding (sentence-transformers multilingual)
  ├─ ChromaDB (cosine similarity)
  └─ Gemini 2.0 Flash chat（串流）
    │
    ▼
rag.py (CLI)
```

---

