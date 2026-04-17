## Sample 651

**Source**: `WebCamToLidarScan\docs\REQUIREMENTS.md` L301

```
桌面 GPU (RTX 4090):
  CPU RAM ←── PCIe 4.0 (32 GB/s) ──→ GPU VRAM (24GB)
  → 必須顯式 cudaMemcpy，延遲高

Jetson Thor:
  ┌──────────────────────────────────────┐
  │   128 GB LPDDR5X 統一記憶體            │
  │   (273 GB/s 頻寬)                     │
  │                                      │
  │   CPU 可存取 ◄──────► GPU 可存取       │
  │   同一塊實體記憶體，無需拷貝             │
  └──────────────────────────────────────┘
  → cudaMallocManaged / 零拷貝映射直接共享
```

---

