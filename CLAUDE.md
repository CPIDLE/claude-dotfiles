# Claude Dotfiles

Custom commands（`/hello`、`/sc`、`/bye`、`/pm` 等）的原始碼：
- **GitHub**：https://github.com/CPIDLE/claude-dotfiles
- **安裝位置**：`~/.claude/`（由 install script 複製）

## 關鍵 ID

| 項目 | ID |
|---|---|
| Slack Channel `#all-cpidle` | `C0AN35HJQ8L` |
| Dashboard Canvas | `F0AMWD1GAD9` |

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
