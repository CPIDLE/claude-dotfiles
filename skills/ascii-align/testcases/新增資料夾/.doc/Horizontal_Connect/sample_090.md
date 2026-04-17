## Sample 090

**Source**: `D435i_LidarScan\FLOW.md` L410

```
Purpose: combine all depth sources for optimal coverage + quality.
Active when --neural-stereo and/or --mono-depth enabled.

Per-frame mono scale correction:
    mono_rel = 1.0 / inv_depth
    scale = median(stereo[overlap] / mono_rel[overlap])  (IQR robust)
    scale_ema = 0.1 * scale + 0.9 * scale_ema
    mono_metric = mono_rel * scale_ema

Texture map from IR:
    local_var = blur(IR²) - blur(IR)²     (7×7 kernel)
    low_texture = local_var < threshold    (default: 50)

3-level fusion:
    ┌──────────────────────────────────────────────────────┐
    │  1. stereo valid?         → built-in stereo (32mm)   │
    │  2. gap + low texture?    → mono metric   (smooth)   │
    │  3. gap + high texture?   → CREStereo     (metric)   │
    │  4. gap + fallback?       → whichever available       │
    └──────────────────────────────────────────────────────┘

Backward compatibility:
    --neural-stereo only        → CREStereo fills all gaps (v3 behavior)
    --mono-depth only           → mono fills all gaps
    --neural-stereo --mono-depth → texture-adaptive fusion
```

---

