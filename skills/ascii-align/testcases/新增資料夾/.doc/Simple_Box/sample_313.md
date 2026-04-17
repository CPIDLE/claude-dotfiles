## Sample 313

**Source**: `Reporter_v0\.data\doc-report_詳細實作設計.md` L172

```
  搜尋階段            工具              目標
  ─────────          ─────             ──────
  2A. 索引掃描       Read _index.json   快速篩選相關文件 (< 1 min)
  2B. 同客戶搜尋     Grep/Glob          找歷史案例 (< 1 min)
  2C. 同產業搜尋     Read .txt files    找類比案例 (2-5 min)
  2D. 產品規格       Read .txt files    找產品參數 (2-5 min)
  2E. 報價參考       Grep 70_業務報價    歷史報價區間 (< 1 min)
```

---

