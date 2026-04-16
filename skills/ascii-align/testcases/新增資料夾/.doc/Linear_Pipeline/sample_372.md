## Sample 372

**Source**: `Reporter_v1\WORKSPACE\a01\07_TM-Program-Analysis-v0.md` L50

```
├── src/
│   ├── tm_flow_parser.py          # .flow 格式解析器
│   ├── tm_flow_analyzer.py        # Flow 分析
│   ├── tm_doc_generator.py        # 文件自動產生
│   ├── tm_analyze.py              # CLI 主程式
│   ├── tm_vision_analyzer.py      # 68 Vision Job XML 分析
│   ├── tm12_kinematics.py         # FK/IK 運動學
│   ├── tm_flow_editor.py          # MutableFlowDocument 語意編輯（Phase 2）
│   ├── tm_flow_simplifier.py      # 重複鏈偵測（Phase 2）
│   └── test_core.py               # 34 個測試
├── output/                        # 49 份自動產生分析文件
│   ├── INDEX.md
│   ├── MainFlow.md
│   ├── SUBFLOW_CALL_GRAPH.md
│   ├── VARIABLE_USAGE_MAP.md
│   ├── VISION_JOB_MAP.md
│   ├── VISION_SYSTEM_ANALYSIS.md
│   ├── DUPLICATE_ANALYSIS.md
│   ├── subflows/（37 個）
│   └── threads/（5 個）
├── docs/                          # 手動分析文件
│   ├── FLOW_ANALYSIS.md
│   ├── ERROR_CODE_REFERENCE.md
│   ├── POINT_DATA.md
│   └── HT_9046LS / MR_PORT 深度分析
├── data/                          # TM 解壓資料
├── archive/                       # TM 匯出壓縮
└── reviews/                       # 審核報告
```

