# Cross-Session Messaging — Design Discussion

**Status**: 討論 / 未實作
**Date**: 2026-04-21
**Context**: 探討在 Claude Code 兩個 live session 之間傳訊息的可行方案。

## 問題

> 有沒有辦法從 session A「即時 push」訊息到 session B？

## 為什麼「真．即時 push」做不到

1. **Session 沒有常駐 inbox** — 每個 `claude` CLI 是一條 user ↔ model 的輪詢對話。沒有 server 端 socket 在背景聽「別的 session 推來的訊息」。
2. **Turn-based 協議** — Anthropic API 是 request/response，model 回完就「靜止」。沒有外部 interrupt/inject 的通道；要下一輪只能等 user 送 prompt 或 hook 觸發。
3. **沒有 broker** — Claude Code 本身不內建 message bus（無 pubsub / websocket / shared queue）。兩個 session 之間唯一共用面是**檔案系統**和**外部服務**。
4. **Session 隔離是安全設計** — 跨 session 任意 push 會是 prompt-injection / confused-deputy 的攻擊面；model 無法驗證訊息真的是自己另一個 session 送的。

所以剩下的是「偽即時」：靠 session 自己**主動定時或被動觸發**去讀檔。

## 替代方案矩陣

| 方案 | 延遲 | LLM tokens 成本 | 自動反應？ | 備註 |
|---|---|---|---|---|
| **UserPromptSubmit hook** | ≈0s（user 打字瞬間） | 0（只跑 bash） | ❌ 需要 user 動作 | 最便宜，不 autonomous |
| **SessionStart hook** | 開 session 瞬間 | 0 | ❌ 只一次 | 接續用 |
| **`/loop 65s` 驅動 skill** | 65s ± | 每 tick 都有 LLM 呼叫成本 | ✅ 完全自動 | 燒 quota，即使 inbox 空也花錢 |
| **背景 bash poller + hook** | poll 65s → user 下次打字 | 0（poll 不燒）+ hook 0 | ⚠️ 半自動 | 最經濟，適合大多數情況 |
| **`CronCreate` remote trigger** | 依 cron | 遠端 agent 成本 | ✅ | 需 remote agent 基建 |
| **外部 webhook / PushNotification** | 視網路 | 0 | ❌ 只通知人 | 通知 User，不通知 model |

`ScheduleWakeup` 的 clamp 是 [60, 3600] 秒，所以 `/loop` 最短 ~60s。

## 推薦架構（分階段）

### 階段 1：零成本版（/pm 入場自動啟）

**觸發**：`/pm` skill 結束時自動 spawn 一個背景 bash poller。

**mailbox 結構**：
```
~/.claude/sessions/
├── registry.json                  # { session_id: { started_at, project, last_seen } }
└── inbox/
    └── <session-id>/
        ├── <timestamp>-<uuid>.json   # { from, type, payload }
        └── processed/                # 已讀的移到這裡（可 GC）
```

**元件**：
1. `~/.claude/bin/mailbox-poll.sh` — 背景 bash loop，每 65s 掃自己的 inbox，有訊息就寫到 `~/.claude/sessions/pending-<session-id>.md`
2. `~/.claude/hooks/mailbox-inject.sh` — `UserPromptSubmit` hook，user 打字前讀 pending 檔，把內容輸出到 stdout（Claude 會當 system-reminder 注入），然後刪除 pending
3. `~/.claude/bin/mailbox-send.sh <target-id> <payload>` — helper：atomic 寫一個 `.json.tmp` 再 `mv` 到 `inbox/<target-id>/`

**流程**：
- A session 跑 `mailbox-send.sh B-id "hello"` → 檔案出現在 B 的 inbox
- B 的背景 poller 60-65s 後掃到、寫 pending
- B 下次 user 打任何字，hook 注入 pending → model 看到「收到訊息：hello」→ 反應

**延遲**：平均 30s + 下次 user 互動。

### 階段 2：Autonomous 升級（選用）

若要「不等 user 就反應」，在階段 1 上加：
- `/mailbox-react` skill — 單次讀 pending 檔、呼叫必要 tools、回報
- `/pm` 結束時若偵測到 `autonomous=true` flag，啟 `/loop 65s /mailbox-react` 並在 `/pm-bye` 停止

**延遲**：≤65s。
**成本**：`/loop 65s` × 5h session ≈ 275 次 LLM 呼叫（每次最少 system prompt + skill body tokens）。

**建議**：只在真的需要時才升級，且加 guardrail：
- 連續 N 次空 poll 就自動 throttle（160s / 320s 逐漸拉長）
- Quota 警戒時自動降級回階段 1

## 限制（必須誠實說清楚）

- Session 沒開就收不到，訊息堆在 inbox 等下次開。這是「等於郵件 inbox」不是「IM」。
- 兩邊同時寫同一個 inbox → 要用 atomic rename（`.tmp` → `mv`）避免 partial read。一般個人情境不易撞。
- Model 在「靜止等 user」狀態下，沒有任何機制能叫醒它。hook 只在 tool / prompt 事件觸發。
- 安全邊界薄 — inbox 檔若被其他程式寫入，等同 prompt injection 到 model。生產用需要 signing / auth。

## 與既有 dotfiles 組件的關係

- **`/pm` skill**：入場點，spawn poller；結束點，呼叫 `/pm-bye` 時同時停 poller
- **`settings.json` hooks**：新增 `UserPromptSubmit` hook 項
- **`pm-update.sh`**：可擴展成同時更新 `registry.json` 的 `last_seen`
- **quota guard**：現有 `UserPromptSubmit` hook 已會看 `usage-cache.json`；階段 2 的 `/loop` 升級決策可以直接讀它

## 待決 / 開放問題

1. **Session ID 來源** — Claude Code 沒明文 API 暴露，要靠 `SessionStart` hook 抓 `$CLAUDE_SESSION_ID`（如果有）還是自己用 `conversation log 路徑` 推？需先驗證。
2. **多 session 同名專案** — 兩個 session 同時開同一個 project 目錄，怎麼區分？用 session ID 不用 project name 解。
3. **GC 策略** — 24h 沒 session 碰過的 inbox 自動清？還是永久保留？
4. **跨機器** — 本設計假設本機 `~/.claude/` 共用。跨機器要改成 S3/GCS/Syncthing；非 MVP scope。

## 下一步（若要實作）

1. 寫 `SessionStart` hook 把 session_id 寫進 `registry.json`
2. 寫 `mailbox-poll.sh` + `mailbox-send.sh` + `mailbox-inject.sh`
3. 在 `settings.json` 掛 `UserPromptSubmit` hook
4. 在 `/pm` skill 結尾補「spawn poller」步驟，`/pm-bye` 補「kill poller」
5. 寫 `docs/mailbox-setup.md`（安裝 + 使用範例）
6. MVP 手動測：開兩個 session，A 送 B 收，驗 ≤ 130s 能收到

預估 10-15 分鐘寫 MVP（階段 1），測試另計。
