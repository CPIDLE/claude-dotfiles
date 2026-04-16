## Sample 104

**Source**: `D435i_LidarScan\REPORT_v3_depth_compensation.md` L285

```
┌─────────────────────────────────────────────────┐
│  Main Thread            Background Thread       │
│                                                 │
│  push_ir_pair(L, R)                             │
│       │                                         │
│       v                                         │
│  _pending_pair ──event───> _worker()            │
│                              │                  │
│                         Resize IR               │
│                         1280x 720 --> 640x 360  │
│                         Gray --> 3ch [B,3,H,W]  │
│                              │                  │
│                         ONNX inference          │
│                         (DML GPU or CPU)        │
│                              │                  │
│                         raw[0] --> disparity    │
│                         (abs of x-flow)         │
│                              │                  │
│                         depth = baselinex fx/disp│
│                         --> _latest_depth       │
│                              │                  │
│  get_latest_depth() <────────┘                  │
│       │                                         │
│  thread-safe (Lock)                             │
└─────────────────────────────────────────────────┘
```

