## Sample 449

**Source**: `Reporter_v1\WORKSPACE\a02\AMHS_Edge_Agent_架構.md` L27

```
╔═══════════════════════════════════════════════════════════╗
║                 廠內封閉網路（Air-Gapped）                  ║
║                                                           ║
║  ┌─ Server GPU / DGX Spark（廠內機房）─────────────────┐  ║
║  │                                                     │  ║
║  │  n8n（觸發 + 預分類，指定 Skill + 參數）             │  ║
║  │    │                                                │  ║
║  │    ▼                                                │  ║
║  │  LLM Agent                                          │  ║
║  │    Phase 1-2: 直接 Ollama REST API                  │  ║
║  │    Phase 3:   採用 LangGraph 管理多步 workflow        │  ║
║  │    │                                                │  ║
║  │    ▼                                                │  ║
║  │  5 Skill（封裝 MCP 呼叫，回傳精簡結果）              │  ║
║  │    dispatch ─→ mcp-mcs + mcp-tsc      (Fast 8B)    │  ║
║  │    diagnose ─→ mcp-eap + mcp-pkb      (Full 72B)   │  ║
║  │    schedule ─→ mcp-mcs + mcp-tsc      (Full 72B)   │  ║
║  │    inventory → mcp-erack + mcp-mcs    (Fast 8B)    │  ║
║  │    traffic ──→ mcp-tsc                (Fast 8B)    │  ║
║  │    │                                                │  ║
║  │    ▼                                                │  ║
║  │  MCP Servers + rule_validate（紅線檢查，不用 LLM）   │  ║
║  │  mcp-mcs · mcp-tsc · mcp-eap · mcp-pkb · mcp-erack │  ║
║  │    │                                                │  ║
║  │    ▼                                                │  ║
║  │  ROS 2 Bridge ←→ AMR        Grafana（監控，零 LLM）  │  ║
║  │                                                     │  ║
║  │  Ollama（72B + 8B）· PKB Qdrant · MCS Lite · TSC    │  ║
║  └─────────────────────┬───────────────────────────────┘  ║
║                        │ 廠內 LAN / Wi-Fi                  ║
║  ┌─────────────────────▼───────────────────────────────┐  ║
║  │  AMR IPC ×N                                         │  ║
║  │  [平時] ROS node（純執行器）                          │  ║
║  │  [斷線] Ollama Tiny 1.7B → L1 收尾 + 停靠           │  ║
║  └─────────────────────────────────────────────────────┘  ║
╚═══════════════════════════════════════════════════════════╝
```

---

