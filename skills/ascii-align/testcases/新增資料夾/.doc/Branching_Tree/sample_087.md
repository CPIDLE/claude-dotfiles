## Sample 087

**Source**: `D435i_LidarScan\FLOW.md` L157

```
while True:
    ┌──────────────────────────────────────────────────┐
    │              process_frame()                     │
    │                    │                             │
    │         ┌──────── v  ────────┐                   │
    │         │   _get_frames()    │                   │
    │         └──────── │ ─────────┘                   │
    │                   │                              │
    │      ┌────────┬───┼────────┬──────┐              │
    │      v        v   v        v      v              │
    │    depth   accel gyro   IR_L    IR_R             │
    │    frame   [xyz] [xyz]  (Y8)    (Y8)             │
    │      │        │                   │              │
    │      │        v                   │              │
    │      │  GravityEstimator.update() │              │
    │      │        │                   │              │
    │      │        v                   │              │
    │      │  get_rotation_matrix()-->R │              │
    │      v                            v              │
    │    ┌── neural_stereo ON? ───────────────┐        │
    │    │ YES                         NO     │        │
    │    │                                    │        │
    │    │ real_points (stereo, ~11%)         │        │
    │    │   (for camera height only)         │        │
    │    │ push IR pair --> bg thread         │        │
    │    │ get_latest_depth --> neural depth  │        │
    │    │ fuse(stereo + neural) --> ~100%    │        │
    │    │ --> fused_points [N,3]             │        │
    │    │                    _depth_to_points│        │
    │    │                    + ground_synth  │        │
    │    │                    --> points [N,3]│        │
    │    └────────────┬───────────────────────┘        │
    │                 │                                │
    │                 ├────────────────┐               │
    │                 v                v               │
    │  _points_to_scan(R)  _points_to_ground_lines(R)  │
    │  [LiDAR 1: horizontal] [LiDAR 2: ground]         │
    │                 │                │               │
    │                 v                v               │
    │     LaserScan        (LaserScan, LaserScan)      │
    │                      line0        line1          │
    └─────┬───────────────────┬────────────────────────┘
          │                   │
    ┌─────┼─────┐        ┌────┼────┐
    v     v     v        v         v
  draw  net_out Rerun   ground_out ground_out
  scan  .send() 3D viz  [0].send() [1].send()
```

