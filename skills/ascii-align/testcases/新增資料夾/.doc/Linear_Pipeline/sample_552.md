## Sample 552

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版.md` L179

```
  ① 粗定位（手動/搖桿）
        │
       ▼
  ② 高解析相機拍照
        │
       ▼
  ③ 計算偏差 dX / dY / dR
        │
       ▼
  ④ 自動補償運動         ←── 重複直到 delta ≤ 容差
        │
       ▼
  ⑤ 最終作業 (精度 ≤ 0.05mm)
```

---

