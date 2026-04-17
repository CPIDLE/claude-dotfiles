## Sample 301

**Source**: `personal-rag_v2\README.md` L128

```
啟動
  → 載入 .env → 驗證 GOOGLE_API_KEY
  → 初始化 SQLite state DB
     ├── 首次：從 MANIFEST.csv 載入 status=copied 的檔案
     └── 續傳：重設 processing → pending，偵測重啟
  → 初始化 ChromaDB (pkb_docs + pkb_images)
  → 註冊 crash handler (atexit + signal)
  → 啟動 2hr 定期 email 通知

處理 images (4 workers 並行)
  → 讀取圖片 bytes
  → Gemini Vision 結構化描述 → {scene, objects, usage, client, caption}
  → Gemini Embedding (3072 dims)
  → 寫入 ChromaDB pkb_images + images_index.csv

處理 docs (4 workers 並行)
  → 萃取文字 + 圖片 (依檔案類型)
     ├── PPTX: python-pptx (slides → text + tables + images)
     ├── PDF:  pymupdf (pages → text + images)
     ├── DOCX: python-docx (paragraphs + images)
     ├── XLSX: openpyxl (sheets → rows)
     ├── XLS:  xlrd
     └── DOC/PPT: LibreOffice headless 轉新格式 → 再萃取
  → 內嵌圖片：存檔至 vault/embedded_images/ + 插入 [IMAGE_REF] 標記
  → 內容去重：MD5 hash 文字內容，跳過重複檔案
  → 長文字切割 (>2000 chars → 1000 chars + 200 overlap)
  → Gemini Embedding → ChromaDB pkb_docs

處理 videos (1 worker，循序)
  → 上傳至 Gemini Files API (ASCII temp path workaround)
  → Vision 時間戳分段描述 [MM:SS-MM:SS]
  → Gemini Embedding → ChromaDB pkb_docs

完成
  → 寄完成通知 email
  → 標記 run complete
```

---

