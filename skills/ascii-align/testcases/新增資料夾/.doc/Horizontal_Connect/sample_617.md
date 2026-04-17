## Sample 617

**Source**: `TM_Program_Analysis_v0\docs\HT_9046LS_TMMARK_NORMAL_ANALYSIS.md` L170

```
IF: g_use_RS485IO == false?  → Gateway（非 RS485）
IF: g_use_RS485IO == true?   → Gateway（RS485）

Gateway: var_to_port_number
  ├─ [1] EQ_PORT1 → 檢查 EQ_TYPE → HT_9046LS_001_front → check_tray_distance
  ├─ [2] EQ_PORT2 → 檢查 EQ_TYPE → HT_9046LS_002_front → check_tray_distance
  └─ [3] EQ_PORT3 → 檢查 EQ_TYPE → HT_9046LS_003_front → check_tray_distance
```

---

