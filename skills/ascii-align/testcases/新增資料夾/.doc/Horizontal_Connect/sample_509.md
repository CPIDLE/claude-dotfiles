## Sample 509

**Source**: `Reporter_v1\WORKSPACE\a04\08_Reporter_v1.md` L30

```
input.md (Markdown 報告)
    │
    v 
gen_gyro_pptx.py (解析器)
    │
    ├─ Slide Plan 生成
    │  (投影片序列、內容規劃)
    │
    ├─ Marp 引擎 (高品質)
    │  --> {prefix}_marp.md (中間格式)
    │  --> Marp CLI (marp-cli)
    │  --> {prefix}_marp.pptx / PDF
    │
    └─ python-pptx 引擎 (可編輯)
       --> {prefix}_editable.pptx
```

