## Sample 033

**Source**: `AMRCoolDown_v0\Phase2_原始碼分析報告.md` L39

```
usserver.py
├── __init__()
│   ├── sensor_model: "UB350"（ROS param，實際值 UB350）
│   ├── rate: frame_rate（ROS param，實際值 8Hz）
│   ├── sensor_number: 8 個超音波感測器
│   ├── uslimit[]: 各感測器距離門檻
│   └── Publisher: /usserial (Int16MultiArray)
├── NormalProcess()  <-- 主迴圈，threading 運行
│   └── while KeepRunning:
│       ├── usmod.dislimitArray_get()  <-- 讀取感測器
│       ├── usserialpub.publish()      <-- 發布到 ROS topic
│       └── time.sleep(resttime) 或 busy wait
└── vrstart()  <-- 啟動 daemon thread

usmodule_UB350.py（感測器驅動）
├── __init__()
│   ├── baudrate: 115200
│   └── comport: /dev/ttyS0（serial port）
├── start()  <-- 開啟 serial port
└── dislimitArray_get()  <-- 核心讀取函式
    ├── while True: serial.read(1) 逐 byte 搜尋 header "UT"
    ├── serial.read(13) 讀取剩餘資料
    ├── XOR checksum 驗證
    └── 判斷 8 個感測器距離是否超過門檻
```

