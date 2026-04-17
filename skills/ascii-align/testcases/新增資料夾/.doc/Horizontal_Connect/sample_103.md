## Sample 103

**Source**: `D435i_LidarScan\REPORT_v3_depth_compensation.md` L233

```
D435i Camera (emitter OFF)
    │
    ├── IR Left (1280x720 Y8)
    ├── IR Right (1280x720 Y8)
    │         │
    │         ▼
    │   Resize 1280x720 → 640x360
    │   Gray → 3-channel [B, 3, H, W] float32
    │         │
    │   ┌─────┴─────┐
    │   │ CREStereo  │  ← ONNX, background thread
    │   │ iter2      │     ~70ms per inference
    │   │ 360x640    │     DirectML GPU / CPU fallback
    │   └─────┬─────┘
    │         │
    │   Output: flow [2, 360, 640]
    │   → take x-flow → abs() → disparity
    │         │
    │   Depth = baseline × fx / (disparity × scale_x)
    │     baseline ≈ 50.0mm (factory calibrated)
    │     fx ≈ 649.9px (at 1280x720)
    │     scale_x = 1280/640 = 2.0
    │         │
    │         ▼
    │   Neural depth map (640x360, float32, meters)
    │
    ├── Built-in Stereo (emitter OFF)
    │   → depth_frame → decimation → spatial → temporal
    │   → stereo depth (640x360, ~11% coverage, 32mm MAE)
    │         │
    │         ▼
    │   ┌─────────────────────────────────────────┐
    │   │ Fusion:                                 │
    │   │   fused[stereo > 0] = stereo  ← 優先   │
    │   │   fused[stereo = 0] = neural  ← 填補   │
    │   └─────────────────────────────────────────┘
    │         │
    │         ▼
    │   Fused depth map (640x360, ~100% coverage)
    │         │
    │   _depth_to_points_from_array()
    │   → 3D point cloud [N, 3]
    │
    └── IMU → Gravity → Rotation R
              → Ground-aligned coordinates
```

---

