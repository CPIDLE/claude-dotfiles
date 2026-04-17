## Sample 653

**Source**: `WebCamToLidarScan\docs\REQUIREMENTS.md` L555

```
時間軸 →

TensorRT stream:  [===推論===]
                              │ cudaEventRecord(trt_done)
                              ▼
Scan stream:                  │ cudaStreamWaitEvent(trt_done)
                              │
                              ├─ reset_scan_bins <<<1,256>>>        (~0.001 ms)
                              │
                              ├─ depth_to_scan <<<(20,60),(32,8)>>> (~0.2 ms)
                              │
                              ├─ cudaStreamSynchronize              (~0.01 ms)
                              │
                              └─ CPU: 讀 scan_bins (統一記憶體)      (~0.001 ms)
                                 → 填入 LaserScan message
                                 → 發布到 /virtual_scan

單幀總延遲: ~0.3 ms（不含 TensorRT 推論）
```

---

