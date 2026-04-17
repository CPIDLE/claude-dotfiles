## Sample 107

**Source**: `D435I_LidarScan_v1\D435i_DepthCompletion_CLAUDE.md` L45

```
D435i（IR Emitter OFF）
    │
    ├─ RGB stream (color)
    ├─ Left IR stream  (emitter off → passive texture only)
    ├─ Right IR stream
    └─ Stereo Depth stream (sparse + holes in featureless regions)
         │
         ▼
  [Stage 1] librealsense Post-processing Filters
  Spatial filter + Temporal filter + Hole-filling filter
  → 快速修補小孔洞，零 AI 成本
         │
         ▼
  [Stage 2] AI Depth Completion
  Input:  RGB image  +  sparse depth (from Stage 1)
  Model:  SparseDC 或 NLSPN（依速度需求選擇）
  Output: Dense depth map
         │
         ▼  （Stage 2 仍有大片 invalid 時的 fallback）
  [Stage 3] Monocular Depth Estimation（選配）
  Input:  RGB image only
  Model:  Depth Anything V2 Small（metric depth）
  用途:   補全 Stage 2 剩餘孔洞，scale 對齊後融合
         │
         ▼
  最終 Dense Depth Map → 障礙物偵測 / Costmap
```

---

