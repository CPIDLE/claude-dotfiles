## Sample 565

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版_0.md` L179

```
  1  粗定位（手動/搖桿）
        │
       v 
  2  高解析相機拍照
        │
       v 
  3  計算偏差 dX / dY / dR
        │
       v 
  4  自動補償運動         <─── 重複直到 delta <= 容差
        │
       v 
  5  最終作業 (精度 <= 0.05mm)
```

