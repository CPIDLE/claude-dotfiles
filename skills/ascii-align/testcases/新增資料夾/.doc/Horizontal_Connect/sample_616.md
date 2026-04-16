## Sample 616

**Source**: `TM_Program_Analysis_v0\docs\HT_9046LS_TMMARK_NORMAL_ANALYSIS.md` L140

```
移動到 P70（近距拍照位）
SET: 重置所有計數器

Vision: RIGHT_HT_9046LS_right_TMMARK_NEAR
  ├─ [成功]
  │    SET: var_temporary_fl = modbus_read("mtcp_AMR","preset_en_fl")  <-- 讀取 AMR 感測器
  │         var_temporary_bl = modbus_read("mtcp_AMR","preset_en_bl")
  │         var_temporary_fr = modbus_read("mtcp_AMR","preset_en_fr")
  │    SET: var_coordrobot = Robot[0].CoordRobot
  │         var_Log_vision_base = Base["vision_...NEAR"]
  │    Log: 記錄座標
  │
  │    ── 驗證：Ry 角度偏差檢查 ──
  │    IF: |g_check_EQ_goal_tolerance[4] - vision_NEAR_base[4]| <= g_check_EQ_near_tolerance[4]?
  │      ├─ [YES] --> 通過! --> Phase 5（Camera Once 分派 或 Port 分派）
  │      └─ [NO]  Ry 偏差過大
  │           ├─ [重試<g_re_try] --> count++ --> 回到 Vision NEAR
  │           └─ [超過重試] --> Log ERROR --> SET: error_code=1226 --> STOP
  │
  └─ [失敗]
       ├─ [重試<g_vision_retry] --> vision_count++ --> 回到 Vision NEAR
       └─ [超過重試]
            --> Log ERROR --> SET: error_code=1225 --> STOP
```

