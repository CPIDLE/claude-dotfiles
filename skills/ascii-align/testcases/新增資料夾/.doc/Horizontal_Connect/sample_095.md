## Sample 095

**Source**: `D435i_LidarScan\FLOW.md` L649

```
600x600 black image, camera at center (300, 300)

┌──────────────────────────────────┐
│  FPS: 14.0  NS: 70ms            │
│  Model: Hokuyo UST-10LX         │
│  Height: 0.1m ~ 1.8m            │
│  Points: 87/1081                 │
│  Min range: 0.45m                │
│  Ground: 45/348 | 42/348        │  ← (when --ground-scan)
│       ╱╱                         │
│      ╱╱  D435i FOV (yellow)      │
│     ╱╱                           │
│   ╱  · ·                         │
│  ╱ ·     ·   ← green dots       │
│ ╱  · · · ·     (obstacles)      │
│╱     ◉  ← camera (yellow dot)   │
│╲                                 │
│ ╲                                │
│  ╲   LiDAR FOV (dark blue)      │
│     ○───○───○  range circles     │
│    1m  2m  3m                    │
│                                  │
│  D435i FOV  LiDAR FOV           │
│  D435i -> Hokuyo UST-10LX       │
└──────────────────────────────────┘

NS: neural stereo inference latency (shown when --neural-stereo)
```

---

