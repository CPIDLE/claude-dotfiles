## Sample 235

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\HT_9046LS_TMMARK_NORMAL_ANALYSIS.md` L209

```
IF: DIO 數位感測器有信號?
  ├─ [YES] 有 Tray
  │    IF: var_LASER_MEASURE <= g_highest_point & var_laser_volt >= 1.5?
  │      ├─ [YES] 距離正常 → 重試 (count++ → 回到 Vision FAR/NEAR)
  │      └─ [NO]  → 二次確認 (double_check)
  │
  └─ [NO] 無 DIO 信號 → Log ERROR → 回到 Vision FAR/NEAR
```

---

