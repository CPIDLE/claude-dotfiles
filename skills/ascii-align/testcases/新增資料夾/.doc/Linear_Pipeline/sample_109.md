## Sample 109

**Source**: `D435i_LidarScan_v2\CLAUDE.md` L15

```
D435i (Emitter OFF, manual exposure for metal reflections)
  │
  ├─ RGB + Depth (Z16 --> CUDA Float32 Tensor)
  │
  v 
[Stage 1] Foundation -- Rerun streaming (RGB, Depth, Time-sequence), CUDA buffer init
  v 
[Stage 2] SDK Pre-processing -- Decimation --> Spatial --> Temporal --> Hole Filling filters
  v 
[Stage 3] YOLO Semantic Detection (TensorRT) -- BBox + Mask for walls/floors/steel equipment
  v 
[Stage 4] Geometric Completion -- CUDA RANSAC plane fitting within YOLO regions, fill zeros with plane equation
  v 
[Stage 5] Neural Refinement -- NLSPN or Depth Anything V2 Small, RGB+sparse depth fusion, weighted residual correction
  v 
[Stage 6] Output -- Camera-->Base Link transform, Voxel Grid downsampling, .pcd or ROS2 PointCloud2 broadcast
```

