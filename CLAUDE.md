# Claude Dotfiles

Custom commands（`/hello`、`/sc`、`/bye`、`/pm` 等）的原始碼：
- **GitHub**：https://github.com/CPIDLE/claude-dotfiles
- **安裝位置**：`~/.claude/`（由 install script 複製）

## 關鍵 ID

| 項目 | ID |
|---|---|
| Chat Email (email-to-chat) | `cpidle-project-report@gyro.com.tw` |
| Dashboard Sheet | `19Wn3U4kbQw712SZGN7eKJDYGa5JYUUYofDi-zuakuPI` |
| Apps Script Web App | `AKfycbz-a6vGaQ1bucB4MGtCZ80ICnkCqHWQ2VFbL2yM8B_dGK8_HLlVURDpNKI1OvUjdTONnw` |

---

# User Preferences

## Notification Sounds
- When asking the user a question or needing user input/selection: handled by PreToolUse hook on AskUserQuestion in settings.json (auto beep before question). No need to manually beep.
- When task is completed: handled by Stop hook in settings.json (auto beep 3 times). No need to manually beep.

## Plan-Execute Workflow (Enhanced Plan Mode)

For any non-trivial task, follow this strict 3-phase workflow:

### Phase 1: Plan (使用者確認)

Before writing any code or executing any action, present a detailed plan:

1. **Use EnterPlanMode** for tasks involving multiple files, architectural decisions, or multi-step operations
2. In the plan, clearly list:
   - **Goal**: what will be achieved
   - **Steps**: numbered action items with specific file paths and changes
   - **Scope boundary**: what is IN scope and what is OUT of scope
   - **Permissions needed**: list all potentially sensitive operations (git push, file deletion, external API calls, running servers, installing packages, etc.)
   - **Estimated impact**: files created/modified/deleted
3. Use **ExitPlanMode** to submit the plan for user approval
4. **Do NOT proceed until the user approves the plan**

### Phase 2: Permission Reminder (權限提醒)

After the user approves the plan, before starting execution:

1. Print a concise **permission summary block** like:
   ```
   --- Permission Summary ---
   This plan will require the following permissions:
   • [Bash] run build/test commands (npm test, npm run build, etc.)
   • [Bash] git commit and push to origin/main
   • [Write] create 3 new files in src/
   • [Edit] modify 5 existing files
   • ...
   Proceeding autonomously within plan scope.
   ---
   ```
2. This is a **notification only** — do not wait for another confirmation. Proceed immediately after displaying it.

### Phase 3: Autonomous Execution (自主執行)

Once the plan is approved, execute **autonomously** within the plan scope:

- **DO auto-approve**: all file reads, writes, edits, glob, grep, bash commands, and tool calls that fall within the approved plan steps
- **DO auto-approve**: running tests, builds, linters, formatters as part of the plan
- **DO auto-approve**: git add, commit (when the plan includes it)
- **DO continue without asking**: when a step succeeds, move to the next step immediately
- **DO use TodoWrite**: track each plan step and mark completed as you go

**STOP and ask the user ONLY when**:
- An action falls **outside the approved plan scope** (e.g., unexpected dependency needed, new file not in the plan)
- A step **fails and cannot be resolved** after reasonable attempts (e.g., test failures that require design decisions, ambiguous errors)
- A **destructive or irreversible action** was not covered in the plan (e.g., force push, dropping data)
- You discover the plan needs **significant revision** (scope creep, wrong assumption found)

**DO NOT stop to ask for**:
- Routine permission prompts for actions already listed in the plan
- Confirmation of individual file edits that match the plan
- Minor adjustments within plan scope (e.g., fixing a typo found during editing)

---

## Coding Discipline (程式品質規則)

以下規則補充系統內建行為未涵蓋的品質約束。

### 小步驗證
- 每完成 Plan 中的一個步驟，就跑相關 test 再進入下一步
- 「相關 test」定義：改動檔案有對應 test 檔 → 跑該 test 檔；沒有 → 跑整個 test suite；執行 test 指令失敗或專案無 test 相關設定 → 跳過
- 多步驟改動中，某步 test 失敗 → 停下修正，不繼續後續步驟

### 範圍控制
- 發現需要額外修改（含重複程式碼需抽共用）時，回報使用者而非自行擴大範圍
- Commit 粒度遵循 Plan 核准的策略；Plan 未指定時，預設一個邏輯功能一次 commit

### Code 品質底線
- 避免模糊命名（`data2`、`result2`、`handleClick2`），test fixtures 或 swap 暫存等慣例用法除外

### 安全編碼底線
- 不 hardcode secrets、API keys、passwords — 用環境變數或 config
- 處理使用者輸入和外部 API 回應時，加入基本驗證與 error handling
