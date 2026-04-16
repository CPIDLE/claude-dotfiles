## Sample 102

**Source**: `D435i_LidarScan\REPORT_v3_depth_compensation.md` L79

```
Color Frame (1280x720 RGB)
    │
    v 
Resize --> (364x210 或其他解析度)
    │
    v 
ImageNet 正規化
  mean=[0.485, 0.456, 0.406]
  std =[0.229, 0.224, 0.225]
    │
    v 
ONNX Inference (DmlExecutionProvider / CPU)
  Model: depth_anything_v2_small.onnx (INT8, ~27MB)
  Input: pixel_values [1, 3, H, W] float32
    │
    v 
Output: predicted_depth [1, H, W]
  --> 相對反向深度（relative inverse depth / disparity）
  --> 非公制深度！需要 scale 校正
    │
    v 
Resize to depth frame resolution
    │
    v 
自動偵測反向深度 (correlation < 0 --> 取倒數)
    │
    v 
Scale / Affine 校正 (median ratio with stereo)
    │
    v 
融合：stereo 有值用 stereo，無值用 mono
```

