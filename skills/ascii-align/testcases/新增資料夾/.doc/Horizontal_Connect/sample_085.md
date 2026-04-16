## Sample 085

**Source**: `D435i_LidarScan\FLOW.md` L88

```
D435iLidarScanner
├── rs.pipeline()              <-- RealSense pipeline
├── GravityEstimator(alpha=0.98)  <-- IMU low-pass filter
├── NeuralStereoEstimator      <-- (optional, when --neural-stereo)
│   └── CREStereo ONNX + background thread
├── MonoDepthEstimator         <-- (optional, when --mono-depth)
│   └── Depth Anything V2 ONNX + background thread
└── Post-processing filters
    ├── rs.decimation_filter()
    ├── rs.spatial_filter()
    ├── rs.temporal_filter()
    └── rs.threshold_filter()
```

