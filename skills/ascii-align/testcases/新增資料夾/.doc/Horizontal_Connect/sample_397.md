## Sample 397

**Source**: `Reporter_v1\WORKSPACE\a01\19_Vision_Depth_Integration.md` L211

```
4x  Livox Mid-360 (Ethernet UDP)
  └--> PTP 時間同步
       └--> 點雲合併
            ├--> 路徑 A: CropBox 3D 安全區偵測 --> 停車/減速（RPi 5, C++）
            ├--> 路徑 B: 高度過濾 --> 2D LaserScan --> Nav2 costmap
            └--> 路徑 C（規劃中）: 4x  魚眼 + YOLOv8-seg（Jetson Orin NX）
```

