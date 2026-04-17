## Sample 520

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\GYRO\00_GYRO_AI_AMHS_Support_Agent_整合報告.md` L491

```
DGX Spark（產線機房，Air-Gapped）
├─ Ollama LLM Runtime
│   ├─ Full 72B (Q4) ~42GB  → diagnose / schedule
│   └─ Fast 8B  (Q4) ~5GB   → dispatch / inventory / traffic
 │
├─ PKB v3 (本軸線交付)
│   ├─ Qdrant Docker (on_disk) ~4GB   ← 6 collections / 195 萬筆
│   ├─ Ollama bge-m3 ~2GB             ← 1024 維 embedding
│   └─ PKB API Server (FastAPI)       ← /kb/search /pkb/diagnose/search /pkb/sop/lookup
 │
├─ 監控與資料
│   ├─ InfluxDB ~2-3GB
│   └─ Grafana
 │
└─ AMHS 控制面
    ├─ MCS-Lite / TSC / EAP
    └─ MCP Servers
```

---

