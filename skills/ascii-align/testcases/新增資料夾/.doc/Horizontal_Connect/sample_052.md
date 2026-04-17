## Sample 052

**Source**: `Chat_bot_v1\使用指引.md` L121

```
Chat_bot_v1/
├── app.py                 # Thin proxy（Cloud Run, JWT 驗證 + 轉發）
├── backend.py             # RAG backend（本機, API key 驗證）
├── rag.py                 # RAG 模組（async embedding + Qdrant + Gemini LLM）
├── Dockerfile             # Cloud Run thin proxy 映像
├── docker-compose.yml     # 本機開發用（Qdrant）
├── start-backend.sh       # Backend + ngrok 啟動腳本
├── stop-backend.sh        # Backend + ngrok 停止腳本
├── requirements.txt       # Proxy 依賴
├── requirements-backend.txt # Backend 依賴
├── .env.example           # 環境變數範本
├── architecture.md        # 架構與帳號歸屬文件
├── conv_logger.py         # （已停用）本地 JSONL 對話記錄
├── drive_logger.py        # （已停用）Google Drive 記錄同步
├── drive_sync.py          # （已停用）JSONL → Drive 增量同步
└── reviews/               # 程式碼審核報告
```

---

