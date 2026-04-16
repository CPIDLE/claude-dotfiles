## Sample 601

**Source**: `StockSage_v0\docs\ARCHITECTURE.md` L486

```bash
# ─── 日常操作 ───
python run.py                              # 每日預測（預設）
python run.py --status                     # 資料庫 & 模型狀態

# ─── 初始化 & 訓練 ───
python run.py --init                       # 首次：全量建庫 + 訓練
python run.py --train                      # 強制重訓 Transformer
python run.py --train-until DATE           # 訓練資料截止日

# ─── RL 引擎 ───
python run.py --rl-train                   # 訓練 PPO agent
python run.py --rl-predict                 # 單次 RL 預測
python run.py --rl-compare                 # RL vs Transformer 比較
python run.py --rl-compare --oos           # 僅樣本外比較

# ─── GMP ───
python run.py --gmp-init                   # 初始化 + 訓練 GMP
python run.py --gmp-train                  # 重訓 GMP
python run.py --gmp-predict                # GMP 預測

# ─── 回測 ───
python run.py --backtest                   # 小台，全樣本
python run.py --backtest --contract full   # 大台
python run.py --backtest --oos             # 僅樣本外
python run.py --backtest --start-date DATE # 指定起始日
python run.py --backtest --no-confidence-filter
```

