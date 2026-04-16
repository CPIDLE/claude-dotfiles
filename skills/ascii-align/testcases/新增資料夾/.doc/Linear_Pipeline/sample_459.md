## Sample 459

**Source**: `Reporter_v1\WORKSPACE\a02\GYRO_AI_AMHS_技術白皮書.marp.md` L558

```
Claude Code 開發 Skill + MCP Server + Bridge
  │
  v 
Gemini API 雲端試驗 ─── 驗證 Skill 邏輯、MCP --> API 連接、查詢準確率
  │
  v 
Ollama 本地測試 ─────── 驗證本地 model 推理品質、延遲、SQLite-->InfluxDB 同步
  │
  v 
DGX Spark 產線部署 ──── Phase 1 --> 2 --> 3 逐步開放
  │                     Phase 1–2：直接 API 呼叫
  │                     Phase 3：採用 LangGraph 管理多步 workflow / state
  v 
Production（24/7 離線運行）
```

