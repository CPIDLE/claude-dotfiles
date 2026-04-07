# Red-Team Review v2 — /do Delegation Plan (Revised)

## Metadata
- Date: 2026-04-07
- Reviewer: Independent red-team (default-deny)
- Subject: Plan v2 (measure-first + safe small edits + conditional threshold)
- Prior review: `reviews/2026-04-07-plan-review.md` (REJECT, F-001..F-011)
- Artifacts re-inspected:
  - `E:\github\claude-dotfiles\settings.json`
  - `E:\github\claude-dotfiles\skills\do\scripts\do_helper.py`
  - `E:\github\claude-dotfiles\statusline.js`
  - `E:\github\claude-dotfiles\install.ps1`

## Verdict: ⚠️ REVISE

v2 is a major improvement in epistemic posture (measure first, narrower scope, honest impact). It correctly retreats from the fabricated quantitative claims and the non-existent `hooks/quota_check.py`. However, several mechanical details are under-specified or technically incorrect, and two new problems are introduced. Not blocking-bad, but cannot be implemented as written.

---

## v1 Findings — Disposition Table

| ID | v1 Issue | v2 Status | Notes |
|---|---|---|---|
| F-001 | `hooks/quota_check.py` does not exist | ✅ Resolved | v2 C1 names `settings.json` literals + `statusline.js:53` directly. |
| F-002 | Project CLAUDE.md edit violates single-source policy | ✅ Resolved | B3 explicitly says "只改全域". |
| F-003 | Statusline 80 threshold + RED label drift | ✅ Resolved | C1 lists statusline.js:53, hook RED text, and global doc together. |
| F-004 | Fabricated "60-70% drop" estimate | ✅ Resolved | A1 introduces logging; "honest impact" admits unknown. |
| F-005 | Fabricated "<1 分 quality loss" | ✅ Resolved | C2 abandons aggressive R2; v2 makes no quality claim. |
| F-006 | T3-C +3 misquote | ⚠️ Not addressed | Minor; v2 simply drops the claim, which is acceptable but not explicit. Mark partial. |
| F-007 | `ast.parse` only works for Python; needs language detection + fence stripping | ✅ Resolved (by removal) | C2 explicitly drops ast.parse. B2 adds fence stripping for R1 — see v2 finding N-002. |
| F-008 | R2 hardening risks R3 runaway | ✅ Resolved | B1 makes added text advisory; R3 untouched. But see N-001 (the advisory may be a no-op). |
| F-009 | R2 prompt fixture-overfitted hints | ✅ Resolved | B1 says "通用語言，不抄 fixture". |
| F-010 | Deep-exclusion list duplication | ✅ Resolved | B3 narrows to `commands/*.md` + `skills/**`. |
| F-011 | "觀察一週" no rollback metric | ⚠️ Partial | A2 lists three criteria, but one ("verdict=fixed 但實壞") has no detection mechanism — see N-005. |

Net: 9 resolved, 2 partial, 0 unaddressed.

---

## v2 New Findings

### N-001 — 🟠 B1 "advisory" R2 change is functionally a no-op
- The current R2 prompt outputs JSON with `verdict: pass|fail`. The downstream `cmd_deep` flow only branches on `verdict`. If you tell the reviewer "note potential issues but only fail on spec violations," and the underlying R2 was already only failing on spec deviations, you have changed nothing observable. The added "advisory" prose either (a) gets ignored by the model, or (b) leaks into `issues[]` with low severity but no consumer reads severity — it still passes through to R3 if verdict flips.
- **Implication**: B1 should either be dropped (admit no-change) or specify a concrete behaviour change — e.g. add an `advisory_notes` field in the JSON schema that the helper logs but does not act on, so future audits can see what was flagged. Without that, B1 is theatre.

### N-002 — 🟠 B2 fence stripping reuse claim is wrong
- `parse_review` (do_helper.py L156-170) extracts a fenced JSON blob via `re.search(r"```(?:json)?\s*\n?(.*?)```", ..., DOTALL)`. The regex matches the **first** fenced block. For R1 output the deliverable is **arbitrary code/text**, not JSON. Three concrete problems if you "reuse" parse_review's logic on R1:
  1. R1 may legitimately contain triple-backtick blocks (e.g. an embedded README example, or a markdown deliverable). Stripping the first fence eats real content.
  2. If R1 is wrapped in ```python ... ``` the regex grabs the inside — correct — but if there are *two* fenced blocks (e.g. code + usage example), only block 1 survives. Silent data loss.
  3. R1 is fed verbatim into the R2 prompt as `## Code:\n` + r1. If you strip fences before the R2 call, R2 may now mis-parse non-fenced multi-language blocks. Spec compliance check degrades.
- **Implication**: Fence stripping for R1 is not a copy of `parse_review`; it needs its own narrower rule, e.g. "only strip if the entire response is exactly one fenced block (`^```\w*\n.*\n```\s*$`)". Plan must specify which rule, or this introduces a regression in deep-mode markdown deliverables.

### N-003 — 🟠 A1 logging "一行加在 hook 旁邊" underestimates difficulty
- The current hook (settings.json L8) is a **single shell-escaped Python one-liner** inside JSON. Every `"` is `\"`, the whole thing is one string. To add `(timestamp, s, w)` append-to-jsonl logic you must:
  - Either extend the one-liner (more `\"` escaping, more failure surface — Windows shell + JSON + Python triple quoting), OR
  - Extract the hook into a real `~/.claude/hooks/quota_check.py` file (which is the right move but is exactly the refactor v1 was rejected for assuming already existed).
- v2 chooses option 1 implicitly ("加一行"). That is not "one line" — it is restructuring an already fragile escaped string. Add `pathlib.Path(...).open('a').write(json.dumps(...)+'\n')` and the JSON-escaping cost is non-trivial. High risk of breaking the existing hook silently (the hook fails closed → no QUOTA RED ever fires → user thinks they are always green).
- **Implication**: A1 should be promoted to "extract hook to a real file first, then add logging," and that extraction itself needs a redeploy + smoke test. v2's framing as "先測量, 安全" hides this cost.

### N-004 — 🟠 usage-log.jsonl path / install / git interactions not specified
- `~/.claude/usage-log.jsonl` is **not** in the repo, so `install.ps1` will not touch it (verified L11-145, no reference to `usage-log`). Good — no overwrite risk.
- BUT: nothing prevents the file from growing unbounded. A user with ~200 prompts/day for a week = ~1400 lines, fine; a heavy user with hooks firing on every sub-prompt = potentially 10k+ lines/week. No rotation, no size cap. Minor disk hygiene issue, not blocking.
- Also: if the user has `~/.claude` in any backup/sync (Dropbox, OneDrive), that file now syncs continuously. Plan should explicitly add it to `.gitignore` (it won't be in the repo, but if someone copies their whole `~/.claude` into the repo for inspection, it would leak quota timing). Yellow-tier; mention in plan.

### N-005 — 🟠 Rollback criterion "verdict=fixed 但實壞" is undetectable
- A2 lists three rollback triggers. Two are mechanical (red drop %, deep wall-clock %). The third — "any verdict=fixed but actually broken" — has **no automated check**. The whole point of the deep flow is that R3's "fixed" verdict ships unchallenged. To detect "actually broken" you need either:
  - Manual user review of every fixed-verdict deliverable for a week (high friction, will not happen), OR
  - An R4 re-validator (which v2 explicitly excluded in C2).
- Without a detection mechanism the criterion will never trigger and is decorative. Either drop it or specify "user manually flags any bad deep output during the observation week, target: 0 incidents."

### N-006 — 🟡 Sample size for Phase A
- One week of UserPromptSubmit events on a single user is a sample of convenience, not a statistical sample. If the user has ~50 prompts/day and the 60-80 band currently fires on ~5% of those → ~17 events. The 25% threshold for "go ahead with C1" is reasonable as a rule of thumb but should not be presented as inferentially solid. Plan should say "decision rule, not significance test."

### N-007 — 🟡 Phase A logging captures `s` and `w` but not whether the hook fired
- To answer "would lowering threshold help?" you also need to know context: was Claude actually about to do delegation-eligible work? Logging just (s, w) tells you the distribution of utilizations at prompt time but not whether the user *would have benefited* from earlier warning. Consider also logging the first 50 chars of the prompt or a task-class hint. (Privacy trade-off — note it.)

---

## Uncovered Risks

1. **Fence-stripping regression on existing markdown deliverables**: B2 could break `/do deep` for any spec asking for a README or doc. No test plan to catch it.
2. **Hook extraction is itself a redeploy**: A1's logging requires `install.ps1` to run, which backs up + overwrites `~/.claude/settings.json`. Any local-only edits the user has there are clobbered (same as v1's uncovered risk #1, still not addressed in v2).
3. **No instrumentation for B1's effect**: even if B1 changed something, there is no logging of how often R2 verdict flips between current and post-B1 prompt. You will not be able to tell if B1 helped, hurt, or did nothing.
4. **Phase A → Phase C decision point has no calendar gate**: "視 Phase A 結果" is open-ended. After how many days exactly? What if the distribution looks bimodal? Define a stop condition.
5. **C2 "明確不做" is good discipline but also leaves the original quality concern (T4-C +3) entirely unaddressed**. v2 honestly admits this; the user should understand they are accepting that gap permanently in exchange for not over-engineering the reviewer.

---

## Scores (1-5)

| Dimension | Score | Notes |
|---|:---:|---|
| Accuracy (paths, file references) | **4** | Correctly names settings.json, statusline.js:53. Mis-claims fence-stripping reuse (N-002). |
| Feasibility (can be implemented as written) | **3** | A1 "one line" understates JSON-escape cost (N-003). B1 may be a no-op (N-001). B2 needs its own rule (N-002). |
| Completeness | **3** | Phase gates underspecified; rollback criterion #3 undetectable (N-005); install.ps1 redeploy interaction still ignored. |
| Risk honesty | **5** | Major improvement. Explicitly admits "量化效果不可預測," drops fabricated numbers, narrows scope, lists what is *not* being done. This is what a good v2 looks like. |

**Overall: REVISE.** Three concrete fixes before implementation:
1. Promote A1 from "add a line" to "extract hook to a real `~/.claude/hooks/quota_check.py` file, then add logging there." Acknowledge this is itself a redeploy step and smoke-test it.
2. Either drop B1 or specify a real schema change (e.g. `advisory_notes` field) so its effect is observable.
3. Specify the exact fence-stripping rule for B2 (full-string-is-one-fence only) and add a regression check for markdown deliverables. Or drop B2 — R1's existing prompt already says "do not wrap," and silently rewriting model output is itself a category of risk.

Optional but recommended: drop rollback criterion #3 (or replace with "user-flagged incident count = 0"), and declare a hard Phase A duration (e.g. 7 calendar days, minimum 100 logged events, whichever later).
