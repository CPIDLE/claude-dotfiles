## Sample 658

**Source**: `WebCamToLidarScan\README.md` L15

```
深度圖 (640×480)
    │
    ├─ 啟動時一次 ─→ RANSAC 地平面校正 → 建立 LUT
    │
    └─ 每幀執行 ──→ 逐像素: 查 LUT → 高度過濾 → 角度分割 → 取最近點
                                                              │
                                                              ▼
                                                   Raw LaserScan (~650 bins)
                                                              │
                                              ┌───────────────┼───────────────┐
                                              │ (可選)         │ (可選)         │
                                              ▼               ▼               ▼
                                           EMA 濾波     中位數濾波    Ego-motion
                                          (自適應平滑)  (抗異常值)    多幀拼接
                                              │               │          (擴展 FOV)
                                              └───────────────┼───────────────┘
                                                              ▼
                                                     LaserScan 發布
```

---

