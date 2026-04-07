# Red-Team Review — /do Delegation Threshold + Deep Mode Quality Plan

## Metadata
- Date: 2026-04-07
- Reviewer: Independent red-team (default-deny)
- Subject: Plan to lower quota threshold 80→60 and harden /do deep R2/R1
- Artifacts inspected:
  - `E:\github\claude-dotfiles\settings.json`
  - `E:\github\claude-dotfiles\skills\do\scripts\do_helper.py`
  - `E:\github\claude-dotfiles\opencode-vs-claude-code-eval-2026-04-07.md`
  - `E:\github\claude-dotfiles\CLAUDE.md`
  - `C:\Users\benth\.claude\CLAUDE.md`
  - Repo root listing (no `hooks/` directory exists)

## Verdict: REJECT (must revise before implementation)

The plan is built on a false premise about where the quota threshold lives. Step 1 cannot be executed as written. Several other steps rest on weak quantitative claims and have unconsidered side-effects.

---

## Findings

### F-001 — `hooks/quota_check.py` does not exist
- Location: Plan Step 1
- Severity: RED (blocking)
- Problem: Plan instructs editing "the threshold constant in `hooks/quota_check.py`". There is no `hooks/` directory in `E:\github\claude-dotfiles` and no file named `quota_check.py` anywhere in the repo.
- Verification: `ls E:\github\claude-dotfiles` shows no `hooks/`; `Grep quota` over the repo only matches docs/statusline, never a hook script.
- Reality: The quota check is an inline Python one-liner embedded directly in `settings.json` at `hooks.UserPromptSubmit[0].hooks[0].command`. The thresholds are two literal `80`s inside a single shell-escaped expression: `red=not stale and (s>=80 or w>=80)`.
- Verdict: Step 1 must be rewritten to edit `settings.json` (the inline command), not a non-existent Python file. This also means there is no "constant" to refactor — both `80`s are literals inside an escaped string and any edit must preserve the JSON+shell+Python triple quoting.

### F-002 — Project `CLAUDE.md` does not contain delegation rules
- Location: Plan Step 1 ("同步更新 CLAUDE.md 與 ~/.claude/CLAUDE.md")
- Severity: RED (blocking, partially)
- Problem: The plan says to update both files. `Grep` for `80|quota|RED` over `E:\github\claude-dotfiles\CLAUDE.md` returns zero matches — the project CLAUDE.md only contains install instructions and explicitly defers to the global file ("User Preferences ... 見全域 ~/.claude/CLAUDE.md，不在此重複"). Editing it to add a threshold would violate its stated single-source-of-truth policy and the MEMORY note `feedback_repo_no_personal_config.md`.
- Verdict: Only the global `~/.claude/CLAUDE.md` should be updated. Drop the project-CLAUDE.md edit, or it will create an inconsistency the user has explicitly told us to avoid.

### F-003 — 80% threshold is also baked into the hook's user-facing message
- Location: Plan Step 1
- Severity: ORANGE
- Problem: The inline hook prints `⚠️ QUOTA RED (5h={s}% 7d={w}%)`. The plan only mentions changing the comparison constant. After lowering to 60, the warning will fire at 60% but still be labelled "RED" — and the global `CLAUDE.md` says "門檻 80% 與 statusline 紅字一致." Statusline (`statusline.js`) almost certainly has its own 80 threshold for red colouring, which the plan does not touch. Result: hook fires at 60 but statusline is still green, breaking the documented invariant.
- Verdict: Either also lower the statusline red threshold, or change the hook label to something like "QUOTA WARN (yellow zone)". Plan must address this.

### F-004 — Quantitative claim "紅燈 ⬇️ 60-70%" has no evidence
- Location: Plan "Estimated impact"
- Severity: ORANGE
- Problem: There is no measured distribution of session-utilization values cited in the plan or in any nearby document. Whether moving from 80→60 cuts red events by 60-70% depends entirely on how often the user sits in the 60-80 band — which is unknown. The number is fabricated.
- Verdict: Either gather a week of `usage-cache.json` snapshots first, or restate as "expected to fire earlier; magnitude unknown until observed."

### F-005 — Quantitative claim "品質損失 < 1 分" is not supported by the eval
- Location: Plan "Estimated impact" + "計劃背景"
- Severity: ORANGE
- Problem: The eval scored a single run per task (the eval itself flags this in Caveats: "Re-runs could shift the overall tie by more than 2 points in either direction"). Claiming sub-1-point loss from a single noisy measurement is statistically meaningless. Worse, the plan's actual mechanism (lower threshold → more delegation to Gemini) directly increases the share of work going through the +3-point-deficit category (T4-C complex code write) — which is exactly the worst case in the eval, not the average.
- Verdict: The "<1 分" figure should be removed or qualified. The honest claim is "we accept up to ~3 points loss on complex-code tasks in exchange for quota relief, mitigated by the expanded deep-exclusion list."

### F-006 — Eval reference T3-C/T4-C +3 is partially misquoted
- Location: Plan "計劃背景"
- Severity: YELLOW
- Problem: Plan says "Claude 在 T3-C / T4-C 複雜程式碼推理 +3 分." Per the eval table: T3 (S+C) is a **tie** at 48/48; the +3 is entirely in T4 (Code write S+C: 45 vs 42). T3-C has prose advantage for Claude but no scoring delta in the category total. Minor but the plan should not over-attribute the gap.
- Verdict: Restate as "Claude +3 in Code-write category (T4)."

### F-007 — Step 4 `ast.parse` only works for Python deliverables
- Location: Plan Step 4
- Severity: ORANGE
- Problem: `do_helper.py` is engine-agnostic and language-agnostic — `cmd_easy`/`cmd_deep` accept arbitrary spec/output. The plan does not say what to do when the deliverable is Markdown, JSON, shell, JS/TS, or a mix. Naively calling `ast.parse` on non-Python output will always fail and either (a) always trigger R2 must-fix (false positives, infinite-feeling loops) or (b) be silently skipped (then the step delivers nothing).
- Sub-problem: Even for Python, the helper currently strips no markdown fences before storing R1 (R1 prompt says "do not wrap in markdown fence" but Gemini ignores that ~30% of the time empirically — see `parse_review`'s own fence-tolerance logic). `ast.parse` will fail on a fenced response.
- Verdict: Plan must specify language detection (heuristic or spec hint) and a skip path for non-Python. Also must strip fences before parsing.

### F-008 — Step 3 R2 hardening risks R3 runaway / regressions
- Location: Plan Step 3
- Severity: ORANGE
- Problem: Current R2 prompt is short and the current `cmd_deep` hard-caps at 3 rounds (R1→R2→R3), with NO re-review of R3. Making R2 more aggressive ("find bugs spec didn't mention") will:
  1. Increase R2 fail rate, so almost every deep run now goes to 3 rounds (+ wall-clock, + cost — not the "+5-10s" guess; closer to +30-50% total deep latency since R3 is the heaviest call).
  2. Push R3 to "fix" things that aren't actually wrong (e.g. the duplicate-import / dead-code list is hyper-specific to fixtures from one eval and may be irrelevant to the actual task). R3 has no validator, so its over-corrections ship as `verdict: "fixed"` unchallenged.
  3. The plan's R3 round-cap is unchanged, meaning the new must-fix from Step 4 (ast.parse failures) competes for the single R3 budget with R2's expanded findings. If both fire, R3 prompt becomes a kitchen sink and quality drops.
- Verdict: Either add an R4 re-review for R3 output, or make Step 3's added criteria advisory ("note potential issues but only fail on spec violations").

### F-009 — Plan does not address R2 prompt being model-specific
- Location: Plan Step 3
- Severity: YELLOW
- Problem: The injected hints (`wall-clock vs monotonic`, `duplicate import itertools`, `misleading "NOT thread-safe" docstring`) are lifted verbatim from the eval's T4-C narrative. Embedding fixture-specific anti-patterns into a general-purpose review prompt is prompt-engineering overfitting. It will produce confident-but-wrong false positives on unrelated tasks.
- Verdict: Generalise the language ("prefer monotonic clocks for relative timing", not "wall-clock vs monotonic").

### F-010 — Step 2 deep-exclusion list overlaps with existing global rules
- Location: Plan Step 2
- Severity: YELLOW
- Problem: Global `~/.claude/CLAUDE.md` already excludes "修改現有核心程式碼", "需要理解上下文的 bug fix", "架構設計相關", "CLAUDE.md/AGENTS.md 修改". The plan's additions ("commands/*.md", "skills/**", "race condition") are already covered by "core code modification" + "context-dependent bug fix". The added entries duplicate intent rather than expand coverage and risk drift between two rule lists.
- Verdict: Add only `commands/*.md` and `skills/**` (genuinely new, since they are prompt files not "core code"); drop the rest as dupes.

### F-011 — Step 5 "觀察一週" has no defined success metric
- Location: Plan Step 5
- Severity: YELLOW
- Problem: No threshold defined for rollback. If after a week red-zone fires drop only 20% (not 60-70%) and three deep runs ship subtly wrong code, what triggers revert? Without a kill criterion the experiment can't fail.
- Verdict: Define rollback condition before deploying.

---

## Uncovered Risks

1. **install.ps1 redeploy ordering**: Editing `settings.json` in repo then running install.ps1 will overwrite the live `~/.claude/settings.json`. If the user has any local-only edits there (e.g. extra MCP servers), they will be lost. Plan does not check.
2. **Deep-mode token budget**: Lowering the threshold means deep runs now happen during the 60-80% band, i.e. when Claude itself is also closer to the wall. If a deep run fails and falls back to Claude (current `do.md` behaviour), it lands at exactly the worst time.
3. **Hook firing on every prompt at lower threshold = more interruptions**: At 80% the QUOTA RED banner fires for ~the last 20% of a session; at 60% it fires for the last 40%. Users have reported alert fatigue from less aggressive hooks; the plan does not consider UX cost.
4. **Cache staleness window (10 min) interacts with new threshold**: A user crossing 60% mid-task will not see the warning until the cache refreshes — meaning the "earlier warning" benefit is partly negated for short bursty sessions.
5. **No telemetry plan**: There is no logging added to measure whether the changes actually achieved their goal. Step 5's "觀察" is purely vibes-based.
6. **Step 4 ast.parse adds a hard dependency on stdlib `ast`** — fine for Python, but if someone later swaps `do_helper.py`'s runtime for a frozen / stripped Python (e.g. embedded), it breaks silently.

---

## Scores (1-5)

| Dimension | Score | Notes |
|---|:---:|---|
| Accuracy (paths/files/constants match reality) | **1** | Step 1 references a non-existent file; project CLAUDE.md edit violates documented policy; T3-C +3 attribution wrong. |
| Feasibility (can be implemented as written) | **2** | Step 1 & Step 4 cannot be implemented as written; Step 3 implementable but mechanically risky. |
| Completeness (covers needed changes) | **2** | Misses statusline threshold, R3 re-review, language detection, install.ps1 redeploy, telemetry, rollback criteria. |
| Risk assessment (is the plan honest about downsides?) | **2** | Quantitative claims (60-70%, <1 分) are unsupported; deep-mode wall-clock estimate (+5-10s) is optimistic; UX cost ignored. |

**Overall: REJECT.** Rewrite Step 1 against `settings.json` reality, drop the false project-CLAUDE.md edit, generalise Step 3's hints, gate Step 4 on language, and replace the fabricated impact numbers with measurement plus a rollback criterion. Then resubmit.
