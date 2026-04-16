## Sample 604

**Source**: `StockSage_v0\README_DEV.md` L9

```
yfinance (全球指數)  -->  daily_features (DB)  ──┐
FinMind (台股籌碼)   -->  daily_features (DB)  ──┤  前 5 天
yfinance (^TWII)    -->  TAIEX 技術指標 (記憶體) ┘  [5, 30]
                                                    v 
                                             Transformer
                                                    v 
                                     {下跌, 持平, 上漲} 機率
```

