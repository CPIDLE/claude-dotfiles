# AI 輔助開發 · Portfolio 自我體檢報告

> 日期：2026-06-22
> 受測範圍：`E:\github\` 下由 CPIDLE + CC 產生的 git repos（共 30 個）
> 依據：`E:\github\TSC_GBD_V0\.docs\AI_SELF_CHECKUP.md`（Gyro 團隊 AI 使用 Review 收斂的 7 項自查）
> 方法：6 個平行 agent 唯讀檢查，分數逐列人工重算（subagent 加總有 9 筆算錯，已修正）

---

## 範圍

**納入（30 個 CPIDLE 自有 git repo）**：AnnSinHome_v0、Chat_bot_v1、Claude_CAD_v0/v1、Claude_code_leak_v0、D435I_LidarScan_v1、D435i_LidarScan、D435i_LidarScan_v2/v3/v3a、D435i_PiBridge_v0、D455_LidarScan、D455_LidarScan_v0、HaloScan_v0、Line_bot_v0、Mail_Checker_v0、ServerAgent_v0/v0b、StockSage_v0、WebCamToLidarScan、ascii-tools、claude-dotfiles、claude_bbs_v0、hacker_v0、opencode-bench、opencode_enhance_v0、personal-rag、personal-rag_v2、virtual-system_v0、win_drive_v0

**排除**：
- 團隊分析類（非自有產出）：AMRCoolDown_v0、TSC_GBD_V0、TM_Program_Analysis_v0、UR_Program_Analysis_v0
- 外部 repo / fork：Claude-Code-Agent-Monitor、GenCAD_ref、opencode、ai-sdk-fix
- 非 git 資料夾：ArmScan_v0、Reporter_v0/v1、draft-forge、Omniverse_v0、claude_Editor_v0 等約 12 個

---

## 7 項評分標準

| # | 項目 | 查什麼 |
|---|---|---|
| 1 | 權限衛生 | `.claude/settings.local.json` 沒進版控 |
| 2 | 權限不過寬 | allowlist 沒有 `Bash(python)`、`Bash(rm *)` 之類萬用條目 |
| 3 | 上下文檔 | 根目錄有 `CLAUDE.md` 且非 /init 樣板 |
| 4 | 行為契約 | 有「改前讀+grep／改後必測／禁佔位／不重構」改扣流程規則 |
| 5 | 機器強制 | `.claude/settings.json` 有 `PostToolUse` hook 跑 lint/test |
| 6 | 測試門檻 | 有測試 + 契約寫明「綠燈才算」 |
| 7 | 揭露與機密 | `Co-Authored-By` trailer 一致、`.env`/金鑰沒外洩 |

評分：✓=2 ｜ △=1 ｜ ✗=0 ｜ 滿分 14
分數帶：12-14 健康 ｜ 8-11 及格 ｜ 4-7 待補 ｜ 0-3 裸奔

---

## 體檢總表（依分數排序）

| Repo | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 分數 |
|---|---|---|---|---|---|---|---|---|
| opencode_enhance_v0 | ✓ | ✓ | ✓ | ✓ | △ | ✓ | △ | **12** ✅健康 |
| ServerAgent_v0 | ✓ | ✓ | ✓ | △ | ✗ | △ | ✓ | 10 |
| ServerAgent_v0b | ✓ | ✓ | ✓ | △ | ✗ | △ | ✓ | 10 |
| Claude_code_leak_v0 | ✓ | ✓ | △ | ✓ | ✗ | △ | ✓ | 10 |
| D455_LidarScan | ✓ | △ | ✓ | △ | ✗ | △ | ✓ | 9 |
| D435i_LidarScan | ✓ | △ | ✓ | ✗ | ✗ | △ | ✓ | 8 |
| D435i_LidarScan_v2 | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ | ✓ | 8 |
| D435i_PiBridge_v0 | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ | ✓ | 8 |
| claude-dotfiles | ✓ | ✓ | △ | ✗ | △ | ✗ | ✓ | 8 |
| AnnSinHome_v0 | ✓ | ✓ | ✗ | ✗ | ✗ | △ | ✓ | 7 |
| Claude_CAD_v1 | ✓ | ✓ | ✗ | ✗ | △ | ✗ | ✓ | 7 |
| D435I_LidarScan_v1 | ✓ | △ | △ | ✗ | ✗ | △ | ✓ | 7 |
| D435i_LidarScan_v3a | ✓ | ✓ | ✗ | ✗ | ✗ | △ | ✓ | 7 |
| StockSage_v0 | ✓ | ✓ | ✗ | ✗ | ✗ | △ | ✓ | 7 |
| opencode-bench | ✓ | ✓ | ✗ | ✗ | ✗ | △ | ✓ | 7 |
| personal-rag_v2 | ✓ | ✓ | ✗ | ✗ | ✗ | △ | ✓ | 7 |
| virtual-system_v0 | ✓ | ✓ | ✗ | ✗ | ✗ | △ | ✓ | 7 |
| Chat_bot_v1 | ✓ | ✓ | ✗ | ✗ | ✗ | △ | △ | 6 |
| Claude_CAD_v0 | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✓ | 6 |
| D435i_LidarScan_v3 | ✓ | △ | ✗ | ✗ | ✗ | △ | ✓ | 6 |
| D455_LidarScan_v0 | ✓ | △ | ✗ | ✗ | ✗ | △ | ✓ | 6 |
| HaloScan_v0 | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✓ | 6 |
| Mail_Checker_v0 | ✓ | ✓ | △ | ✗ | ✗ | ✗ | △ | 6 |
| WebCamToLidarScan | ✓ | △ | ✗ | ✗ | ✗ | △ | ✓ | 6 |
| ascii-tools | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✓ | 6 |
| hacker_v0 | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✓ | 6 |
| personal-rag | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✓ | 6 |
| win_drive_v0 | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✓ | 6 |
| Line_bot_v0 | ✓ | △ | ✗ | ✗ | ✗ | ✗ | ✓ | 5 |
| claude_bbs_v0 | ✗ | ✓ | ✗ | ✗ | ✗ | △ | △ | 4 |

**分數分布**：健康 1 ｜ 及格 8 ｜ 待補 21 ｜ 裸奔 0 ｜ 平均 **7.1/14**

整體守得住資安底線（無裸奔），但卡在「待補」——多半不是做不好，是還沒設規則。

---

## 系統性弱點（30 repo 共通）

### 第 5 項 機器強制 hook — 幾乎全軍覆沒
沒有任何一個 repo 有跑 lint/test 的 `PostToolUse` hook。最接近的 claude-dotfiles 只跑 `index-append.py`、opencode_enhance 只有 commit 署名 hook（都記 △）。**這是整個 portfolio 最大的單一缺口**——所有「改後必測」都只靠自律。

### 第 4 項 行為契約 — 規則沒跟著 repo 走
改扣流程規則（改前讀+grep／改後必測／禁佔位／不重構）只住在全域 `~/.claude/CLAUDE.md`。一旦 repo 被 clone、分享、或雲端 agent 接手，這些規則就消失。只有 opencode_enhance、Claude_code_leak（AGENTS.md）真正把契約寫進 repo。

### 第 3 項 CLAUDE.md — 半數沒有
有寫的多半是硬體/scan 類（D435i、D455、PiBridge、ServerAgent）；工具/RAG/雜項類（personal-rag、ascii-tools、hacker、win_drive、StockSage、Mail_Checker…）幾乎都只有 README，AI 進來要重新猜架構。

---

## 資安處理紀錄（2026-06-22 已完成）

體檢時發現 4 項版控衛生風險，當日已全數止血：

| Repo | 風險 | 處理 | 狀態 |
|---|---|---|---|
| opencode_enhance_v0 | 工作目錄缺 `.gitignore`，untracked `.env`/`CREDENTIALS.md`（明碼密碼 `eggs123`、admin endpoint、LiteLLM `sk-1234`），`git add .` 會全帶入 | 還原 origin `.gitignore` + 補 `CREDENTIALS.md`、`.playwright-mcp/` | ✅ 止血（無 commit，本機 HEAD unborn；origin 從未洩漏，不需輪換金鑰） |
| HaloScan_v0 | `.claude/settings.local.json` 已誤入版控 | `git rm --cached` + gitignore 補 `.claude/settings.local.json`，commit `d095faa` | ✅ 已移出版控 |
| claude_bbs_v0 | 巢狀 `spike/s5-sandbox/.claude/settings.local.json` 已誤入版控 | `git rm --cached` + gitignore 補 `**/.claude/settings.local.json`，commit `97d054e` | ✅ 已移出版控 |
| D435i_LidarScan_v3 | gitignore 沒擋 `.claude/` 也沒擋 `.env`（未爆彈） | gitignore 補兩條，commit `bbc80f6` | ✅ 預防 |

> 三筆 commit 為本機，尚未 push。

---

## Top 3 最划算的下一步（全 portfolio）

| 優先 | 動作 | 效果 |
|---|---|---|
| 1 | 做一份共用 `.gitignore` + `PostToolUse` hook 樣板，掃過 30 個 repo 統一鋪上 | 一次補滿第 1、5 項，把第 5 項從全✗拉到全✓ |
| 2 | 把全域 CLAUDE.md 的「修改規則」段抽成 snippet，貼進每個 repo 的 CLAUDE.md | 補第 4 項，規則跟著 repo 走 |
| 3 | 替沒有 CLAUDE.md 的 ~15 個 repo 各補一份（架構+build/test+坑） | 補第 3 項 |

---

*非強制建議。本報告為單次快照（2026-06-22），repo 狀態會隨開發變動。*
