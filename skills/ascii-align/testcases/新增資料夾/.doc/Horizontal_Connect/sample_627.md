## Sample 627

**Source**: `TM_Program_Analysis_v0\docs\MR_PORT_PLACE_ANALYSIS.md` L178

```
MR_PORT_PLACE 入口
│
├─ Log: PLACE_TRAY (x 2)
├─ SET: var_grip_in = "MR"
├─ SET: var_MR_check_PSPL = false
│
├─ Gateway: MR_PORT_NUMBER (var_MR_port_number)
│   ├─ [1]  --> MR_1_front --> MR_1_pre_take
│   ├─ [2]  --> MR_2_front --> MR_2_pre_take
│   ├─ [3]  --> MR_3_front --> MR_3_pre_take
│   ├─ [4]  --> MR_4_front --> MR_4_pre_take
│   ├─ [5]  --> P22 --> MR_5_front --> MR_5_pre_take
│   ├─ [6]  --> P22 --> MR_6_front --> MR_6_pre_take
│   ├─ [7]  --> P10 --> MR_7_front --> MR_7_pre_take
│   ├─ [8]  --> P10 --> MR_8_front --> MR_8_pre_take
│   ├─ [9]  --> ...
│   └─ [12] --> ...
│
│  ===== 以下以 Port 1 為例 =====
│
├─ SET: reset_PSPL_counter (var_PSPL_check = 0)
│
├─ IF: var_MR_check_PSPL == true?
│   ├─ [YES] --> 放置前 PSPL 檢查
│   │   ├─ IF: Buffer_1_PS != true & Buffer_1_PL != true?
│   │   │   ├─ [YES] Port 空 --> 繼續
│   │   │   └─ [NO]  Port 有東西
│   │   │       ├─ [重試<3] --> PSPL_check++, Log, WaitFor 500ms --> 回到檢查
│   │   │       └─ [重試>=3] --> Log ERROR --> Modbus 1311 --> STOP
│   │   └─ SET: reset_PSPL_counter
│   │
│   └─ [NO] --> SET: pause_false --> 跳過檢查
│
├─ SubFlow: SENSOR_Grip_half（夾爪半開）
│
├─ Point: MR_1_take_up（Port 1 上方）
├─ SET: SET_grip（設定夾爪為 open 狀態）
├─ Point: MR_1_take（下降到放置位）
│
├─ SubFlow: SENSOR_Grip_open（夾爪全開，釋放 Tray）
│
├─ SET: reset_PSPL_counter (var_PSPL_check = 0)
│
├─ IF: var_MR_check_PSPL == true?
│   ├─ [YES] --> 放置後 PSPL 確認
│   │   ├─ IF: Buffer_1_PS == true & Buffer_1_PL == true?
│   │   │   ├─ [YES] Tray 在位 --> 繼續
│   │   │   └─ [NO]  Tray 不在位
│   │   │       ├─ [重試<3] --> PSPL_check++, Log, WaitFor 500ms --> 回到確認
│   │   │       └─ [重試>=3] --> Log ERROR --> Modbus 1311 --> STOP
│   │   └─ SET: reset_PSPL_counter
│   │
│   └─ [NO] --> 跳過確認
│
├─ Move: back_15mm（後退 15mm）
├─ Point: MR_1_ready_to_take（準備離開位）
├─ Point: MR_1_front（回到前方安全位）
│
├─ Log: PLACE_TRAY (x 2)
├─ SET: var_if_CHECK_ALL_SENSOR_WHEN_CAR_MOVING = true
├─ SET: var_grip_in = "MR"（重設夾爪來源）
│
└─ 結束（返回上層流程）
```

