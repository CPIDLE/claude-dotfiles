## Sample 644

**Source**: `UR_Program_Analysis_v0\docs\FLOW_ANALYSIS.md` L330

```
K11_UR30_Project/programs/
├── Gyro/                           # 核心與輔助
│   ├── initial_prog.script/.txt    # 主程式入口（12,241 行）
│   ├── initial_modbus_tcp.script   # Modbus TCP 訊號定義
│   ├── tc100_gripper_open.script   # 夾爪開啟
│   ├── tc100_gripper_close.script  # 夾爪關閉
│   ├── fork_sensor_check.script    # Fork sensor 檢查
│   ├── payload.script              # Payload 計算
│   ├── set_alarm_and_stop.script   # 統一錯誤處理
│   ├── get_command_*.script        # 指令解析
│   ├── gripeer_cover_*.script      # 蓋子開關
│   ├── Loop.script / Loop_initial.script  # 迴圈計數器
│   └── rs485io_read.script         # RS485 IO 讀取
├── Body_*.script/.txt              # Body 取放
├── EQ*.script/.txt                 # 各設備操作
├── Erack_*.script/.txt             # Erack 裝卸
├── .SensoPart/calibsets/*.calib    # VISOR 校正
└── *.urp                           # 二進位程式（未解析）
```

