## Sample 106

**Source**: `D435i_LidarScan\REPORT_v3_depth_compensation.md` L450

```
┌────────────────────────────────────────────────────────────────────┐
│ Depth Source Priority                                              │
│                                                                    │
│ 1. --neural-stereo 啟用？                                          │
│    YES → Built-in stereo (priority) + CREStereo (fill)            │
│          → ~100% coverage                                          │
│          → emitter 強制 OFF                                        │
│          → 地面點合成停用                                           │
│                                                                    │
│ 2. --emitter OFF？                                                 │
│    YES → Built-in stereo (~11%) + 地面點合成 (color segmentation)  │
│          → 有色地板區域補點                                         │
│                                                                    │
│ 3. --emitter ON                                                    │
│    → Built-in stereo (~62%) 直接使用                               │
│    → 最簡單，但半導體廠不可用                                      │
└────────────────────────────────────────────────────────────────────┘
```

---

