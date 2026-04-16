## Sample 097

**Source**: `D435i_LidarScan\README.md` L41

```
D435i Camera (emitter OFF)
    │
    ├── IR Left + Right ───> CREStereo ONNX (bg thread, ~70ms)
    │                       --> metric depth (textured surfaces)
    │
    ├── Color RGB ─────────> Depth Anything V2 ONNX (bg thread, ~77ms)
    │                       --> relative inverse depth (smooth surfaces)
    │                       --> per-frame scale correction from stereo overlap
    │
    ├── IR Left ───────────> Texture map (local variance)
    │                       low variance = smooth --> use mono
    │                       high variance = textured --> use CREStereo
    │
    ├── Built-in Stereo ───> Priority 1: stereo (32mm MAE, ~11%)
    │   (640x360)           Priority 2: mono on smooth gaps
    │                       Priority 3: CREStereo on textured gaps
    │                       Fallback: whichever available
    │                         │
    │                         v 
    │                fused depth (640x360, ~100% coverage)
    │                         │
    └── IMU ───> Gravity ───> _depth_to_points --> 3D point cloud
```

