---
name: Dual Engine SOP
description: Claude Code + opencode 分層委派架構草案，從 L0 全做到 L4 自主巡邏
type: project
---

## 分層委派架構

核心思路：Claude Code 是決策者，opencode 是執行者。隨著信任建立，逐步擴大委派範圍。

### Level 0：Claude Code 全做（基線）

所有工作由 Claude Code 完成。用量最高，品質最穩。

### Level 1：新模組委派（已驗證 2026-04-03）

```
Claude Code: 寫 spec + 審核
opencode:    實作新檔案
```

- 只碰新檔案，不改現有程式碼
- Spec 必須包含完整 API 簽章 + 交付清單
- Claude Code 跑測試 + 讀 diff 驗收

### Level 2：受控修改委派

```
Claude Code: 寫 spec（含 diff 級指示）+ 審核
opencode:    修改現有檔案 + 新增檔案
```

- 允許修改指定的現有檔案（spec 明列可改 + 禁改）
- Spec 對修改部分寫到「哪個函式、改什麼、為什麼」
- 審核加強：regression 必跑 + 逐個 diff 確認
- 交付清單加「未修改確認」項目

### Level 3：任務級委派

```
Claude Code: 寫任務描述（不寫函式簽章）+ 審核
opencode:    自行決定結構 + 實作
```

- Claude Code 只描述目標，不規定實作方式
- 前提：完善 AGENTS.md + 足夠測試覆蓋
- Claude Code 審核時間較長（要理解設計決策）

### Level 4：自主巡邏

```
Claude Code: 定期審核 + 方向修正
opencode:    主動找問題 + 修復
```

- opencode 定期跑 lint/測試/靜態分析，自動修小問題
- 開 feature branch，等 Claude Code 審
- 需要：git branch 保護 + CI + 定期 review 機制

### 用量估算

| Level | Claude | opencode | 適用場景 |
|-------|--------|----------|---------|
| 0 | 100% | 0% | 核心架構、緊急修復 |
| 1 | ~30% | ~70% | 新模組開發 |
| 2 | ~25% | ~75% | 功能迭代 |
| 3 | ~15% | ~85% | 獨立小功能 |
| 4 | ~10% | ~90% | 維護期 |

### 升級條件

| 升級 | 條件 |
|------|------|
| L0→L1 | 有 AGENTS.md + 基礎測試 |
| L1→L2 | L1 成功 3 次、測試覆蓋 > 60% |
| L2→L3 | L2 成功 5 次、未破壞現有功能 |
| L3→L4 | 有 CI + branch 保護 + 定期 review |

任何 level 搞砸 → 降回上一級。

### 不委派紅線

- 架構決策
- AGENTS.md / CLAUDE.md 修改
- 安全敏感操作
- 跨系統整合
- 最終 review 和 release

### 實戰紀錄

- 2026-04-03 L1 驗證通過：Phase 2 四個模組，opencode (Gemini 3 Flash) 一次交付，46 tests 全過
- 已知問題：spec 沒寫到的地方 opencode 會自行決定（FK DH 參數、自比排除），品質不穩
