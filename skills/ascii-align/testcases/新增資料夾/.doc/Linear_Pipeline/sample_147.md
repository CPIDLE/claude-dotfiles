## Sample 147

**Source**: `HaloScan_v0\docs\07_UAM-05LP_設定檔解析.md` L30

```
<?xml version="1.0" encoding="UTF-8"?>
<UAMProjectDesigner>
  └── <Areas>
        ├── <Area Type="NormalArea|ReferenceArea" Id="1">
        │     ├── <AreaComment>        — 區域備註（最大 64 字元）
        │     ├── <ScanSkipCount>      — 掃描跳過次數（0~3，0 = 每圈都檢查）
        │     └── <Regions>
        │           ├── <Region Type="Warning1">      — 外層警告區
        │           │     ├── <Points>   — 1081 個徑向距離值（mm）
        │           │     └── <Vertices> — 多邊形控制點索引
        │           ├── <Region Type="Warning2">      — 內層警告區
        │           │     ├── <Points>
        │           │     └── <Vertices>
        │           └── <Region Type="Protection1">   — 保護區（急停）
        │                 ├── <OnDelay>  — 觸發延遲（掃描次數，1次=30ms）
        │                 ├── <OffDelay> — 解除延遲（掃描次數，1次=30ms）
        │                 ├── <MinDetectionWidth> — 最小偵測寬度（僅新韌體）
        │                 ├── <Points>
        │                 └── <Vertices>
        ├── <Area Type="NormalArea" Id="2">
        │     └── （同上結構）
        └── <Area Type="NormalArea" Id="4">
              └── （同上結構）
```

---

