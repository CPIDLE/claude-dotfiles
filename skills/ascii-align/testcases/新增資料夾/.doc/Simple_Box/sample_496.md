## Sample 496

**Source**: `Reporter_v1\WORKSPACE\a04\01_Chat_bot_v1.md` L49

```
├── app.py                    # Thin proxy（Cloud Run, JWT 驗證 + 轉發）
├── backend.py                # RAG backend（本機, API key 驗證）
├── rag.py                    # RAG 模組（async embedding + Qdrant + Gemini LLM）
├── rate_limit.py             # Rate limiting
├── start-backend.sh          # Backend 啟動腳本
├── stop-backend.sh           # Backend 停止腳本
├── autostart-backend.vbs     # Windows 開機自啟
├── Dockerfile                # Cloud Run 映像
├── docker-compose.yml        # 本機 Qdrant
├── apps-script/              # Google Apps Script（每日統計報表 trigger）
│   ├── Code.gs
│   └── appsscript.json
├── tests/
│   ├── test_unit.py
│   └── test_thin_proxy.py
├── reviews/                  # 5 份審核報告
├── architecture.md           # 架構文件
├── 使用指引.md               # 使用者指南
└── conv_logger.py / drive_*.py  # （已停用）對話記錄功能
```

