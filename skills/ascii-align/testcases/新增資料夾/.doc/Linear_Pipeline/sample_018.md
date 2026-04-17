## Sample 018

**Source**: `AMRCoolDown_v0\AMR_網路頻寬分析.md` L197

```
RealSense D435 × 4
  ↓ USB 3.0（每台 ~30 MB/s）
  ↓
ROS Driver（realsense-ros）
  ↓ 發布 /d435_*/color/image_raw（30 Hz, 921 KB/frame）
  ↓
┌─────────────────────────────────┐
│ Subscriber 1: camera_monitor    │ ← 接收 4 台 = 110 MB/s
│ Subscriber 2: processjsonservice│ ← 接收 4 台 = 110 MB/s（視覺定位時）
│ Subscriber 3: video_record      │ ← 接收 4 台 = 110 MB/s（錄影時）
│ Subscriber 4: web_video_server  │ ← 接收 4 台 = 110 MB/s（串流時）
└─────────────────────────────────┘
                                    最壞情況：4 subscriber × 110 MB/s = 440 MB/s
                                    = CPU 必須每秒複製/序列化 440 MB 的 image data
```

---

