## Sample 184

**Source**: `opencode-bench\opencode-2026-04-07\RESULTS.md` L120

```
benchmarks/opencode-2026-04-07/
├── README.md, RESULTS.md (本檔), opencode.json
├── run_bench.sh         # 第一輪 driver
├── run_t2_retry.sh      # T2 修正後重跑
├── prompts/T1.md, T2.md, T2_inline.md
└── {gemini3-flash, gemma4-e2b, qwen25-14b, qwen25-16k}/
    ├── T1_log.txt, T1_meta.txt   # 全失敗
    ├── T2_log.txt, T2_meta.txt   # 第一輪（廢）
    └── T2_retry.txt, T2_retry_meta.txt  # 第二輪（有效）
```

