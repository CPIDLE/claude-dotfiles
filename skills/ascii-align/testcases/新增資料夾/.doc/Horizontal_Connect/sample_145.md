## Sample 145

**Source**: `HaloScan_v0\docs\04_Mid360_技術計畫_初版.md` L150

```
livox_ros_driver2（x  4，各感測器獨立 topic）
      │
TF transform（sensor frame --> /base_link，含 pitch offset）
      │
PassThrough filter：z: 0.00 m ～ 1.80 m
      │
ConcatenatePointCloud（合併 4 組點雲）
      │
pointcloud_to_laserscan（最近距離投影 --> 2D）
      │
/scan（sensor_msgs/LaserScan，10 Hz，360°）
      │
Nav2 Costmap  ／  安全停機層
```

