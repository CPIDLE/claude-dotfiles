## Sample 105

**Source**: `D435i_LidarScan\REPORT_v3_depth_compensation.md` L430

```
D435i Camera (emitter OFF) ───> Depth Frame ───> 3D Point Cloud ───> Ground-Aligned
                  IMU Frame  ───> Gravity Vector ───> Rotation Matrix ┘
               Color Frame  ───> Floor Segmentation ─┐                │
           IR Left + Right  ───> CREStereo (ONNX) ───┤                │
                                                     │                │
                                           ┌─────────┴───────────────┴┐
                                           v                             v 
                                  [LiDAR 1: Horizontal]       [LiDAR 2: Ground]
                                   Height Filter --> 2D Scan     Vertical Angle Filter
                                           │                   --> 2 x  LaserScan
                                   ┌───────┤                          │
                                   v        v                    ┌─────┴─────┐
                                 UDP:7777  ROS2:/scan          v            v 
                                 OpenCV                     UDP:7778    UDP:7779
                                                            line0       line1
```

