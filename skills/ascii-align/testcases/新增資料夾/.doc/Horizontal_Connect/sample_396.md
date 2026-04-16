## Sample 396

**Source**: `Reporter_v1\WORKSPACE\a01\19_Vision_Depth_Integration.md` L195

```
RGB (webcam / D435i)
  └--> DA V2 ViT-S ONNX (94.5MB)
       └--> Metric Depth Map
            └--> RANSAC 地面校正（IMU gravity constraint）
                 └--> LUT 單次遍歷 --> ~650 bins LaserScan
                      └--> EMA 時序濾波（IMU-aware）
                           └--> [選用] Ego-motion 多幀拼接
                                └--> ROS 2 /virtual_scan
```

