## Sample 602

**Source**: `StockSage_v0\docs\ARCHITECTURE.md` L575

```
StockSage_v0/
├── run.py                     # 主入口 CLI
├── config.py                  # 全域設定
├── pipeline/                  # Transformer 引擎
│   ├── model.py               #   StockTransformer 模型
│   ├── feature_builder.py     #   特徵工程
│   ├── auto_trainer.py        #   訓練（WF-CV）
│   ├── daily_update.py        #   每日資料更新
│   └── weekly_runner.py       #   推論 & 排程
├── rl/                        # RL PPO 引擎
│   ├── env.py                 #   TradingEnv (Gymnasium)
│   ├── policy.py              #   Policy 網路定義
│   ├── config.py              #   RL 超參數
│   ├── trainer.py             #   訓練（平行 WF-CV）
│   ├── predictor.py           #   推論
│   └── evaluate.py            #   模型比較工具
├── gmp/                       # GMP 全球市場預測
│   ├── feature_engineer.py    #   50+ 維特徵
│   ├── model.py               #   LightGBM 週/月模型
│   ├── predictor.py           #   預測
│   └── trainer.py             #   訓練
├── fetchers/                  # 資料擷取
│   ├── us_market.py           #   美股 & 全球（yfinance）
│   └── tw_market.py           #   台灣法人（FinMind）
├── backtest/                  # 回測
│   └── gap_backtest.py        #   隔夜跳空策略
├── db/                        # 資料庫
│   ├── schema.py              #   SQLAlchemy schema
│   └── stocksage.db           #   SQLite 資料檔
├── scripts/                   # 排程腳本
│   ├── daily_predict_email.py #   每日 Email 管線
│   ├── run_daily.bat          #   Windows 排程用
│   └── setup_schedule.bat     #   建立排程
├── models/                    # 訓練好的模型（gitignored）
├── docs/                      # 文件
└── .env                       # 環境變數（gitignored）
```

