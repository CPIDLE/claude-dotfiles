## Sample 049

**Source**: `Chat_bot_v1\README.md` L66

```
Chat_bot_v1/
├── app.py                 # Thin proxy（Cloud Run, JWT 驗證 + 轉發）
├── backend.py             # RAG backend（本機, API key 驗證 + LINE webhook/push）
├── rag.py                 # RAG 模組（async embedding + Qdrant + Gemini LLM）
├── rate_limit.py           # Sliding window per-IP rate limiter
├── conv_logger.py         # （已停用）本地 JSONL 對話記錄
├── drive_logger.py        # （已停用）Google Drive 記錄同步
├── drive_sync.py          # （已停用）JSONL → Drive 增量同步
├── start-backend.sh       # Backend 啟動腳本（Windows/Linux）
├── stop-backend.sh        # Backend 停止腳本
├── Dockerfile             # Cloud Run thin proxy 映像
├── docker-compose.yml     # 本機開發用（Qdrant）
├── requirements.txt       # Python 依賴
├── pyproject.toml         # Ruff / pytest 設定
├── requirements-dev.txt   # 開發依賴（pytest, ruff）
├── tests/                 # Unit tests（33 cases）
├── architecture.md        # 架構與帳號歸屬文件
├── .env.example           # 環境變數範本
└── reviews/               # 程式碼審核報告
```

---

