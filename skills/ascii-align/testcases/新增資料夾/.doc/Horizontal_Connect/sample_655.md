## Sample 655

**Source**: `WebCamToLidarScan\docs\REQUIREMENTS.md` L707

```
                        v1 路徑（冗餘）
                    ┌─ Depth Image → PointCloud2 ─→ virtual_lidar_node
Depth Anything V3 ─┤
(TensorRT)          └─ Depth Image ─────────────────→ virtual_lidar_node
                        v2 路徑（直接）
```

---

