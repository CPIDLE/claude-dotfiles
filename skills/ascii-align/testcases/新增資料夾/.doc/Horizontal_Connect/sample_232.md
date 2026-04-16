## Sample 232

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\HT_9046LS_TMMARK_NORMAL_ANALYSIS.md` L103

```
Vision: RIGHT_HT_9046LS_right_TMMARK_FAR
  ├─ [成功]
  │    SET: var_coordrobot = Robot[0].CoordRobot          <-- 記錄當前機器人座標
  │         var_Log_vision_base = Base["vision_...FAR"]   <-- 記錄視覺基座值
  │    Log: 記錄座標
  │
  │    ── 驗證 1：Rz 角度檢查 ──
  │    IF: abs(vision_base[5]) 在 80°~100° 之間?
  │      ├─ [YES] --> 驗證 2
  │      └─ [NO]  角度異常
  │           ├─ [重試<g_vision_retry] --> vision_count++ --> 回到 Vision FAR
  │           └─ [重試>=g_vision_retry]
  │                --> Log ERROR --> SET: error_code=1227 --> STOP
  │
  │    ── 驗證 2：Z 軸距離檢查 ──
  │    IF: |coordrobot[2] - vision_base[2]| <= 350?
  │      ├─ [YES] --> 驗證 3
  │      └─ [NO]  Z 軸偏差過大
  │           ├─ [重試<=g_tag_distance_retry] --> tag_distance_count++ --> 回到 Vision FAR
  │           └─ [超過重試] --> Log ERROR --> SET: error_code=1224/1225 --> STOP
  │
  │    ── 驗證 3：Ry 角度偏差檢查 ──
  │    IF: |g_check_EQ_goal_tolerance[4] - vision_base[4]| <= g_check_EQ_far_tolerance[4]?
  │      ├─ [YES] --> 通過! --> 移動到 P70 --> Phase 4
  │      └─ [NO]  Ry 偏差過大
  │           ├─ [重試<g_re_try] --> count++ --> 回到 Vision FAR
  │           └─ [超過重試] --> Log ERROR --> SET: error_code=1223 --> STOP
  │
  └─ [失敗]
       ├─ [重試<g_vision_retry] --> vision_count++ --> Log ERROR --> 回到 Vision FAR
       └─ [超過重試]
            --> Log ERROR --> SET: error_code=1223 --> STOP
```

