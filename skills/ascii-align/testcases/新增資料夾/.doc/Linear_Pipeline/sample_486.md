## Sample 486

**Source**: `Reporter_v1\WORKSPACE\a04\00_REVIEW.md` L377

```
input.md (Markdown 報告)
    │
    ▼
gen_gyro_pptx.py (解析器)
    │
    ▼
Slide Plan 生成（共享）
  └─ 投影片序列、內容規劃
    │
    ├──────────────┬──────────────┐
    │                              │
Marp 引擎（高品質）          python-pptx 引擎（可編輯）
    ├─ {prefix}_marp.md           ├─ 直接寫 PPTX
    ├─ Marp CLI                   ├─ GYRO 品牌樣式注入
    └─ {prefix}_marp.pptx/PDF     └─ {prefix}_editable.pptx
```

---

