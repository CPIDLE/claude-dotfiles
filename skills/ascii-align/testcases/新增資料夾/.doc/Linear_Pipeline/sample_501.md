## Sample 501

**Source**: `Reporter_v1\WORKSPACE\a04\04_personal-rag.md` L29

```
檔案輸入 (PDF/PPTX/DOCX/MP4)
    │
    v 
rag_loaders.py
├─ PDFLoader (pdfplumber)
├─ PPTXLoader (python-pptx)
├─ DOCXLoader (python-docx)
└─ VideoLoader (ffmpeg + Whisper)
    │
    v 
rag_core.py (RAGEngine)
├─ Chunking (chunk_size=800, overlap=100)
├─ Embedding (sentence-transformers)
├─ ChromaDB (向量存儲)
└─ Gemini Chat (生成式回答)
    │
    v 
rag.py (CLI)
```

