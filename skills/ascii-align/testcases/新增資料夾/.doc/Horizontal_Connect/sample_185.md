## Sample 185

**Source**: `opencode-bench\README.md` L67

```
opencode-bench/
├── SUMMARY.md                  # 全平台結果總表（快速參考）
├── RESULTS.md                  # 詳細結果 + 根因分析
├── collect_all.py              # 掃描 *_meta.txt --> xlsx 報告
├── fixtures/A3/                # A3 task fixture（mini_queue + TOCTOU bug）
├── fixtures/A4/                # A4 task fixture（thread-safe mini_queue）
├── three-way-2026-04-08/       # 共用 prompt 目錄（A1~A4）
├── a4-bench-2026-04-09/        # A4 全平台 benchmark
├── 4090-litellm-2026-04-09/    # 4090 LiteLLM benchmark（R1）
├── 4090-litellm-2026-04-09-r2/ # 4090 LiteLLM benchmark（R2）
├── dgx-spark-litellm-2026-04-09/ # DGX Spark benchmark
├── fix-proxy/                  # Ollama tool_calls index fix
│   ├── proxy.py                # HTTP streaming proxy（修正 index）
│   ├── bench_3way.sh           # 3-way bench script
│   ├── bench-3way-20260410-*/  # 3-way bench raw results
│   ├── retest-*/               # proxy retest raw results
│   └── batch_retest.sh         # batch retest script
├── a1-dual-file-test/          # A1 雙檔 bug 調查（6 variants x  2 platforms）
├── a1-repeat-4090/             # A1 重複測試（5 runs）
├── a1-repeat-dgx/              # A1 重複測試（5 runs）
└── HANDOFF.md                  # 交接文件
```

