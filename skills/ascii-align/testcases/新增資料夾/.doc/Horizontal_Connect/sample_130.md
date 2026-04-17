## Sample 130

**Source**: `HaloScan_v0\docs\01_會議計畫書_v0.md` L17

```
4× Livox Mid-360 (各 200K pts/s，合計 ~800K pts/s)
│
├─── 路徑 A：安全區偵測（本專案核心）
│    │
│    TF transform（sensor frame → /base_link，含 pitch offset）
│    │
│    C++ 安全區判定（PCL CropBox / 手寫座標閾值）
│    ├── 4 核心各處理 1 顆 LiDAR（std::thread / OpenMP）
│    ├── 定義 3D Bounding Box：停止區、減速區、懸崖區
│    └── 點落在危險區 → 計數超過雜訊閾值 → 觸發狀態
│    │
│    統整 4 顆結果 → 發佈 std_msgs/Int8
│    │        0 = 安全 ／ 1 = 減速 ／ 2 = 停止
│    │
│    RPi 5 ──(ROS Topic via Switch)──→ IPC (ROS Master 訂閱)
│                                       └─ 0.5s watchdog timeout
│                                          未收到 → 強制停車
│
└─── 路徑 B：導航避障（沿用既有導航架構）
     │
     TF transform → PassThrough filter (z: 0.00~1.80m)
     │
     ConcatenatePointCloud（合併 4 組）
     │
     pointcloud_to_laserscan（最近距離投影 → 2D）
     │
     /scan（sensor_msgs/LaserScan，10 Hz，360°）
     │
     Nav2 Costmap ／ 導航軟體消費
```

---

