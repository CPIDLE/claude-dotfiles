## Sample 657

**Source**: `WebCamToLidarScan\docs\TECHNICAL.md` L370

```
Per-frame breakdown (current):
  AI depth inference:    ~80ms   (GPU, DmlExecutionProvider)  ← bottleneck
  Depth-to-scan (LUT):  ~1ms    (CPU, numpy vectorized)
  EMA filter:            ~0.5ms  (CPU, ~650 bins)
  IMU processing:        ~0.1ms  (CPU)
  Ground calibration:    ~50ms   (one-time at startup)
  ──────────────────────────────
  Total:                ~82ms/frame = ~12 FPS
```

---

