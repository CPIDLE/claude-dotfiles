## Sample 381

**Source**: `Reporter_v1\WORKSPACE\a01\12_StockSage_v0.md` L50

```
├── pipeline/
│   ├── daily_update.py       # 每日資料更新
│   ├── feature_builder.py    # 特徵工程
│   ├── model.py              # Transformer model
│   ├── auto_trainer.py       # 自動訓練
│   └── weekly_runner.py      # 週排程
├── fetchers/
│   ├── tw_market.py          # 台股資料
│   └── us_market.py          # 美股資料
├── gmp/                      # Global Market Predictor
│   ├── predictor.py
│   ├── trainer.py
│   ├── model.py              # LightGBM
│   ├── feature_engineer.py
│   ├── fetcher.py
│   └── symbols.py            # ~55 tickers
├── backtest/
│   └── gap_backtest.py       # 回測
├── scripts/
│   ├── daily_predict_email.py   # 每日信件
│   ├── run_daily.bat            # Windows 排程
│   └── setup_schedule.bat       # Task Scheduler 設定
├── config.py
├── db/schema.py
├── docs/TRADING_GUIDE.md
├── README.md / README_DEV.md
└── reviews/
```

