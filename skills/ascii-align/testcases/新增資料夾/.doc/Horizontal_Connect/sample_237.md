## Sample 237

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\HT_9046LS_TMMARK_NORMAL_ANALYSIS.md` L233

```
IF: g_double_check_if_tray_on_EQ_port == true?
  ├─ [YES]
  │    IF: var_LASER_MEASURE >= g_lowest_point?
  │      ├─ [YES] 距離夠遠，確認沒有 Tray
  │      │    SET: var_temp_LASER_MEASURE = var_LASER_MEASURE  ← 暫存
  │      │    Move: in_gyro_move_to_tray                       ← 靠近一點再看
  │      │    WaitFor: 1000ms
  │      │    SET: 重新測量 LASER_MEASURE
  │      │    SET: 重新計算 put_down_distance
  │      │    → 第二輪感測器檢查
  │      │
  │      └─ [NO] 距離太近，可能有 Tray → Gateway 分派到各 Port front
  │           → GOTO 回到主流程
  │
  └─ [NO] 不做二次確認 → 直接到 Port 分派
```

---

