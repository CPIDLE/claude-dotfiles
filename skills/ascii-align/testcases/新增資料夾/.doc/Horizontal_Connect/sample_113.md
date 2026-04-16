## Sample 113

**Source**: `D455_LidarScan\FLOW.md` L160

```
D455 Camera
    │
    ├── Depth (z16, 1280x720 @ 30fps)
    │    ├── Decimation (/ 2 --> 640x360)
    │    ├── Threshold (0.6-6.0m)
    │    ├── Spatial (edge-preserving smooth)
    │    ├── Temporal (inter-frame smooth)
    │    └── Vectorized deprojection --> Nx3 point cloud
    │
    ├── IR Left/Right (y8, 1280x720 @ 30fps) [if --neural-stereo]
    │    └── CREStereo ONNX (background thread)
    │         ├── Resize to model resolution (640x360)
    │         ├── Disparity bias correction (ratio LUT)
    │         ├── Disparity --> metric depth (baseline * fx / disp)
    │         └── Fusion: stereo base + neural fills gaps
    │              └── IP-Basic gap filling (dilation + bilateral)
    │
    ├── Color (rgb8, 1280x720 @ 30fps) --> Rerun camera image
    │
    ├── Accelerometer --> GravityEstimator --> Rotation Matrix
    │
    └── Point cloud + Rotation
         │
         ├── Auto camera height (EMA, 15th percentile)
         │
         ├───> LiDAR 1: Height filter --> 2D polar --> LaserScan
         │    └── Output: OpenCV / Rerun / UDP / ROS2
         │
         └───> LiDAR 2: Vertical angle filter --> Dual LaserScan
              └── Output: Rerun / UDP / ROS2
```

