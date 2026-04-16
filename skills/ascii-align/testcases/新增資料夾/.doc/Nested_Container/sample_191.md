## Sample 191

**Source**: `personal-rag_v1\flow.md` L5

```
.doc/ (7,388 文件)          .image/ (73,200 圖片)
    v  .txt 提取文本              v  .md 語意描述
    v                             v 
┌─────────────────────────────────────────┐
│  Gemini gemini-embedding-001 (3072 維)  │
└─────────────────────────────────────────┘
    v                             v 
┌───────────┐              ┌──────────┐
│ docs      │              │ images   │
│ collection│              │ collection   │
└───────────┘              └──────────┘
         ChromaDB (.chroma/)
            v 
┌──────────────────────────────────────────┐
│            FastAPI Backend               │
│  /docs/search  /images/search  /chat     │
│  /images/context  /kb-image/  /health    │
└──────────────────────────────────────────┘
              v 
┌──────────────────────────────────────────┐
│       Chat Frontend (chat.html)          │
│  KB mode .  file upload .  lightbox      │
│  markdown .  badges .  persistent history│
└──────────────────────────────────────────┘
```

