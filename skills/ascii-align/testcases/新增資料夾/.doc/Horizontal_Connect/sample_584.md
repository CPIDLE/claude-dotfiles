## Sample 584

**Source**: `Reporter_v1\WORKSPACE\a06\TM_UR_程式架構完整版.md` L36

```
Start
  │
  ▼
ARM_parameter（初始化）
  ├─ RS485IO == false → 直接設 ENCODER/LED
  └─ RS485IO == true  → 檢查 RS485IO[0..7] → SET_ARM_POSE
  │
  ▼
AMR_V001_CommunicationNoStop1（Modbus 持續監聽 AMR 指令）
  │
  ▼
讀取 var_var_running_array[0]
  │
  ├─ [0] → 待機（NONE_MOVE）
  ├─ [1] → MOVE_TRAY_to_LEFT_multi_EQ  ─→ 左側設備搬運
  ├─ [2] → MOVE_TRAY_to_RIGHT_multi_EQ ─→ 右側設備搬運
  └─ [3] → MOVE_INITIAL（回初始位）
  │
  ▼
MISSION_DONE → GOTO 回通訊迴圈
```

---

