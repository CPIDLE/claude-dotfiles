## Sample 537

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\TM_UR\04_UR_Program_Analysis_v0.md` L47

```
├── src/
│   ├── ur_script_parser.py       # URScript 解析器
│   ├── ur_tree_parser.py         # 樹狀結構解析
│   ├── ur_project_loader.py      # 專案載入器
│   ├── ur_flow_analyzer.py       # Flow 分析
│   ├── ur_doc_generator.py       # 文件自動產生
│   ├── ur_analyze.py             # CLI 主程式
│   ├── ur_flow_editor.py         # 語意級腳本編輯（Phase 2）
│   ├── ur_flow_simplifier.py     # 跨檔案重複偵測（Phase 2）
│   ├── ur30_kinematics.py        # FK 驗證 + Rodrigues（Phase 2）
│   ├── ur_script_editor.py
│   ├── ur_script_simplifier.py
│   ├── test_core.py              # 31 個測試
│   ├── test_phase2.py            # 15 個測試
│   └── test_refactor.py
├── K11_UR30_Project/programs/    # UR 程式原始檔（160+ 檔案）
├── output/                       # 自動產生的 82 份分析文件
├── docs/                         # 手動撰寫的分析文件
│   ├── FLOW_ANALYSIS.md
│   ├── ERROR_CODE_REFERENCE.md
│   ├── POINT_DATA.md
│   ├── PHASE2_SPEC.md
│   └── gRPC/                    # GYRO gRPC 整合資料
└── archive/                      # UR 匯出壓縮
```

---

