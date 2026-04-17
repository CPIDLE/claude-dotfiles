## Sample 613

**Source**: `TM_Program_Analysis_v0\docs\FLOW_ANALYSIS.md` L382

```
                    ┌─────────────────────┐
                    │   AMR (Modbus 通訊)  │
                    └──────────┬──────────┘
                               │ var_var_running_array
                    ┌──────────▼──────────┐
                    │   ARM_parameter     │ ← 初始化（RS485/TXT 點位）
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │      Gateway        │ ← 主分派器
                    │  [0]=方向 [3]=目標   │
                    └─┬────┬────┬────┬───┘
                      │    │    │    │
              ┌───────┘    │    │    └────────┐
              ▼            ▼    ▼             ▼
         MOVE_LEFT    MOVE_RIGHT  INITIAL   NONE_MOVE
              │            │        │
    ┌─────┬──┴──┬────┐    ...   ReturnHome
    ▼     ▼     ▼    ▼
  ERACK  EQ   ICOS  STK   ← [3] 目標類型
    │     │          │
  PORT_1~8          TAKE/PLACE ← [4] Port 編號
    │
  ┌─┴─────────────────┐
  │  HT_9046LS_TAKE   │ ← 設備操作
  │  HT_9046LS_PLACE  │
  │  MR_PORT_TAKE     │
  │  MR_PORT_PLACE    │
  │  ERACK_TAKE/PLACE │
  │  STK_TAKE/PLACE   │
  └────────────────────┘
           ↕
    ┌──────────────┐
    │  Vision Jobs  │ ← TMark/AprilTag/Barcode
    │  Sensor Check │ ← 夾爪/雷射/IO
    │  Log/Modbus   │ ← 回報 AMR
    └──────────────┘

背景執行緒（常駐同時運作）：
  - CHECK_GRIP_2        持續監控夾爪（440 節點）
  - CHECK_ENCODER       監控編碼器（17 節點）
  - CHECK_ALL_SENSOR_WHEN_CAR_MOVING_2  移動中安全監控（86 節點）
  - Pause_handle        處理暫停請求（9 節點）
  - Pub_RS485IO         發佈 I/O 狀態（7 節點）
```

---
