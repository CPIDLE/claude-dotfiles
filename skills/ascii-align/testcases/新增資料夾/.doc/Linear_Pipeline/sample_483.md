## Sample 483

**Source**: `Reporter_v1\WORKSPACE\a04\00_REVIEW.md` L223

```
Web 前端（單檔 HTML + vanilla JS）
  ├─ Lightbox 圖片檢視
  ├─ 拖曳/Ctrl+V 上傳
  └─ localStorage 對話持久化（3 天 / 10MB）
    │
    v 
FastAPI 後端 (api/main.py)
  ├─ /chat (Gemini Function Calling 入口)
  │   ├─ search_documents
  │   ├─ search_images
  │   ├─ generate_image_context
  │   └─ generate_image (use_kb param)
  ├─ /docs/search   (語意搜尋)
  ├─ /images/search (語意搜尋)
  ├─ /kb-image/{path} (靜態服務)
  └─ /health
    │
    v 
ChromaDB（本地持久化）
  + gemini-embedding-001 (3072 維)
  + gemini-2.0-flash (Chat)
  + gemini-2.5-flash-image (生成)
```

