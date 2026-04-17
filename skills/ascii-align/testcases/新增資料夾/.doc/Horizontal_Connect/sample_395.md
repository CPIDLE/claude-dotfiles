## Sample 395

**Source**: `Reporter_v1\WORKSPACE\a01\19_Vision_Depth_Integration.md` L178

```
D435i (IR OFF)
  ├→ RGB ──→ SegFormer-B0 地板偵測
  ├→ RGB ──→ DA V2 深度校正（需 emitter pulse）
  └→ Depth ──→ 5 種 BEV 模式
       ├→ IPM（平面假設）
       ├→ Point Cloud（3D 投影）
       ├→ Hybrid（推薦：IPM 地板 + 深度物體）
       ├→ Dual IR
       └→ Vertical
```

---

