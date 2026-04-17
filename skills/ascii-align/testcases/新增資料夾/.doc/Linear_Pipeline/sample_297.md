## Sample 297

**Source**: `personal-rag_v2\PKB_專案說明_v2_0327.md` L54

```
personal-rag_v2\PKB\
├── .env                    GEMINI_API_KEY / GOOGLE_API_KEY
├── CLAUDE.md               Claude Code 規則 + 草圖引擎邏輯
├── GYRO_context.md         產品規格 / 客戶 / 公式（≤150 行）
├── MANIFEST.csv            Phase 1 處理清單（SHA256 去重）
├── SKIPPED_ARCHIVES.csv    跳過的壓縮檔清單（302 個）
├── images_index.csv        圖片精確標籤
├── image_embed_state.db    Phase 3 圖片/影片 embedding 進度
├── vault\                  原始資料備份（唯讀，SHA256 去重）
│   ├── docs\               技術文件（PPTX/PDF/DOCX）
│   ├── images\             圖片
│   ├── videos\             影片
│   └── embedded_images\    文件內嵌圖片
├── templates\              報告模板 Markdown（14 類）
│   ├── 00_報告產生流程\    Marp 使用指南 + 範例
│   ├── 01_客戶提案\        含 8 種子模板
│   ├── 04_測試報告\  05_進度報告\  06_會議記錄\
│   ├── 08_市場分析\  09_設計文件\  10_操作手冊\
│   ├── 12_工作管制表\  13_圖紙\  14_不良分析報告\
│   ├── 16_內部研究\  17_介紹信\  18_AGV規劃\
├── raw_phase3\             Phase 3 歸納中間產出（僅供參考）
│   ├── customers\          客戶分析（24 batches）
│   ├── products\           產品線分析
│   └── templates\          模板原型（18 種）
├── scripts\                所有執行腳本（見下方）
├── sketch\                 草圖 SVG 輸出
├── workspace\              每次任務工作資料夾
├── logs\                   執行日誌
└── db\chroma\              ChromaDB legacy（唯讀，待清除）
```

---

