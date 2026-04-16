## Sample 393

**Source**: `Reporter_v1\WORKSPACE\a01\19_Vision_Depth_Integration.md` L149

```
D435i (IR OFF)
  ├--> 內建 stereo depth ───> 覆蓋率 ~11%（32mm MAE）
  └--> CREStereo ONNX ─────> 覆蓋率 ~89%（95mm MAE）
       └--> 融合（stereo 優先）───> ~100% 覆蓋率
            └--> 水平切片 --> 1081-bin LaserScan
                 └--> UDP / ROS2 LaserScan
```

