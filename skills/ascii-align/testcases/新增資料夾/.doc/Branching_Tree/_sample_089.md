## Sample 089

**Source**: `D435i_LidarScan\FLOW.md` L253

```
pipeline.wait_for_frames()
         │
         ├──► depth_frame
         │         │
         │         ▼  Post-processing pipeline
         │    ┌─────────────┐
         │    │ Decimation   │  1280x720 → 640x360 (mag=2)
         │    └──────┬──────┘
         │    ┌──────▼──────┐
         │    │ Threshold    │  Remove < range_min or > range_max
         │    └──────┬──────┘
         │    ┌──────▼──────┐
         │    │ Spatial      │  Edge-preserving spatial smoothing
         │    └──────┬──────┘
         │    ┌──────▼──────┐
         │    │ Temporal     │  Cross-frame temporal smoothing
         │    └──────┬──────┘
         │           ▼
         │    filtered depth_frame
         │    (+ update intrinsics if resolution changed)
         │
         ├──► color_frame → RGB8 image (1280x720)
         │    (stored for ground synthesis + visualization)
         │
         ├──► infrared_frame(1) → Left IR (1280x720 Y8)  *
         ├──► infrared_frame(2) → Right IR (1280x720 Y8) *
         │    (* when --neural-stereo enabled)
         │
         ├──► accel_frame → [ax, ay, az]  (m/s²)
         │
         └──► gyro_frame  → [gx, gy, gz]  (rad/s)
```

---
