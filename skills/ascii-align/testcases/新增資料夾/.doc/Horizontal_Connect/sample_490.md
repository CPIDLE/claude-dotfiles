## Sample 490

**Source**: `Reporter_v1\WORKSPACE\a04\00_Support_Agent_簡報版.md` L29

```
   ┌──────────── Agent 的三個資料來源 ───────────────┐
   │                                                 │
   │  MCP Servers ───> 現在（即時狀態 + 指令）       │
   │  InfluxDB    ───> 過去（歷史趨勢）              │
   │  Qdrant/PKB  ───> 知識（維修經驗 + SOP）  *     │
   │                                                 │
   └─────────────────────────────────────────────────┘
                          v 
                    5 個 Skill
   ┌───────────────────────────────────────────────┐
   │  Skill        Model       使用 PKB？          │
   │  ──────────   ─────────   ──────────          │
   │  dispatch     Fast 8B     x                   │
   │  diagnose     Full 72B    ✅ 歷史案例 + SOP   │
   │  schedule     Full 72B    x                   │
   │  inventory    Fast 8B     x                   │
   │  traffic      Fast 8B     x                   │
   └───────────────────────────────────────────────┘
```

