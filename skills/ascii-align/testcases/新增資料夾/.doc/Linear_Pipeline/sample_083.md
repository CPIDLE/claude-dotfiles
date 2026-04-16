## Sample 083

**Source**: `D435i_LidarScan\FLOW.md` L5

```
D435i Camera (emitter BLINK/OFF) -> Depth Frame ───> 3D Point Cloud ───> Ground-Aligned
                  IMU Frame  ───> Gravity Vector ───> Rotation Matrix ┘
               Color Frame  ───> Depth Anything V2 (mono) ─┐          │
           IR Left + Right  ───> CREStereo (stereo ONNX) ──┤          │
                            ───> Texture Map (IR variance)──┤         │
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

