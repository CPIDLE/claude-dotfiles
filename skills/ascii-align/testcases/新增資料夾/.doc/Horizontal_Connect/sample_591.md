## Sample 591

**Source**: `Reporter_v1\WORKSPACE\a07\opencode_enhance_history.md` L152

```
opencode-bench/
├── README.md                   # 專案概覽
├── RESULTS.md                  # 詳細結果 + 根因分析
├── SUMMARY.md                  # 全平台結果總表
├── BENCHMARK-REPORT.md         # 最終效能評測報告
├── ARCHITECTURE.md             # 系統架構說明
├── HANDOFF.md                  # 交接文件
├── 4090-SETUP.md               # RTX 4090 環境設定
├── 4090-DEPLOYMENT.md          # 部署提案（含成本分析）
├── collect_all.py              # 掃描 *_meta.txt --> xlsx（109 rows）
├── opencode_enhance_all_benchmarks.xlsx  # 全量 benchmark 報告
├── fixtures/                   # A3/A4 task fixtures
│
├── # ── Benchmark 腳本 ──
├── bench_4090_5runs.sh
├── bench_dgx.sh
├── bench_gemini_5runs.sh
├── bench_a5_5runs.sh / bench_a5_quick.sh
├── bench_stress.sh
├── run_a1_repeat.sh / run_a1_extra.sh
│
├── # ── 結果目錄（按平台x 日期）──
├── opencode-2026-04-07/        # 最初測試
├── three-way-2026-04-08/       # 早期三方對照
├── 4090-2026-04-08/
├── 4090-real-2026-04-08/
├── dgx-spark-2026-04-08/
├── gemini-3way-2026-04-08/
├── 4090-ollama-2026-04-09/     # 直連 Ollama（全滅）
├── 4090-litellm-2026-04-09/    # LiteLLM R1
├── 4090-litellm-2026-04-09-r2/ # LiteLLM R2
├── dgx-spark-litellm-2026-04-09/
├── a4-bench-2026-04-09/        # A4 專題
├── a1-dual-file-test/          # A1 雙檔 bug 調查
├── a1-repeat-4090/ + a1-repeat-dgx/  # A1 重複測試
├── fix-proxy/                  # Ollama index bug 修復 + retest
│   ├── proxy.py
│   ├── bench_3way.sh
│   └── bench-3way-20260410-*/
├── 4090-5runs-20260410-*/      # 5-run 穩定性
├── dgx-5runs-20260410-*/
├── gemini-5runs-20260410-*/
├── a5-5runs-20260410-*/
├── a5-quick-20260410-*/
└── stress-20260410-*/          # 壓力測試
```

