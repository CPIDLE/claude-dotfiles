# Red-Team Review v4 — /do Delegation Plan (Round 4)

## Metadata
- Date: 2026-04-07
- Reviewer: Independent red-team (default-deny)
- Subject: Plan v4 (revision of v3 addressing N-101..N-108)
- Prior reviews: v1 REJECT, v2 REVISE, v3 REVISE
- Re-inspected:
  - `E:\github\claude-dotfiles\settings.json`
  - `E:\github\claude-dotfiles\install.sh`
  - `E:\github\claude-dotfiles\install.ps1`
  - `E:\github\claude-dotfiles\skills\do\scripts\do_helper.py`
  - `E:\github\claude-dotfiles\commands\do.md` (do_history format)

## Verdict: ⚠️ REVISE (close to APPROVE — 2 mechanical fixes + 2 spec clarifications)

v4 addresses every v3 finding directly. The blockers (N-101 path expansion, N-102 silent fail, N-105 CRLF) are resolved by design. Remaining issues are mechanical (parse_review fallback dict, JSON-escaping inside settings.json command string, baseline definition for the wall-clock rollback gate) — none architectural. After these are pinned down v4 is implementable as written.

---

## v3 Disposition Table

| ID | Sev | v3 Issue | v4 Status | Evidence |
|---|---|---|---|---|
| N-101 | 🔴 | `~` not expanded by python argv on Windows | ✅ Resolved | A1a uses `bash -c "python ~/.claude/hooks/quota_check.py"` matching settings.json L29 precedent (`bash ~/.claude/pm-update.sh reset`). Bash is invoked first, expands `~`. |
| N-102 | 🟠 | Fail-open masks dead hook | ✅ Resolved | A1b adds positive invocation-trace test (jsonl line appears) before relying on RED rendering. Stderr breadcrumb on exception further covers silent path. |
| N-103 | 🟠 | Rotation race window | ✅ Resolved (accepted) | A1c wraps rename in try/except, swallows ERROR_SHARING_VIOLATION, continues append. Acceptable for single-user 7-day window; data loss bounded to one rotated file. |
| N-104 | 🟠 | do.md report enforcement is soft | ✅ Resolved (acknowledged) | B1 explicitly notes helper JSON-lines is source-of-truth and adds N-104 known-limit footnote in do.md. |
| N-105 | 🟡 | CRLF in strip_full_fence regex | ✅ Resolved | v4 regex now `\r?\n`. |
| N-106 | 🟡 | install.sh not updated; hooks dir does not exist | ✅ Resolved | A1a explicitly lists install.ps1 + install.sh + creating hooks/ directory. |
| N-107 | 🟡 | The 70 fallback was a guess | ✅ Resolved | v4 deletes the 10-25% → 70 branch entirely. Two outcomes only (>25% → median, ≤25% → no change). |
| N-108 | 🟡 | "last line" parsing must enumerate advisory_notes | ✅ Resolved | B1 explicitly states advisory_notes lives only on the final-line emission, not on round emissions, and do.md must spell it out. |

8 of 8 resolved.

---

## v4 New Findings

### N-201 — 🟠 JSON-escaping of the bash -c command inside settings.json
- v4 specifies `bash -c "python ~/.claude/hooks/quota_check.py"` as the hook command. settings.json L8 already shows the existing pattern: the entire command field is a JSON string, double-quotes inside the command must be escaped as `\"`.
- The literal that must end up in settings.json is therefore:
  ```json
  "command": "bash -c \"python ~/.claude/hooks/quota_check.py\""
  ```
  not what the plan text reads. v4 should spell this out explicitly. Otherwise the first install.sh redeploy will write a malformed JSON or a single-quoted bash form (which behaves differently for `~` expansion only when no shell metacharacters are present — currently fine, but brittle).
- **Recommended:** use single quotes inside the command to avoid the escape entirely:
  ```json
  "command": "bash -c 'python ~/.claude/hooks/quota_check.py'"
  ```
  This is JSON-clean (no `\"`), bash-clean (single quotes prevent shell expansion *inside* the quoted string but `~` is still expanded by bash because it is a separate token at start of word — actually NO: `~` inside single quotes is NOT expanded). Pick one and pin it:
  - `bash -c "python ~/.claude/hooks/quota_check.py"` → JSON needs `\"` escaping. `~` expands (outside any inner quotes).
  - `bash -c 'python $HOME/.claude/hooks/quota_check.py'` → JSON-clean, but uses `$HOME` because `~` would not expand inside single quotes.
- v4 must commit to one form and document the escape. Suggested: option 1, with the JSON form `"bash -c \"python ~/.claude/hooks/quota_check.py\""` shown verbatim in the plan.

### N-202 — 🟠 Hook spawn shell on Windows is unspecified
- v3 N-101 assumed Claude Code on Windows spawns hooks via `cmd.exe`. Verified settings.json already uses `bash ~/.claude/pm-update.sh reset` (SessionStart, L29) and it works on this user's setup → Claude Code is finding `bash` on PATH (Git Bash). This means the spawn is **direct exec, not via cmd.exe** (cmd.exe would not find a bare `bash` without `.exe`, though Windows path resolver might).
- The risk: if a future user has no `bash` on PATH (vanilla Windows with no Git installed), the hook silently fails. Existing pm-update.sh has the same dependency, so this is a consistent constraint, not a regression. Worth one line in rollout-criteria.md: "Requires Git Bash on PATH; same constraint as existing SessionStart hook."
- Not a blocker; document and move on.

### N-203 — 🟠 parse_review backward-compat for advisory_notes is under-specified
- do_helper.py L156-170 (current `parse_review`):
  - Success path: `return json.loads(text)` — if R2 model omits `advisory_notes`, the returned dict simply has no key. Downstream `review.get("advisory_notes", [])` would be safe but the plan does not show that call site.
  - Failure path (JSONDecodeError fallback, L166-170): returns a hard-coded dict with `verdict/issues/fix_instructions` only. **This dict does not include `advisory_notes`.** If cmd_deep then does `review["advisory_notes"]` → KeyError. Must use `.get("advisory_notes", [])` everywhere, or add `"advisory_notes": []` to the fallback dict.
- **Fix required:** v4 must explicitly state:
  1. The fallback dict in `parse_review` gains `"advisory_notes": []`.
  2. cmd_deep extracts via `review.get("advisory_notes", [])`, never `review["advisory_notes"]`.

### N-204 — 🟠 advisory_notes provenance when R3 fires is ambiguous
- do_helper.py L194-229: when R2 verdict ≠ pass, R3 runs and the final emit becomes `{"final": r3, "rounds": 3, "verdict": "fixed", ...}`. v4 says "cmd_deep final JSON 加 advisory_notes". The plan must answer: when R3 fires, are the advisory_notes carried forward from R2's review, or re-derived?
- The only reasonable answer is **carry from R2** (R3 prompt does not request a JSON review structure; it returns code only). v4 should state explicitly: `advisory_notes` always sourced from the R2 `parse_review` dict, regardless of whether R3 ran. Otherwise reviewers will guess wrong during implementation.
- **Fix required (one line):** "advisory_notes is taken from R2 review; in the R3 path, the same R2 advisory_notes are attached to the final emit."

### N-205 — 🟠 "deep wall-clock +50%" rollback gate has no baseline
- Verified `commands/do.md` L296-301 do_history.md row format:
  ```
  | 日期 | Level | 任務 | 引擎 | 結果 | 備註 |
  ```
  No wall-clock column exists. Only the free-text 備註 sometimes contains "3 rounds, 2 issues fixed" — no timing.
- v4's A2 rollback criterion "deep wall-clock +50%" therefore has **no historical baseline** to compare against. There are three options:
  1. Add a wall-clock column to do_history.md *before* Phase A starts (one-shot schema bump), capture pre-change samples for at least 3-5 deep runs as the baseline.
  2. Use the do_helper.py-internal timing (already feasible — wrap each `engine.call` in `time.perf_counter()` and emit elapsed in the final JSON-line). Cleaner, no schema bump.
  3. Drop the "+50%" gate as unmeasurable and rely on subjective + red-drop only.
- v4 currently picks none. **Fix required:** either delete the criterion or specify how to measure. Option 2 is cheapest but adds code outside the v4 scope ("不改 easy 邏輯 / 引擎 / R3"). Option 3 is honest with current scope.

### N-206 — 🟡 1MB rotation cap → ~weekly capacity arithmetic
- A1c rotates at 1MB. Each jsonl row per v4 is `{ts,s,w,red,stale}` ≈ 60-80 bytes including newline. At 1MB that's roughly **13k-17k events**. UserPromptSubmit fires once per user message; an active week is plausibly 200-1000 prompts. Even at 1k/week, the cap holds ~13 weeks of data — well over the 1-week observation window.
- Conclusion: cap is fine, possibly over-engineered. Not a finding, just confirmation. Could simplify A1c by skipping rotation entirely (v3 N-103 alternative path) since the cap will not be hit during Phase A.

### N-207 — 🟡 install.sh hooks block — easy to add
- Verified `install.sh` has clear section structure (sections 1-11, each with `echo "--- ... ---"` header). Adding section "8.5 Hooks" between Skills (8) and Docs (9) is mechanical. Same template:
  ```bash
  echo ""
  echo "--- Hooks ---"
  if [ -d "$SCRIPT_DIR/hooks" ]; then
      mkdir -p "$CLAUDE_DIR/hooks"
      for f in "$SCRIPT_DIR/hooks/"*.py; do
          [ -e "$f" ] || continue
          backup_and_copy "$f" "$CLAUDE_DIR/hooks/$(basename "$f")"
      done
  fi
  ```
  Parallel block in install.ps1 between sections 8 and 9 is equally trivial. No blocker; flagged as "ready to lift verbatim."

### N-208 — 🟡 statusline.js:53 reference unverified
- v4 says "C1 同步改 settings.json 兩個 80 + statusline.js:53 + hook RED 文字 + 全域 CLAUDE.md". I did not re-verify that statusline.js line 53 is still the threshold line (file may have shifted). Recommend v4 add "verify line number at execution time, do not hard-code in script" — but this is style, not a finding.

---

## Carry-Forward Risks (still open, accepted)

1. **Empty-dataset Phase A → C gate**: v3 raised; v4's A1b smoke test positive case mitigates the silent-zero-event risk, but A2 still does not specify a minimum event count. Recommend: "≥ 50 logged events before Phase C decision, otherwise extend observation."
2. **install.ps1 settings.json clobber**: still un-mitigated. v4 forces a redeploy in A1a. `.bak` exists; document in rollout note.
3. **B1 effect-measurement**: emitting advisory_notes does not measure if they helped. Accepted, repeat acknowledgement.

---

## Required Fixes Before APPROVE

1. **N-201**: Spell out the exact JSON literal for the hook command (with `\"` escaping or single-quote form). One line in A1a.
2. **N-203**: Add `"advisory_notes": []` to the parse_review JSONDecodeError fallback dict, and use `.get()` on the success path. One line in B1.
3. **N-204**: State that advisory_notes is sourced from R2 even when R3 path runs. One line in B1.
4. **N-205**: Either delete the "+50% wall-clock" rollback criterion, or specify how it is measured (recommend: instrument do_helper.py with `time.perf_counter()` and emit `elapsed_ms` on the final JSON-line; capture 3 baseline samples before Phase A starts). One paragraph in A2.

## Recommended (non-blocking)

- N-202: One sentence in rollout-criteria.md noting Git Bash dependency.
- N-206: Consider dropping rotation entirely; the cap will not trigger.
- Pre-register Phase A → C minimum event count (≥ 50).

---

## Scores (1-5)

| Dimension | Score | Notes |
|---|:---:|---|
| Accuracy (paths, escaping, file refs) | **4** | Correctly identifies bash -c precedent, install.sh/ps1 needs, hooks dir. Underspecifies JSON escaping (N-201) and parse_review fallback (N-203). |
| Feasibility | **4** | bash -c form will work; install.sh additions mechanical; rotation defensive. Wall-clock baseline (N-205) is the only "would not actually be measurable" gap. |
| Completeness | **4** | All v3 findings addressed. parse_review fallback dict, R3 advisory provenance, and timing baseline are the missing footnotes. |
| Risk honesty | **5** | Drops the 70 compromise, admits v1 assumption may be wrong, removes unmeasurable C2 items, scopes tightly. Strong epistemics. |

**Overall: REVISE.** Four one-line fixes (N-201, N-203, N-204, N-205) and v4 is APPROVE. None require code yet — all are plan-text clarifications. v4 is the closest any iteration has been to ready-to-execute.
