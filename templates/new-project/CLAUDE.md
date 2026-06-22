# <專案名稱>

<一段話：這個專案做什麼、解決什麼問題>

## 架構與核心模組

<核心模組在哪、彼此怎麼接。例：>
- `<entrypoint>` — <進入點 / 主流程>
- `<core/>` — <核心邏輯>
- `<data flow>` — <資料怎麼流動>

## Build / Test

```bash
# 安裝
<install 指令，例：pip install -e . / npm install>

# 跑測試
<TEST_CMD>

# lint（如有）
<lint 指令>
```

## 反直覺的坑

<這個 repo 踩過的雷、AI 容易猜錯的 API、不能改的東西。沒有就先留空。>

---

## 修改規則（給 AI）

- **改前**：完整讀目標檔 + 所有 import 它的模組；不准假設 API，用 grep 確認簽名。
- **改中**：禁止 `# ...` 佔位註解；不省略未改動的程式（會截斷就用 Write 全量輸出）。
- **改後**：立刻跑 `<TEST_CMD>`；要看到全綠才繼續，失敗立刻停下修。
- **禁止**：未經要求重構能跑的程式、改既有資料結構欄位定義、擴大 scope。

> 機器強制：`.claude/settings.json` 的 PostToolUse hook 會在 Write/Edit/MultiEdit 後自動跑 `.claude/check.sh`，失敗（exit 1）就擋下這次改動。
