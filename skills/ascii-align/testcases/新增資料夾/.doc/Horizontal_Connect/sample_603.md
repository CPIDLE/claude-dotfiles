## Sample 603

**Source**: `StockSage_v0\README.md` L191

```
StockSage_v0/
├── run.py                        # 唯一入口（所有 CLI 指令）
├── config.py                     # 全域設定
├── requirements.txt
│
├── db/
│   └── schema.py                 # SQLAlchemy ORM
│
├── fetchers/
│   ├── base.py                   # 重試、upsert、日誌
│   ├── us_market.py              # yfinance：全球指數
│   └── tw_market.py              # FinMind：台股籌碼
│
├── pipeline/
│   ├── model.py                  # Transformer Encoder
│   ├── feature_builder.py        # 特徵組裝 + TAIEX 技術指標
│   ├── auto_trainer.py           # Walk-Forward 訓練
│   └── weekly_runner.py          # 每日預測主流程
│
├── rl/                           # 強化學習模組
│   ├── config.py                 # RL 超參數
│   ├── env.py                    # Gymnasium TradingEnv
│   ├── policy.py                 # Transformer feature extractor for SB3
│   ├── trainer.py                # Walk-Forward PPO 訓練
│   ├── predictor.py              # RL 推論
│   └── evaluate.py               # RL vs Transformer 比較
│
├── gmp/                          # Global Market Predictor
│   ├── config.py                 # GMP 設定
│   ├── fetcher.py                # 全球市場資料抓取
│   ├── feature_engineer.py       # 48 維特徵工程
│   ├── trainer.py                # LightGBM 訓練
│   └── predictor.py              # 週/月報酬率預測
│
├── scripts/
│   ├── daily_predict_email.py    # 每日 Email（完整 pipeline + 昨日回顧）
│   ├── run_daily.bat             # Task Scheduler 執行用 wrapper
│   └── setup_schedule.bat        # 排程安裝腳本
│
├── backtest/
│   └── gap_backtest.py           # 夜盤結算→開盤跳空回測
│
└── models/
    ├── stocksage_model.pt        # Transformer 模型權重
    ├── model_meta.pkl            # Transformer 訓練 metadata
    ├── rl_ppo_agent.zip          # RL PPO agent
    ├── rl_meta.pkl               # RL 訓練 metadata
    └── gmp_model.pkl             # GMP LightGBM 模型
```

---

