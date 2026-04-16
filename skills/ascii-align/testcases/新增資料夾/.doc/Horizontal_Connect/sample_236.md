## Sample 236

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\HT_9046LS_TMMARK_NORMAL_ANALYSIS.md` L221

```
IF: var_RS485IO[7] == 0?  <-- RS485 第 8 位 = Tray 感測器
  ├─ [0] 無 Tray
  │    IF: LASER_MEASURE <= g_highest_point & laser_volt >= 1.5?
  │      ├─ [YES] 雷射也確認無 Tray --> 重試
  │      └─ [NO]  --> 二次確認 (double_check)
  │
  └─ [非0] 有 Tray --> Log ERROR --> 回到 Vision FAR/NEAR
```

