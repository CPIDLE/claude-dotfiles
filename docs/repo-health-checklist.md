# Repo 健檢清單（AI 輔助開發 7 項）

> `/pm` 開工健檢與 `/pm health` 的 yardstick。蒸餾自 Gyro 團隊 AI 使用 Review（2026-06）。
> 來源全文：`E:\github\TSC_GBD_V0\.docs\AI_SELF_CHECKUP.md`。
> 完整 portfolio 體檢報告：`docs/ai-self-checkup-2026-06-22.md`。

每項評 ✓=2 / △=1 / ✗=0，滿分 14。檢查用唯讀指令，**預設不改檔**。

| # | 項目 | 查法（唯讀） | ✓ | △ | ✗ |
|---|---|---|---|---|---|
| 1 | 權限衛生 | `git ls-files \| grep -i settings.local.json` | 無結果（已 ignore 或無此檔） | — | 有結果＝誤入版控 |
| 2 | 權限不過寬 | 讀 `.claude/settings.local.json` 的 `allow` | 無萬用條目 | 少數寬鬆（`python -c *`/`pip install *`） | 危險萬用（`rm *`/`Bash(*)`） |
| 3 | 上下文檔 | 根目錄 `CLAUDE.md` 在否、是否非 /init 樣板 | 有實質內容 | 薄/樣板/僅 README | 無 |
| 4 | 行為契約 | `CLAUDE.md`/`AGENTS.md` 是否含「修改規則」 | 齊全（改前讀+grep/改後測/禁佔位/不重構） | 部分 | 無 |
| 5 | 機器強制 | `.claude/settings.json` 有 PostToolUse(Write\|Edit\|MultiEdit) 跑 lint/test | 有 | 有 hook 但非 lint/test | 無 |
| 6 | 測試門檻 | 有測試（`test_*`/`*_test`/`tests/`）+ 契約寫「綠燈才算」 | 兩者皆有 | 只有其一 | 皆無 |
| 7 | 揭露與機密 | trailer 一致；`.env`/金鑰沒進版控（`git ls-files \| grep -E '\.env$'`） | 皆乾淨 | 小問題（trailer 混用/gitignore 缺防護） | 機密外洩 |

## 分數帶

```
12-14  健康   有護欄，維持即可
 8-11  及格   挑 1-2 項補強（多半缺 hook 或行為契約）
 4-7   待補   規則多靠自律，先補第 4、5 項
 0-3   裸奔   先做第 1、2 項（資安），再補文件與契約
```

## 優先序

- **資安項（1 / 2 / 7）有 ✗ → 立刻處理**：誤入版控的 `settings.local.json`、`.env`/金鑰外洩、萬用權限。
- **品質項（3 / 4 / 5 / 6）**：用 `/pm health` 同意後一鍵 scaffold 補上（CLAUDE.md + .gitignore + `.claude/` hook）。

> 補強模板：`~/.claude/templates/new-project/`（`/pm new` 與 `/pm health` 共用同一份）。
