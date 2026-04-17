## Sample 096

**Source**: `D435i_LidarScan\FLOW.md` L702

```
D435i USB 3.0
    │
    ├── Depth Stream (1280×720 @ 15fps)
    │       │
    │       ▼
    │   [Decimation] → [Threshold] → [Spatial] → [Temporal]
    │       │
    │       ▼
    │   depth_image (640x360 float32, meters)
    │       │
    │       ├──── [--neural-stereo/--mono-depth ON] ────────┐
    │       │     stereo_depth (numpy, ~11% coverage)       │
    │       │         │                                     │
    │       │         ▼                                     │
    │       │     3-source texture-adaptive fusion:          │
    │       │     ├── stereo valid → stereo    (32mm MAE)   │
    │       │     ├── gap+smooth  → mono      (scaled)      │
    │       │     └── gap+textured → CREStereo (metric)     │
    │       │         │                                     │
    │       │         ▼                                     │
    │       │     fused_depth → _depth_to_points_from_array │
    │       │     → points [N, 3]  (~100% coverage)         │
    │       │                                               │
    │       ├──── [--neural-stereo OFF] ────────────────┐   │
    │       │     Vectorized deprojection               │   │
    │       │     → real_points [N, 3]                  │   │
    │       │         │                                 │   │
    │       │         ├── [Emitter OFF] Ground synthesis │   │
    │       │         │   Color seg + plane eq           │   │
    │       │         │   → points = concat(real, synth) │   │
    │       │         │                                 │   │
    │       │         └── [Emitter ON] points = real     │   │
    │       │                                           │   │
    │       ├─── Camera height: stereo-only points (EMA)┘   │
    │       │                                               │
    │       ▼                                               │
    │   3D point cloud [N, 3] ◄─────────────────────────────┘
    │       │
    │       ├──────────────────────┐
    │       ▼                      ▼
    │   [LiDAR 1: Horizontal]  [LiDAR 2: Ground]
    │       │                      │
    │       ▼                      ▼
    │   Height filter          Vertical angle filter
    │   (0.1m ~ 1.8m)         (a° ± tol, (a+d)° ± tol)
    │       │                      │
    │       ▼                      ▼
    │   2D projection          Horizontal angular binning
    │   (XZ plane)             (slant range)
    │       │                      │
    │       ▼                      ▼
    │   Polar + binning        (LaserScan_0, LaserScan_1)
    │   (model specs)              │
    │       │                      ├──► UDP :7778 (line0)
    │       ▼                      └──► UDP :7779 (line1)
    │   LaserScan                  └──► ROS2 /ground_scan/*
    │       │
    │       ├──► OpenCV visualization
    │       ├──► UDP :7777 (broadcast)
    │       ├──► ROS2 /scan
    │       └──► Rerun 3D viewer
    │
    ├── Color Stream (1280×720 @ 15fps, RGB8)
    │       │
    │       ├── [--mono-depth] → MonoDepthEstimator.push_rgb()
    │       │       → background thread
    │       │       → resize → ImageNet norm → [1,3,210,364]
    │       │       → Depth Anything V2 ONNX (~77ms)
    │       │       → inverse depth (for fusion on next frame)
    │       │
    │       ├── [emitter OFF, no neural/mono] → ground point synthesis
    │       │
    │       └── Rerun camera image
    │
    ├── IR Left Stream (1280×720 @ 15fps, Y8)  *
    ├── IR Right Stream (1280×720 @ 15fps, Y8) *
    │       │  (* when --neural-stereo or --mono-depth)
    │       │
    │       ├── [--neural-stereo] NeuralStereoEstimator.push_ir_pair()
    │       │       → background thread
    │       │       → resize 1280×720 → 640×360
    │       │       → CREStereo ONNX inference (~70ms)
    │       │       → disparity → depth (baseline × fx / disp)
    │       │       → _latest_depth (for fusion on next frame)
    │       │
    │       └── [--mono-depth] → texture map (IR local variance)
    │
    ├── Accel Stream (63/250 Hz)
    │       │
    │       ▼
    │   GravityEstimator (low-pass alpha=0.98)
    │       │
    │       ▼
    │   Rotation matrix R [3×3] ──────────────────────────────
    │
    └── Gyro Stream (200/400 Hz)
            │
            └── (reserved for future complementary filter)
```

---
