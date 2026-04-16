## Sample 650

**Source**: `WebCamToLidarScan\docs\REQUIREMENTS.md` L263

```
    ┌───────────────┐
    │  UNCONFIGURED  │
    └──────┬────────┘
           │ on_configure():
           │   • 載入參數
           │   • 初始化 subscriber / publisher
           │   • 等待第一幀 CameraInfo
           ▼
    ┌───────────────┐
    │   INACTIVE     │
    └──────┬────────┘
           │ on_activate():
           │   • 收到 CameraInfo → 建立 bin_index LUT
           │   • 開始收集校正幀
           ▼
    ┌───────────────┐
    │  CALIBRATING   │  收集 N 幀 → 取樣 → RANSAC
    │                │  → 建立 height_coeff + range_coeff LUT
    └──────┬────────┘
           │ 校正完成 → 發布 calibration_done = true
           ▼
    ┌───────────────┐
    │    ACTIVE      │  每幀: 讀深度圖 → 單次遍歷 → 發布 LaserScan
    └───────────────┘
           │ recalibrate_ground service
           ▼
         回到 CALIBRATING
```

