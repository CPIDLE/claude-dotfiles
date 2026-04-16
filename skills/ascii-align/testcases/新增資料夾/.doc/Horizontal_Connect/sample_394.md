## Sample 394

**Source**: `Reporter_v1\WORKSPACE\a01\19_Vision_Depth_Integration.md` L163

```
D435i (IR OFF)
  └--> Stage 1: 資料擷取
       └--> Stage 2: NLSPN 深度補全（>200ms）
            └--> Stage 3: YOLO 物體偵測（non-blocking）
                 └--> Stage 4: 點雲處理 + RANSAC
                      └--> Stage 5: 場景分析
                           └--> Stage 6: SegFormer 分割 + Rerun 3D
```

