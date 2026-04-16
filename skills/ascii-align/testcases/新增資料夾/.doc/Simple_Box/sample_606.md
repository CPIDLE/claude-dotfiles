## Sample 606

**Source**: `StockSage_v0\rl\ARCHITECTURE.md` L50

```
rl/
├── config.py       # 超參數（reward、PPO、walk-forward）
├── env.py          # TradingEnv -- Gymnasium 環境
├── policy.py       # TransformerFeaturesExtractor（實驗用，目前未啟用）
├── trainer.py      # RLTrainer -- Walk-Forward PPO 訓練
├── predictor.py    # get_rl_prediction() -- 推論
└── evaluate.py     # ModelComparator -- RL vs Transformer 比較
```

