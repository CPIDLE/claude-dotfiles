## Sample 656

**Source**: `WebCamToLidarScan\docs\REQUIREMENTS.md` L963

```
時間軸 →

TensorRT stream:  [===推論===]
                             │
Scan stream:                 ├─ reset_scan_bins          (~0.001 ms)
                             ├─ depth_to_scan            (~0.2 ms)
                             ├─ apply_ema_filter         (~0.001 ms)  ← 新增
                             ├─ cudaStreamSynchronize
                             │
CPU:                         ├─ 讀 filtered_bins          (~0.001 ms)
                             ├─ ego-motion 合併（如啟用）  (~0.3 ms)   ← 新增
                             └─ 發布 LaserScan

單幀總延遲:
  無時間融合: ~0.3 ms
  +EMA:       ~0.3 ms（無感）
  +Ego-motion: ~0.6 ms（仍遠低於目標 3 ms）
```

---

