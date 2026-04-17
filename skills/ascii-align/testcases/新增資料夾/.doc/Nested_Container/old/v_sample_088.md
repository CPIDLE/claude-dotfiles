## Sample 088

**Source**: `D435i_LidarScan\FLOW.md` L211

```
When --emitter is enabled, IR emitter runs in blink cycle:

    ┌─────────────────────────────────────────────────────────────┐
    │  3.0s OFF          │ 3 frames ON (~0.2s) │  3.0s OFF  ...   │
    │  emitter=0         │ emitter=1           │  emitter=0       │
    │                    │                     │                  │
    │  Neural stereo v   │ Neural stereo x     │  Neural stereo v │
    │  Mono depth    v   │ Mono depth    x     │  Mono depth    v │
    │  Fusion        v   │ Fusion: skip        │  Fusion        v │
    │  Apply corr maps   │ Update corr maps    │  Apply corr maps │
    │  -> corrected fused│ -> real_points only │  -> corrected    │
    └─────────────────────────────────────────────────────────────┘

Emitter ON frames:
  - Built-in stereo has high coverage (~62%) from IR dot pattern
  - Neural stereo/mono push skipped (IR dots corrupt input)
  - Capture stereo depth as reference (ground truth)
  - Compare reference vs stale neural/mono results --> update correction maps
  - No fusion - use real_points directly

Emitter OFF frames (majority):
  - Normal fusion pipeline: stereo + CREStereo + mono depth
  - Neural depth x neural_correction_map --> corrected neural depth
  - Mono relative depth x mono_correction_map --> corrected mono (before scale_map)
  - Correction maps fix systematic model bias, not scene geometry

Correction map computation:
  - Per-block (20x20) median of ref_depth / pred_depth
  - EMA blend a=0.7 new + 0.3 old across blink cycles
  - Clamped to [0.5, 2.0] range
  - Requires >30% emitter-ON coverage, >500 overlap pixels

Compatible with: --neural-stereo, --mono-depth, standalone
```

---

