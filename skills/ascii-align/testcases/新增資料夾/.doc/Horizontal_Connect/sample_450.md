## Sample 450

**Source**: `Reporter_v1\WORKSPACE\a02\AMR_Log_to_SQLite_遷移方案.md` L22

```
case01/260319_260328_195945_L4STR-nnUF-FD124-FS54/
├── job/            carwork_*.csv         (1-2 Hz, ~3MB/天)    車輛狀態、位置、電池、alarm
├── statistics/     consumption_*.csv     (1 Hz, ~12MB/天)     馬達負載、電池、輪距、TM 電流
│                   WIFI_Coor_*.csv       (高頻, ~8MB/天)      WiFi 座標、訊號強度
├── tcpbridge/      pscmd_*.csv           (依指令, ~3MB/天)    AMR <-> TSC TCP 指令
│                   log/*inputlog.txt.log                      TCP 序列號原始記錄
│                   log/*outputlog.txt.log
├── maintain/       carmaintain_*.csv     (稀疏, ~KB)          維修記錄
│                   carmeterage_*.csv     (1 Hz, ~2KB/天)      里程、電池循環數
├── e84/            *_PIO1.log            (~37KB/天)           E84 硬體錯誤碼
│                   errorlog.txt                               歷史錯誤彙總
├── ros/            rostopic_*.log        (2,761 檔, ~480MB)   ROS node 啟動、topic 連線
└── syswork/        cpu_monitor 輸出      (每 5s, ~1MB/天)     CPU% / RAM / Load
```

