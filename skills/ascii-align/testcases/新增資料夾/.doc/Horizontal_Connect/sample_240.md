## Sample 240

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\HT_9046LS_TMMARK_NORMAL_ANALYSIS.md` L345

```
HT_9046LS_TMMARK_NORMAL 入口
│
├─ 初始化 (Log, SET grip_in="EQ", 重置計數器)
│
├─ Camera Once 優化?
│   ├─ [已拍過] --> 跳過視覺 --> Phase 5
│   └─ [未拍過] v 
│
├─ ═══ Vision FAR ═══════════════════════
│   │  Job: RIGHT_HT_9046LS_right_TMMARK_FAR
│   │  辨識: Landmark (TM Mark)
│   │
│   ├─ [成功] --> 記錄座標
│   │   ├─ 驗證 1: Rz in [80°, 100°]?
│   │   │   └─ [失敗] --> 重試 <= g_vision_retry --> STOP(1227)
│   │   ├─ 驗證 2: |D Z| <= 350mm?
│   │   │   └─ [失敗] --> 重試 <= g_tag_distance_retry --> STOP(1224)
│   │   └─ 驗證 3: |D Ry| <= far_tolerance?
│   │       └─ [失敗] --> 重試 <= g_re_try --> STOP(1223)
│   │
│   └─ [失敗] --> 重試 <= g_vision_retry --> STOP(1223)
│
├─ 移動到 P70（近距位）
│
├─ ═══ Vision NEAR ══════════════════════
│   │  Job: RIGHT_HT_9046LS_right_TMMARK_NEAR
│   │  辨識: Landmark (TM Mark)
│   │
│   ├─ [成功] --> 記錄座標 + 讀取 AMR 感測器
│   │   └─ 驗證: |D Ry| <= near_tolerance?
│   │       └─ [失敗] --> 重試 <= g_re_try --> STOP(1226)
│   │
│   └─ [失敗] --> 重試 <= g_vision_retry --> STOP(1225)
│
├─ ═══ Port 分派 ════════════════════════
│   Gateway: var_to_port_number
│   ├─ [1] --> HT_9046LS_001_front --> check_tray_distance
│   ├─ [2] --> HT_9046LS_002_front --> check_tray_distance
│   └─ [3] --> HT_9046LS_003_front --> check_tray_distance
│
├─ ═══ 雷射測距 ═════════════════════════
│   WaitFor: 1000ms（穩定）
│   LASER = AI[0] x  57.5 + 30 (mm)
│   put_down_distance = LASER - gripper_depth
│
├─ ═══ Tray 存在判斷 ════════════════════
│   │
│   ├─ 第一層: DIO / RS485IO[7] 感測器
│   ├─ 第二層: LASER <= highest_point & volt >= 1.5V?
│   └─ 第三層: double_check --> 靠近再測一次
│
├─ ═══ 最終輸出 ═════════════════════════
│   var_nothing_on_port_can_place = true/false
│   │
│   └─ g_place_again?
│       ├─ [true]  --> 允許重試放置
│       └─ [false] --> STOP(1014)
│
└─ 收尾 (Log, SET grip_in="", 返回)
```

