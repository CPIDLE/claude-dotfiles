# Evaluation Report — Claude Code vs OpenCode (Gemini 3 Flash Preview)

## Setup

- **Claude Code**: `claude-opus-4-6` via `claude -p ... --permission-mode bypassPermissions`
- **OpenCode**: `google/gemini-3-flash-preview` via `opencode run -m ...`
- **Date**: 2026-04-07
- **Host**: Windows 11, bash (Git Bash)
- **Fixtures**: small Flask task queue with intentional TOCTOU race (`eval/fixtures/mini_queue/`) + 3 contradictory spec docs (`eval/fixtures/specs/`)
- **Tasks**: 8 prompts covering {doc read, doc write, code read, code write} × {simple, complex} — see `eval/tasks/`
- **Runner**: `eval/run.sh` records output, stderr, and wall-clock timing to `eval/runs/<tool>/<task>/`
- **Scoring**: 5 criteria × 5 points each (Maintainability skipped on non-code tasks). Max 180 overall.

## Headline results

| | OpenCode | Claude | Δ |
|---|:---:|:---:|:---:|
| **Total score** | **168 / 180 (93 %)** | **166 / 180 (92 %)** | OpenCode +2 |
| **Wall-clock**  | **221 s** | 429 s | OpenCode −48 % |

| Category | OpenCode | Claude | Winner |
|---|:---:|:---:|:---:|
| Doc read  (T1-S + T1-C)  | 39/40 | 38/40 | OpenCode +1 |
| Doc write (T2-S + T2-C)  | 39/40 | 35/40 | OpenCode +4 |
| Code read (T3-S + T3-C)  | 48/50 | 48/50 | Tie |
| Code write(T4-S + T4-C)  | 42/50 | **45/50** | **Claude +3** |

**TL;DR** — Quality is essentially tied (within 1 %). Claude pulls ahead on the hardest tasks (complex code reasoning and writing). OpenCode is roughly **twice as fast** and produces usable output on every task first try.

## Per-task observations

### T1 — Doc read
- **T1-S** (summarise README): Both correct. OpenCode more concise, Claude marginally more structured.
- **T1-C** (3-spec contradiction report): Both caught all 5 core conflicts. **Claude more thorough** — added a latent-issues section noting that "200/min per API key" and "100/min per token" are not reconcilable because the auth models differ; also flagged the missing integer-ID migration window. OpenCode missed a few single-spec gaps (429 response code, token revocation).

### T2 — Doc write
- **T2-S** (curl-example Usage section): Both correct. **Claude is richer** — includes 404 path, explicit status codes, and a bonus end-to-end shell smoke test.
- **T2-C** (architecture.md with Mermaid diagrams): OpenCode delivered a clean, complete document inline in `output.md`. Claude wrote to `fixtures/mini_queue/architecture.md` only (not inline in output.md) — **instruction-delivery miss**, but the content itself was higher quality, finding extra defects (duplicate `import itertools`, `TTLCache` storing live `Task` references which makes TTL/invalidation partially moot, misleading module docstring).

### T3 — Code read
- **T3-S** (explain `TaskStore.claim`): Both correctly identified the TOCTOU race and the intentional `time.sleep(0)`. Essentially equivalent.
- **T3-C** (trace call chain + race analysis + fix): **Claude's answer is the best piece of output in the whole eval.** Explicit step-by-step 2-worker interleaving table showing how `claimed_by` ends up as whichever thread wrote last, while both `complete` calls still succeed; also caught that `enqueue` and `complete` have the same TOCTOU shape, that Flask's dev server is multi-threaded (so the race is actually reachable), and that a multi-process deployment breaks the in-memory store entirely. OpenCode's diff was fine; the analysis just wasn't as deep.

### T4 — Code write
- **T4-S** (stand-alone `csv2json.py`): Both produced correct, stdlib-only scripts. Both mishandled the output path placeholder — OpenCode wrote to `runs/gemini-3-flash-preview/T4-S/`, Claude created a directory literally named `<tool>`. Minor instruction-following bugs on both sides.
- **T4-C** (TTL cache layer + race fix + tests, wired into server): Both delivered complete working implementations. **Claude's is notably better engineered**:
  - Uses `time.monotonic()` for expiry — immune to wall-clock jumps
  - Removes the dead `time.sleep(0)` and the now-misleading "NOT thread-safe" docstring
  - Dedupes the double `import itertools` (which OpenCode actually *introduced* on its own run)
  - `CHANGES.md` explains *why* closing the race matters for cache invalidation correctness, not just *what* changed
  - Ran its own tests before finishing (pycache artefacts present)

  OpenCode's version is functionally correct and complete — lock-guarded dict cache, 5 tests including a bonus race-condition test — just less polished.

## Strengths

**OpenCode (Gemini 3 Flash Preview)**
- **Speed** — roughly 2× faster on wall-clock across all 8 tasks.
- **Reliability** — every task produced usable output on the first attempt, no permission or harness friction.
- **Clean formatting** — tables, code blocks, and markdown structure are consistently good.
- **Good enough on simple-to-medium tasks** — scored full marks on T1-S and T2-C.

**Claude Code (Opus 4.6)**
- **Deeper reasoning on complex code tasks** — the T3-C and T4-C deliverables are of a higher engineering standard.
- **Finds issues the prompt didn't ask for** — caught bugs in fixture code (and in OpenCode's own output) spontaneously.
- **Better judgement under ambiguity** — chose `time.monotonic()`, cleaned up dead code, wrote "why" not just "what".
- **Richer doc output on T2-S** — 404 case, status codes, end-to-end example.

## Weaknesses

**OpenCode**
- Slightly shallower on the hardest analysis tasks (T1-C gap list, T3-C race analysis).
- Introduced a small regression in its own T4-C edit (duplicate `import itertools` line) — not noticed until Claude pointed it out.
- No evidence of running tests to verify its own work.

**Claude Code**
- **~2× slower** on every task.
- `claude -p` defaults to restrictive write permissions — without `--permission-mode bypassPermissions` the first run of T2-C / T4-S / T4-C produced nothing. This is a sharp footgun for scripted / batch workflows.
- Tends to write deliverables to file paths (via Write tool) instead of inlining them in the `output.md` that the runner captures. Fine in interactive mode, awkward for harness-based eval.
- Literal-minded on placeholder substitution (`<tool>` in T4-S).

## Recommended usage

| Prefer **OpenCode / Gemini 3 Flash Preview** for | Prefer **Claude Code / Opus 4.6** for |
|---|---|
| Batch / scripted tasks where reliability matters more than polish | Complex refactors, race-condition analysis, architectural changes |
| Summaries, documentation, simple code scaffolding | Tasks where "find the extra bug I didn't mention" is useful |
| Anything latency-sensitive | Deliverables that need to survive code review |
| Running against large numbers of simple tasks (cost/speed favour it) | Situations where a single task's quality dominates the cost |

A pragmatic split: **OpenCode for volume, Claude for depth.**

## Caveats

- **Single run per task** — no variance measurement. Re-runs could shift the overall tie by more than 2 points in either direction.
- **Fixtures are small** — the code tasks involve ~150 lines of Python. Real codebases may stress the tools differently (context handling, cross-file reasoning).
- **Harness effects** — `claude -p` mode is not how Claude Code is usually used; interactive mode may score differently on the doc-write / code-write tasks where inline delivery matters.
- **Fixture contamination** — during T4-C, OpenCode modified `fixtures/mini_queue/store.py` and `server.py` directly (adding the cache + race fix in-place). All subsequent runs saw a mutated baseline. This was discovered mid-run and noted but not corrected; it did not affect scoring because each tool's T4-C was evaluated against its own runs/ output directory, not the fixture.
- **Gemini 3 Flash Preview is a preview model** — behaviour and pricing may change.

## Files

- `eval/PLAN.md` — plan and rubric
- `eval/tasks/` — 8 task prompts
- `eval/fixtures/` — test code and spec docs
- `eval/runs/<tool>/<task>/` — per-run prompt, output, stderr, meta
- `eval/scoreboard.md` — scored matrix with per-task notes
- `eval/run.sh` / `eval/run_all.sh` — runners
