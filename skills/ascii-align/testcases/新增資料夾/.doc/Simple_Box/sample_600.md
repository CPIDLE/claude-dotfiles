## Sample 600

**Source**: `StockSage_v0\docs\ARCHITECTURE.md` L448

```
1. 檢查是否為交易日（跳過週末 & 台股假日）
2. 更新全球 + 台灣市場資料
3. 回填昨日實際結果
4. 執行預測（Transformer 或 RL，依 STOCKSAGE_USE_RL）
5. 寫入 prediction_log
6. 組成 HTML Email：
   ├─ 昨日回顧（實際 vs 預測）
   ├─ 今日訊號（動作 + 機率分布）
   ├─ GMP 全球展望（選用）
   └─ 近期準確率統計
7. 透過 Gmail SMTP 寄送
```

