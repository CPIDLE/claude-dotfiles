## Sample 649

**Source**: `WebCamToLidarScan\docs\REQUIREMENTS.md` L51

```
sensor_msgs/Image (深度圖, 16UC1 or 32FC1)
  +
sensor_msgs/CameraInfo (相機內參)
        │
        ▼
  ┌─────────────────────────────────────────────────────┐
  │  ⓪ 預計算查找表 (LUT)  — 僅在啟動/參數變更時執行一次  │
  │                                                     │
  │  對每個像素 (u, v) 預先計算:                           │
  │    • ray_x = (u - cx) / fx                          │
  │    • ray_y = (v - cy) / fy                          │
  │    • 水平角度 angle = atan2(ray_x, 1.0)             │
  │    • 對應的 angular bin index                        │
  │    • 地平面高度係數 (用於快速高度計算)                  │
  └─────────────────┬───────────────────────────────────┘
                    │ (一次性, 啟動時)
                    ▼
  ┌─────────────────────────────────────────────────────┐
  │  ① 地平面校正  — 啟動時收集 N 幀，RANSAC 擬合一次     │
  │                                                     │
  │  校正完成後，對每個像素預計算:                          │
  │    height_coeff[u,v] = (a·ray_x + b·ray_y + c) / ‖n‖│
  │  使得: 像素高度 = depth × height_coeff[u,v] + d/‖n‖  │
  └─────────────────┬───────────────────────────────────┘
                    │ (一次性, 校正後)
                    ▼
  ┌─────────────────────────────────────────────────────┐
  │  ② 單次遍歷核心（每幀執行）                            │
  │                                                     │
  │  for each pixel (u, v):                             │
  │    depth = depth_image[v][u]                        │
  │    if depth < range_min or depth > range_max:       │
  │        continue                  // 距離無效          │
  │                                                     │
  │    height = depth × height_coeff[u][v] + d_offset   │
  │    if height < h_min or height > h_max:             │
  │        continue                  // 高度不在避障範圍   │
  │                                                     │
  │    bin = bin_index_lut[u]        // 查表取角度 bin    │
  │    range = depth × range_coeff[u][v]  // 水平距離    │
  │                                                     │
  │    if range < scan[bin]:                            │
  │        scan[bin] = range         // 保留最近點        │
  │                                                     │
  └─────────────────┬───────────────────────────────────┘
                    │
                    ▼
          sensor_msgs/LaserScan (虛擬 2D LiDAR)
```

---
