## Sample 612

**Source**: `TM_Program_Analysis_v0\docs\FLOW_ANALYSIS.md` L55

```
Start
  └─ SubFlow: ARM_parameter（初始化手臂參數）
       ├─ [g_use_RS485IO == false] --> 非 RS485 模式初始化
       │    ├─ [g_use_initial_point_setting_from_txt == false] --> 直接設 ENCODER/LED
       │    └─ [true] --> 從 TXT 檔讀取初始點位（read_file --> READ_TXT --> 迴圈解析）
       │
       └─ [g_use_RS485IO == true] --> RS485 模式初始化
            ├─ 檢查 RS485IO[0..7] 狀態 --> SET_ENCODER/LED
            ├─ 同樣支援 TXT 檔讀取
            └─ 設定 I/O Box x  6 + I/O EX x  4 --> SET_ARM_POSE

  --> Component: AMR_V001_CommunicationNoStop1（Modbus 通訊，持續監聽 AMR 指令）
  --> SET: SET_ARM_param --> port_name --> landmark_id --> BARCODE_ID
  --> Log: MISSION_START x  3
  --> SET: set_var_running

  --> [var_var_running_array[0] == 3] --> Gateway (主分派器)
       ├─ [0] --> NONE_MOVE（待機）
       ├─ [1] --> MOVE_TRAY_to_LEFT_multi_EQ（左側設備搬運）
       ├─ [2] --> MOVE_TRAY_to_RIGHT_multi_EQ（右側設備搬運）
       └─ [3] --> MOVE_INITIAL（回初始位）

  --> Log: MISSION_DONE x  3
  --> GOTO: AMR_V001_CommunicationNoStop1（回到通訊迴圈）
```

