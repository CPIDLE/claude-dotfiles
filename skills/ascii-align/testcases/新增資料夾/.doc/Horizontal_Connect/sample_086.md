## Sample 086

**Source**: `D435i_LidarScan\FLOW.md` L104

```
┌─────────────────────────────────────────────┐
│ 1. Enable streams                           │
│    ├── depth (1280x720, z16, 15fps)         │
│    ├── color (1280x720, rgb8, 15fps)        │
│    ├── infrared 1 (1280x720, y8, 15fps) *   │
│    ├── infrared 2 (1280x720, y8, 15fps) *   │
│    ├── accel (accelerometer)                │
│    └── gyro  (gyroscope)                    │
│    (* IR when --neural-stereo or --mono-depth)│
│                                             │
│ 2. Configure sensor                         │
│    ├── Emitter: BLINK mode or OFF           │
│    ├── Set visual preset (high_accuracy)    │
│    └── Get depth_scale                      │
│                                             │
│ 3. Neural stereo setup (if enabled)         │
│    ├── Get IR intrinsics (fx for depth)     │
│    ├── Get stereo baseline from extrinsics  │
│    └── Create NeuralStereoEstimator         │
│                                             │
│ 4. Configure post-processing filters        │
│    ├── Decimation: magnitude = 2            │
│    │   (1280x720 → 640x360)                │
│    ├── Spatial: alpha=0.5, delta=20         │
│    ├── Temporal: alpha=0.2, delta=50        │
│    └── Threshold: range_min ~ range_max     │
│                                             │
│ 5. Get depth intrinsics (fx, fy, cx, cy)    │
│                                             │
│ 6. Precompute pixel coordinate grid         │
│    u_grid[H,W], v_grid[H,W]                │
└─────────────────────────────────────────────┘
```

---

