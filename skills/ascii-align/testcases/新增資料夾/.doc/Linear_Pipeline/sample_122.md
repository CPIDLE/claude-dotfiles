## Sample 122

**Source**: `D455_LidarScan\README_temp.md` L420

```
D435i (single camera)
    │
    ├──► LiDAR 1: Horizontal 2D LiDAR
    │    ├── Simulates Hokuyo / RPLIDAR / SICK
    │    ├── Height range 0.1~1.8m compressed to single scan plane
    │    ├── For: obstacle avoidance, SLAM, navigation
    │    └── Output: UDP :7777 or ROS2 /scan
    │
    └──► LiDAR 2: Dual-Line Ground Scanner
         ├── Two scan lines at α° and (α+Δ)° below horizontal
         ├── Slant range (3D distance) per bin
         ├── For: AGV ground inspection (pit/bump detection)
         └── Output: UDP :7778/:7779 or ROS2 /ground_scan/line0, line1
```

---

