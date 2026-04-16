## Sample 035

**Source**: `AMRCoolDown_v0\Phase2_原始碼分析報告.md` L183

```
Step 1: 從 12 個 ROS Subscriber 讀取最新狀態
       ├── /carmovestate (routeprogress) --> 車輛移動狀態
       ├── /battery_level (Float32)      --> 電池電量
       ├── /robot_pose (Pose)            --> 機器人位姿
       ├── /sysindicator/error (syserr)  --> 警報代碼
       ├── /sysindicator/warn (syswarn)  --> 警告代碼
       ├── /rfiderack (String)           --> RFID 讀取
       ├── /rfiderack_UHF (String)       --> UHF RFID
       ├── /cansns (cansns1)             --> CAN 感測器 1
       ├── /cansns4 (cansns4)            --> CAN 感測器 4
       ├── /cansns2 (cansns2)            --> CAN 感測器 2
       ├── /docking_pose (Float32MultiArray) --> 對接位姿
       └── listener class 封裝每個 subscriber

Step 2: 比較 20+ 個 field 的 new vs old 值
       ├── work_status, docking_status, next_point...
       ├── arm_status, battery_level, e84State...
       ├── lotStatus, chargeStationState, alarmcode...
       └── 任一欄位變化 --> 觸發寫入

Step 3: 如果有變化
       ├── check_file()       --> 驗證 CSV 檔案完整性（讀取整個檔案！）
       ├── 讀取 CSV 最後一行  --> 與新資料再次比較
       └── 寫入 CSV            --> append 一行（25 個欄位）

Step 4: 更新 old = new（15 個 field）
```

