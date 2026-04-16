## Sample 238

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\HT_9046LS_TMMARK_NORMAL_ANALYSIS.md` L253

```
移動到 HT_9046LS_00X_front（Port 前方）

IF: var_LASER_MEASURE >= g_lowest_point?
  ├─ [YES] var_nothing_on_port_can_place = true   <-- Port 空的，可以放
  └─ [NO]  var_nothing_on_port_can_place = false   <-- Port 有東西，不能放

Log: LASER_DISTANCE
```

