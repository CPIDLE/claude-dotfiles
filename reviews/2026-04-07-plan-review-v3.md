# Red-Team Review v3 — /do Delegation Plan (Round 3)

## Metadata
- Date: 2026-04-07
- Reviewer: Independent red-team (default-deny)
- Subject: Plan v3 (hook-extract + smoke-tested logging + advisory_notes + full-fence-only stripping + conditional threshold)
- Prior reviews: v1 (REJECT, F-001..F-011), v2 (REVISE, N-001..N-007)
- Re-inspected:
  - `E:\github\claude-dotfiles\install.ps1`
  - `E:\github\claude-dotfiles\settings.json`
  - `E:\github\claude-dotfiles\skills\do\scripts\do_helper.py`
  - `E:\github\claude-dotfiles\commands\do.md`

## Verdict: ⚠️ REVISE (close to APPROVE)

v3 fixes the structural problems v2 raised. The epistemic posture is now solid: each phase has a tested gate, B1 has a real schema change, B2 has a precise rule, A1 acknowledges the file extraction. Three mechanical issues remain that will bite during implementation, plus one residual judgment call (the 70 fallback). None are blocking-bad, but the plan still cannot be implemented exactly as written.

---

## Disposition Table

### v2 Findings

| ID | Issue | v3 Status | Notes |
|---|---|---|---|
| N-001 | B1 advisory was a no-op | ✅ Resolved | v3 adds concrete `advisory_notes: [string]` JSON field, emitted in cmd_deep JSON-lines, surfaced in do.md report. Observable. |
| N-002 | B2 fence-strip reuse claim wrong | ✅ Resolved | v3 introduces `strip_full_fence` as a separate helper with the exact "entire response is one fence" regex. Does not touch parse_review. Matches the rule the review demanded. |
| N-003 | A1 "one line" understated escape cost | ✅ Resolved | A1a explicitly extracts hook to `hooks/quota_check.py`. A1b smoke-tests before A1c adds logging. Good sequencing. |
| N-004 | usage-log.jsonl unbounded growth | ✅ Resolved (size cap) | A1c specifies >1MB rotate to `.1`. Gitignore concern from v2 not mentioned but is yellow-tier. See v3 N-103. |
| N-005 | "verdict=fixed but broken" undetectable | ⚠️ Partial | v3 reframes as "subjective: any user report → revert," which is honest but still not a measurable gate. Acceptable as a manual escape hatch; should be labelled as such. |
| N-006 | Sample size disclaimer | ✅ Resolved | A2 explicitly admits "樣本不足、無自動偵測、無 task 類型". |
| N-007 | Logging task context | ⚠️ Not addressed | v3 logs only s/w. Means C1 decision is still based on raw distribution, blind to whether the user was about to do delegation-eligible work. Acceptable if explicitly accepted; v3 silently drops it. |

### v1 Carry-overs

| ID | Issue | v3 Status |
|---|---|---|
| F-006 | T3-C +3 misquote | ✅ Resolved by removal (no quantitative claim survives in v3) |
| F-011 | "觀察一週" no rollback metric | ✅ Resolved | A2 lists three concrete triggers (red-drop <30%, deep wall-clock +50%, subjective revert) |

Net: 9 resolved, 2 partial-but-acknowledged, 0 unaddressed.

---

## v3 New Findings

### N-101 — 🔴 `~` does not expand inside settings.json hook command on Windows
- Plan A1a says: change settings.json hook command to `python ~/.claude/hooks/quota_check.py`.
- Verified in `settings.json` L29 the existing `bash ~/.claude/pm-update.sh reset` works **only because bash is the program being invoked and bash itself expands `~`**. A bare `python ~/.claude/...` runs CPython's argv parser, which on Windows passes `~/.claude/hooks/quota_check.py` literally to `os.open`. Python does **not** expand `~` in argv. The hook will fail with `FileNotFoundError` on every prompt.
- Existing precedent in this same file: line 8 uses `pathlib.Path.home()` precisely because `~` is not portable in argv.
- **Fix required**: use one of
  - `python %USERPROFILE%\.claude\hooks\quota_check.py` (Windows-only, breaks macOS/Linux symmetry)
  - `python -c "import runpy,pathlib; runpy.run_path(str(pathlib.Path.home()/'.claude'/'hooks'/'quota_check.py'))"` (cross-platform but reintroduces an inline Python wrapper — somewhat defeating A1a's purpose)
  - Or shell out via `bash -c 'python ~/.claude/hooks/quota_check.py'` (requires bash on PATH; matches the pm-update.sh pattern).
- This is the single biggest implementation hazard. Combined with fail-open (N-102), the failure mode is silent: hook errors → fail-open → never warns → user thinks they're always green → exact behaviour v1 was supposed to fix.

### N-102 — 🟠 Fail-open masks real RED + masks N-101's failure
- A1a says "try/except fail-open." Combined with N-101, a broken file path raises `FileNotFoundError` → caught → silent exit → no RED ever fires. The user has no signal that the hook is dead. The whole observation week (Phase A) silently collects zero events and the rollout decision is made on an empty dataset.
- Other fail-open footguns: corrupted `usage-cache.json` (json.JSONDecodeError) → fail-open → user runs near 100% with no warning.
- **Fix required**: Phase A1b's smoke test must include a *negative* case proving the hook actually executes (e.g. log to a sentinel file on every invocation, not only on RED). Alternatively: fail-open should still write a one-line stderr breadcrumb that the user notices in Claude Code's debug output. At minimum, phase A2 rollout criteria should add "logged event count > 0 after 24h" as a sanity gate.

### N-103 — 🟠 Rotation race window
- A1c rotation is described as "append, stat-and-rename if >1MB." Concurrent prompts (two Claude Code sessions, or hook re-entrancy) hit:
  1. Process X stats file at 1.05MB, calls rename → file becomes `.1`.
  2. Process Y had file handle open in append mode pre-rename; on Windows, rename of an open file fails (ERROR_SHARING_VIOLATION). On POSIX, X's rename succeeds but Y now writes to the renamed file, losing data.
- Fix: either (a) skip rotation entirely and rely on user occasional cleanup (it's a 7-day window, 1MB caps risk of unbounded only marginal), or (b) wrap append+rotate in a per-process lock file. Given Phase A is one week, (a) is cheaper.

### N-104 — 🟠 do.md "advisory display" has no enforcement
- Plan B1 says do.md report adds "💡 Advisory: N notes". Verified do.md L281+ is the report template Claude reads at runtime. do.md is a prompt, not code — Claude *might* render advisory_notes if instructed, but there is no parser, no test, and no fallback if Claude forgets. Compare to `verdict`/`rounds`/`issues` which are also instructions-only and which Claude already inconsistently surfaces.
- **Implication**: B1's "observability via do.md report" is soft. The hard observability is the JSON-lines emission in cmd_deep (which *is* code and *is* enforceable). Plan should treat the do.md edit as best-effort and the JSON-lines emission as the source of truth for any retrospective. State that explicitly so future audits don't trust the rendered report.

### N-105 — 🟡 strip_full_fence + Windows CRLF
- Proposed regex: `^\s*` + triple-backtick + `[\w+-]*\n(.*)\n` + triple-backtick + `\s*$` with DOTALL.
- Python's `re.DOTALL` makes `.` match `\n` and `\r`. The literal `\n` in the pattern matches LF only, not CRLF. Gemini outputs LF, so it usually works. But on Windows, if the model output ever round-trips through PowerShell or `text=True` subprocess decoding with universal newlines disabled, the trailing `\r` before `\n` will cause the fence-close `\n` + triple-backtick to not match.
- **Fix**: use `\r?\n` for both newlines in the pattern, or call `text.replace('\r\n', '\n')` first. Trivial but necessary.

### N-106 — 🟡 install.ps1 hooks directory copy not in current script
- Verified install.ps1 L1-166: there is **no** `hooks` block. Plan A1a says "改 install.ps1 複製 hooks 目錄" — feasible (skills block at L113-127 is the obvious template), but the plan doesn't specify *what* to copy. A `hooks/` directory must:
  1. Be created in the repo first (currently does not exist — verified by absence of any `hooks` reference outside settings.json).
  2. Have `install.ps1` create `~/.claude/hooks/` if missing.
  3. Have a parallel block added to `install.sh` (the plan only mentions install.ps1).
- Minor scope creep risk: `install.sh` is mentioned in CLAUDE.md as the macOS/Linux installer; if it's not updated, cross-platform users break. Add to A1a checklist.

### N-107 — 🟡 The 70 "compromise" is still a guess
- C1's middle branch (10-25% in 60-80 band → switch to 70) is, as the prompt itself notes, a feel-based number with the same epistemics as v1's rejected 60. The honest response is: either commit to "we will not change the threshold unless the data is unambiguous (>25%)" — i.e. delete the 70 branch — or pre-register why 70 specifically (e.g. "halfway between 60 and 80, conservative bias toward fewer false positives"). v3 currently does neither; it just smuggles 70 in as a third bucket.
- Recommendation: drop the 70 branch. Two outcomes only — change to 60 or don't change. Cleaner decision, fewer post-hoc rationalizations.

### N-108 — 🟡 do.md L73 still claims Claude parses "last line"
- do.md L73: "Claude Code 解析最後一行取 `final`...". With B1 adding `advisory_notes` to the round emissions and possibly to the final emission, the "last line" structure must remain stable. If advisory_notes is added to the *round 2* emit but not to the *final* emit, fine. If added to final, do.md needs to enumerate the new field so Claude knows to read it.
- Trivial; just spell out which JSON-lines record carries advisory_notes.

---

## Uncovered Risks (carried forward)

1. **install.ps1 redeploy clobbers local edits to settings.json**: still un-mitigated since v1. Phase A1a forces a redeploy. If user has hand-edited their `~/.claude/settings.json` outside the repo, it gets backed up to `.bak` (good) but overwritten (expected). Worth a one-line note in the rollout doc.
2. **No B1 effect-measurement plan**: v3 emits advisory_notes but doesn't define how to evaluate whether they were useful. Same gap v2 had — accepted, but should be acknowledged.
3. **Phase A → C calendar gate**: v2 raised this; v3 says "視 Phase A 一週資料" — still no minimum-event threshold. Combined with N-102 (silent zero-event scenario), this is a real risk.

---

## Scores (1-5)

| Dimension | Score | Notes |
|---|:---:|---|
| Accuracy (paths, file refs) | **3** | Correctly identifies install.ps1 needs change; misses the `~` expansion bug (N-101) and the missing `hooks/` dir (N-106). do.md "advisory display" mis-trusts a prompt as enforceable. |
| Feasibility | **3** | Will fail at A1b smoke test (N-101). After fixing path, will probably pass. Rotation race (N-103) only matters under load. CRLF (N-105) only matters cross-platform. |
| Completeness | **4** | Phase gates well-defined, smoke test before logging, B1/B2 each have a concrete observable change. install.sh and the empty-dataset failure mode are gaps. |
| Risk honesty | **5** | Maintains v2's strong epistemic posture: explicit non-goals (C2), explicit limitations in A2, no fabricated numbers. The 70 compromise is the only soft spot. |

**Overall: REVISE.** Three required fixes, then APPROVE:

1. **N-101 (blocker)**: Replace `python ~/.claude/hooks/quota_check.py` with a form that actually finds the file on Windows. Recommend `bash -c 'python ~/.claude/hooks/quota_check.py'` to match the existing pm-update.sh precedent in settings.json L29, or have Phase A1a's hook command use `%USERPROFILE%` on Windows + a parallel POSIX form. Verify in A1b smoke test by deliberately checking the hook fires (sentinel log line), not just by checking RED appears.
2. **N-102 (blocker)**: A1b's smoke test must prove the hook *executes*, not just that RED renders when injected. Add "log invocation count > 0 after 24h" to A2 rollout criteria. Otherwise N-101 plus fail-open gives a silent week of zero data.
3. **N-105 (one-line fix)**: Use `\r?\n` in strip_full_fence regex.

Recommended (not blocking):
- Drop the 70 fallback in C1 (N-107). Two outcomes only.
- Skip rotation in A1c (N-103) — for a 7-day window the disk hygiene benefit is not worth the race.
- Update install.sh in lockstep with install.ps1 for the hooks directory (N-106).
- Note in do.md report section that JSON-lines emission is the source of truth, do.md rendering is best-effort (N-104).
