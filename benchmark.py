"""
Benchmark: opencode CLI vs Gemini API
比較兩者在程式碼與文件產出的品質差異。
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
GEMINI_MODEL = os.environ.get("BENCH_MODEL", "gemini-3-flash-preview")
RESULTS_DIR = Path("benchmark-results")
OUTPUTS_DIR = RESULTS_DIR / "outputs"
OPENCODE_TIMEOUT = 180  # seconds

# ---------------------------------------------------------------------------
# 8 Example module sources (for Tasks 3A / 4B)
# ---------------------------------------------------------------------------
CALC_PY = Path("dual-engine/examples/calc.py").read_text(encoding="utf-8")
COUNTER_PY = Path("dual-engine/examples/counter.py").read_text(encoding="utf-8")
GREET_PY = Path("dual-engine/examples/greet.py").read_text(encoding="utf-8")
PASSGEN_PY = Path("dual-engine/examples/passgen.py").read_text(encoding="utf-8")
TEMP_PY = Path("dual-engine/examples/temp.py").read_text(encoding="utf-8")
WC_PY = Path("dual-engine/examples/wc.py").read_text(encoding="utf-8")
JSONF_PY = Path("dual-engine/examples/jsonf.py").read_text(encoding="utf-8")
B64_PY = Path("dual-engine/examples/b64.py").read_text(encoding="utf-8")

ALL_MODULES = f"""## calc.py
```python
{CALC_PY}
```

## counter.py
```python
{COUNTER_PY}
```

## greet.py
```python
{GREET_PY}
```

## passgen.py
```python
{PASSGEN_PY}
```

## temp.py
```python
{TEMP_PY}
```

## wc.py
```python
{WC_PY}
```

## jsonf.py
```python
{JSONF_PY}
```

## b64.py
```python
{B64_PY}
```
"""

# ---------------------------------------------------------------------------
# Task Definitions
# ---------------------------------------------------------------------------
TASKS = [
    # Axis 1: Simple Code
    {
        "id": "1a", "axis": "Simple Code", "name": "units.py",
        "type": "code",
        "spec": """Write a Python CLI tool `units.py` that converts between common units:
- km/miles, kg/lbs, liters/gallons
- Usage: python units.py <from_unit> <to_unit> <value>
- Print result to 2 decimal places
- Handle invalid unit pairs with clear error message
- Handle non-numeric values gracefully
Output ONLY the Python code, no explanation.""",
    },
    {
        "id": "1b", "axis": "Simple Code", "name": "mdtable.py",
        "type": "code",
        "spec": """Write a Python CLI tool `mdtable.py` that reads CSV from stdin and outputs a Markdown table.
- First row is header
- Align columns left
- Handle empty input gracefully (print nothing)
- Usage: cat data.csv | python mdtable.py
Output ONLY the Python code, no explanation.""",
    },
    # Axis 2: Complex Code
    {
        "id": "2a", "axis": "Complex Code", "name": "filesync.py",
        "type": "code",
        "spec": """Write a Python module `filesync.py` with these functions:
- scan_dir(path) -> dict mapping relative paths to MD5 hashes
- diff_dirs(source, target) -> dict with keys "added", "removed", "modified" (lists of paths)
- sync_dirs(source, target, dry_run=False) -> list of actions taken
  - Actions: copy new, overwrite modified, delete removed
  - dry_run=True: return actions without executing
- CLI: python filesync.py <source> <target> [--dry-run]
- Handle permission errors, missing dirs, symlinks (skip with warning)
- Include docstrings for all public functions
Output ONLY the Python code, no explanation.""",
    },
    {
        "id": "2b", "axis": "Complex Code", "name": "taskq.py",
        "type": "code",
        "spec": """Write a Python module `taskq.py` implementing an in-memory task queue:
- TaskQueue class with methods: submit(fn, *args, **kwargs) -> task_id, status(task_id) -> dict, results() -> list
- Tasks run in ThreadPoolExecutor (max_workers configurable)
- Auto-retry on exception (max 3 attempts, exponential backoff: 1s, 2s, 4s)
- Status returns: {"id": ..., "state": "pending|running|done|failed", "result": ..., "attempts": N, "error": ...}
- CLI demo: python taskq.py (runs 5 sample tasks, 2 of which randomly fail, shows status table)
- Include type hints throughout
Output ONLY the Python code, no explanation.""",
    },
    # Axis 3: Simple Docs
    {
        "id": "3a", "axis": "Simple Docs", "name": "README.md",
        "type": "docs",
        "spec": f"""Write a README.md for the following Python CLI calculator tool. Include: description, installation, usage examples (all 4 operations + error cases), API reference for format_output(), and a "Limitations" section.

```python
{CALC_PY}
```

Output ONLY the Markdown content.""",
    },
    {
        "id": "3b", "axis": "Simple Docs", "name": "CHANGELOG.md",
        "type": "docs",
        "spec": """Write a CHANGELOG.md entry (Keep a Changelog format) for version 0.2.0 of a CLI toolkit that added these changes:
- Added: password generator (passgen.py) with --length and --no-symbols flags
- Added: base64 encoder/decoder (b64.py) supporting stdin pipe
- Changed: calc.py now handles infinity/NaN without crashing (was OverflowError)
- Fixed: counter.py race condition when multiple instances write .counter.json simultaneously

Write clear, user-facing descriptions. Do not just repeat the bullet points -- expand each with context.
Output ONLY the Markdown content.""",
    },
    # Axis 4: Complex Docs
    {
        "id": "4a", "axis": "Complex Docs", "name": "ADR.md",
        "type": "docs",
        "spec": """Write an ADR (Architecture Decision Record) for the following decision:

Context: We have a CLI task delegation system where Claude Code writes specs and opencode executes them. We are considering migrating from opencode CLI to LangGraph + Gemini API.

The current system: pipes specs to opencode CLI, which uses Gemini models internally. It works but has limitations: linear flow only, no state persistence across sessions, no conditional routing.

The proposed system: LangGraph graph with nodes for classify/execute/validate/report, direct Gemini API calls, SQLite state persistence, conditional retry logic.

Write the ADR with sections: Title, Status, Context, Decision, Consequences (positive and negative), Alternatives Considered. Use Markdown. Be specific and technical.
Output ONLY the Markdown content.""",
    },
    {
        "id": "4b", "axis": "Complex Docs", "name": "API-Reference.md",
        "type": "docs",
        "spec": f"""Write comprehensive API reference documentation for the following 8 Python CLI modules. For each module, document: purpose, CLI usage, all functions with signatures and parameter descriptions, return values, error conditions, and examples.

{ALL_MODULES}

Output as a single Markdown document with table of contents, consistent formatting, and cross-references where modules share patterns.
Output ONLY the Markdown content.""",
    },
]

# ---------------------------------------------------------------------------
# Runners
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = (
    "You are a skilled software engineer. Complete the following task. "
    "Output only the deliverable (code or documentation). "
    "Do not wrap code in markdown code fences unless the deliverable IS markdown."
)

OPENCODE_PREFIX = (
    "You must execute immediately. Do not plan, do not ask for confirmation. "
    "Complete the following task and output only the deliverable (code or documentation). "
    "Do not wrap in markdown code fences unless the deliverable IS markdown."
)


def run_gemini_api(spec: str) -> str:
    """Runner B: Direct Gemini API call."""
    from google import genai

    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    prompt = f"{SYSTEM_PROMPT}\n\n{spec}"
    response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
    return response.text


def run_opencode(spec: str) -> str:
    """Runner A: opencode CLI."""
    prompt = f"{OPENCODE_PREFIX}\n\n{spec}"
    try:
        result = subprocess.run(
            ["opencode", "run", "--format", "json"],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=OPENCODE_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return "[TIMEOUT]"
    except FileNotFoundError:
        return "[OPENCODE_NOT_FOUND]"

    # Parse opencode JSON output — extract assistant text
    output = result.stdout
    if not output.strip():
        return result.stderr or "[EMPTY_OUTPUT]"

    # opencode --format json outputs JSONL: {"type":"text","part":{"text":"..."}}
    text_parts = []
    for line in output.strip().splitlines():
        try:
            evt = json.loads(line)
            if isinstance(evt, dict) and evt.get("type") == "text":
                part = evt.get("part", {})
                if isinstance(part, dict) and "text" in part:
                    text_parts.append(part["text"])
        except json.JSONDecodeError:
            pass

    return "\n".join(text_parts) if text_parts else output


def extract_code(text: str) -> str:
    """Strip markdown code fences if present."""
    # Match ```python ... ``` or ``` ... ```
    m = re.search(r"```(?:python)?\s*\n(.*?)```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return text.strip()


# ---------------------------------------------------------------------------
# Auto-test for code tasks
# ---------------------------------------------------------------------------
def auto_test_code(task_id: str, code: str) -> dict:
    """Run automated tests on generated code. Returns {passed, total, details}."""
    results = {"passed": 0, "total": 0, "details": []}

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / f"{task_id}.py"
        filepath.write_text(extract_code(code), encoding="utf-8")

        if task_id == "1a":
            tests = [
                (["python", str(filepath), "km", "miles", "10"], "6.21", 0),
                (["python", str(filepath), "kg", "lbs", "1"], "2.20", 0),
                (["python", str(filepath), "km", "kg", "1"], None, 1),  # invalid pair
                (["python", str(filepath), "km", "miles", "abc"], None, 1),  # non-numeric
            ]
            for cmd, expected_out, expected_rc in tests:
                results["total"] += 1
                try:
                    r = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                    ok = r.returncode == expected_rc
                    if expected_out and ok:
                        ok = expected_out in r.stdout.strip()
                    results["details"].append(
                        f"{'PASS' if ok else 'FAIL'}: {' '.join(cmd[-3:])} -> rc={r.returncode} out={r.stdout.strip()[:50]}"
                    )
                    if ok:
                        results["passed"] += 1
                except Exception as e:
                    results["details"].append(f"ERROR: {e}")

        elif task_id == "1b":
            tests = [
                ("a,b\n1,2\n3,4", True),   # valid CSV
                ("", False),                 # empty input — should not crash
            ]
            for csv_input, expect_table in tests:
                results["total"] += 1
                try:
                    r = subprocess.run(
                        ["python", str(filepath)],
                        input=csv_input, capture_output=True, text=True, timeout=10,
                    )
                    if expect_table:
                        ok = "|" in r.stdout and r.returncode == 0
                    else:
                        ok = r.returncode == 0  # just don't crash
                    results["details"].append(
                        f"{'PASS' if ok else 'FAIL'}: input={'<csv>' if csv_input else '<empty>'} rc={r.returncode}"
                    )
                    if ok:
                        results["passed"] += 1
                except Exception as e:
                    results["details"].append(f"ERROR: {e}")

        elif task_id == "2a":
            # Create temp source/target dirs
            src = Path(tmpdir) / "src_dir"
            tgt = Path(tmpdir) / "tgt_dir"
            src.mkdir()
            tgt.mkdir()
            (src / "a.txt").write_text("hello")
            (src / "b.txt").write_text("world")
            (tgt / "a.txt").write_text("old")

            # Test dry-run
            results["total"] += 1
            try:
                r = subprocess.run(
                    ["python", str(filepath), str(src), str(tgt), "--dry-run"],
                    capture_output=True, text=True, timeout=15,
                )
                ok = r.returncode == 0
                results["details"].append(f"{'PASS' if ok else 'FAIL'}: dry-run rc={r.returncode}")
                if ok:
                    results["passed"] += 1
            except Exception as e:
                results["details"].append(f"ERROR: {e}")

            # Test actual sync
            results["total"] += 1
            try:
                r = subprocess.run(
                    ["python", str(filepath), str(src), str(tgt)],
                    capture_output=True, text=True, timeout=15,
                )
                ok = r.returncode == 0
                results["details"].append(f"{'PASS' if ok else 'FAIL'}: sync rc={r.returncode}")
                if ok:
                    results["passed"] += 1
            except Exception as e:
                results["details"].append(f"ERROR: {e}")

        elif task_id == "2b":
            # Just run the demo
            results["total"] += 1
            try:
                r = subprocess.run(
                    ["python", str(filepath)],
                    capture_output=True, text=True, timeout=30,
                )
                ok = r.returncode == 0
                results["details"].append(
                    f"{'PASS' if ok else 'FAIL'}: demo rc={r.returncode} out_len={len(r.stdout)}"
                )
                if ok:
                    results["passed"] += 1
            except Exception as e:
                results["details"].append(f"ERROR: {e}")

    return results


# ---------------------------------------------------------------------------
# Scoring helpers
# ---------------------------------------------------------------------------
def composite_score(correctness: float, completeness: float, quality: float) -> float:
    return round(correctness * 0.4 + completeness * 0.3 + quality * 0.3, 2)


def auto_correctness_score(passed: int, total: int) -> int:
    """Map pass rate to 1-5 score."""
    if total == 0:
        return 3
    ratio = passed / total
    if ratio >= 1.0:
        return 5
    elif ratio >= 0.75:
        return 4
    elif ratio >= 0.5:
        return 3
    elif ratio >= 0.25:
        return 2
    else:
        return 1


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------
def generate_report(all_results: dict) -> str:
    lines = [
        f"# Benchmark Results: opencode vs Gemini API",
        f"Date: {time.strftime('%Y-%m-%d %H:%M')}",
        f"Gemini Model: {GEMINI_MODEL}",
        f"opencode Model: gemini-3-flash-preview",
        "",
        "## Scores",
        "",
        "| Axis | Task | Runner | Correctness | Completeness | Quality | Composite |",
        "|------|------|--------|-------------|--------------|---------|-----------|",
    ]

    axis_scores = {}
    for task in TASKS:
        tid = task["id"]
        for runner in ["gemini", "opencode"]:
            key = f"{tid}-{runner}"
            scores = all_results.get(key, {})
            c = scores.get("correctness", "?")
            comp = scores.get("completeness", "?")
            q = scores.get("quality", "?")
            cs = scores.get("composite", "?")
            lines.append(f"| {task['axis']} | {task['name']} | {runner} | {c} | {comp} | {q} | {cs} |")

            if isinstance(cs, (int, float)):
                axis_scores.setdefault(task["axis"], {}).setdefault(runner, []).append(cs)

    lines.extend(["", "## Summary by Axis", "",
        "| Axis | opencode avg | gemini avg | Delta |",
        "|------|-------------|------------|-------|"])

    overall = {"gemini": [], "opencode": []}
    for axis in ["Simple Code", "Complex Code", "Simple Docs", "Complex Docs"]:
        for runner in ["gemini", "opencode"]:
            vals = axis_scores.get(axis, {}).get(runner, [])
            overall[runner].extend(vals)
        oc_vals = axis_scores.get(axis, {}).get("opencode", [])
        gm_vals = axis_scores.get(axis, {}).get("gemini", [])
        oc_avg = round(sum(oc_vals) / len(oc_vals), 2) if oc_vals else "?"
        gm_avg = round(sum(gm_vals) / len(gm_vals), 2) if gm_vals else "?"
        delta = round(gm_avg - oc_avg, 2) if isinstance(gm_avg, float) and isinstance(oc_avg, float) else "?"
        lines.append(f"| {axis} | {oc_avg} | {gm_avg} | {delta:+.2f} |" if isinstance(delta, float) else f"| {axis} | {oc_avg} | {gm_avg} | {delta} |")

    oc_total = round(sum(overall["opencode"]) / len(overall["opencode"]), 2) if overall["opencode"] else "?"
    gm_total = round(sum(overall["gemini"]) / len(overall["gemini"]), 2) if overall["gemini"] else "?"
    delta_total = round(gm_total - oc_total, 2) if isinstance(gm_total, float) and isinstance(oc_total, float) else "?"
    d_str = f"{delta_total:+.2f}" if isinstance(delta_total, float) else str(delta_total)
    lines.append(f"| **Overall** | **{oc_total}** | **{gm_total}** | **{d_str}** |")

    # Verdict
    lines.extend(["", "## Verdict", ""])
    if isinstance(delta_total, float):
        if delta_total >= -0.3:
            lines.append("**Gemini API quality is comparable or better.** LangGraph migration is viable.")
        elif delta_total >= -0.7:
            lines.append("**Gemini API is slightly weaker.** Investigate weak axes; prompt engineering may help.")
        else:
            lines.append("**Gemini API is significantly weaker.** Pause migration; opencode orchestration adds substantial value.")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    RESULTS_DIR.mkdir(exist_ok=True)
    OUTPUTS_DIR.mkdir(exist_ok=True)

    all_results = {}
    auto_test_log = []

    # Parse CLI args
    run_gemini_only = "--gemini-only" in sys.argv
    run_opencode_only = "--opencode-only" in sys.argv
    score_only = "--score-only" in sys.argv

    # --score-only: read scores.json and regenerate report only
    if score_only:
        scores_path = RESULTS_DIR / "scores.json"
        if scores_path.exists():
            all_results = json.loads(scores_path.read_text(encoding="utf-8"))
        report = generate_report(all_results)
        (RESULTS_DIR / "scores.md").write_text(report, encoding="utf-8")
        print("Report regenerated from scores.json")
        print(report)
        return

    runners = []
    if run_gemini_only:
        runners = ["gemini"]
    elif run_opencode_only:
        runners = ["opencode"]
    else:
        runners = ["gemini", "opencode"]

    # --- Run tasks ---
    for runner in runners:
        print(f"\n{'='*60}")
        print(f"Running: {runner.upper()}")
        print(f"{'='*60}")
        for task in TASKS:
            tid = task["id"]
            ext = ".py" if task["type"] == "code" else ".md"
            outfile = OUTPUTS_DIR / f"{tid}-{task['name'].replace('.py','').replace('.md','')}-{runner}{ext}"

            print(f"\n  [{tid}] {task['name']} ... ", end="", flush=True)
            start = time.time()

            if runner == "gemini":
                output = run_gemini_api(task["spec"])
            else:
                output = run_opencode(task["spec"])

            elapsed = time.time() - start
            outfile.write_text(output, encoding="utf-8")
            print(f"done ({elapsed:.1f}s, {len(output)} chars)")

    # --- Auto-test code tasks ---
    print(f"\n{'='*60}")
    print("Auto-testing code outputs")
    print(f"{'='*60}")

    for task in TASKS:
        if task["type"] != "code":
            continue
        tid = task["id"]
        for runner in ["gemini", "opencode"]:
            ext = ".py"
            outfile = OUTPUTS_DIR / f"{tid}-{task['name'].replace('.py','')}-{runner}{ext}"
            if not outfile.exists():
                auto_test_log.append(f"[{tid}-{runner}] SKIP: output file not found")
                continue

            code = outfile.read_text(encoding="utf-8")
            print(f"\n  [{tid}-{runner}] {task['name']} ... ", end="", flush=True)
            test_result = auto_test_code(tid, code)
            passed = test_result["passed"]
            total = test_result["total"]
            score = auto_correctness_score(passed, total)
            print(f"{passed}/{total} passed (correctness={score})")

            key = f"{tid}-{runner}"
            all_results[key] = {"correctness": score}
            auto_test_log.append(f"[{tid}-{runner}] {passed}/{total} passed, correctness={score}")
            for d in test_result["details"]:
                auto_test_log.append(f"  {d}")

    # --- Manual scoring prompt ---
    print(f"\n{'='*60}")
    print("Manual scoring needed for all tasks")
    print(f"{'='*60}")
    print("\nFor each task, review outputs in benchmark-results/outputs/")
    print("Score Completeness (1-5) and Quality (1-5)")
    print("For docs tasks, also score Correctness (1-5)\n")

    for task in TASKS:
        tid = task["id"]
        for runner in ["gemini", "opencode"]:
            key = f"{tid}-{runner}"
            if key not in all_results:
                all_results[key] = {}

            existing = all_results[key]
            if "correctness" not in existing and task["type"] == "docs":
                # Docs tasks need manual correctness too
                existing["correctness"] = "?"
            existing.setdefault("completeness", "?")
            existing.setdefault("quality", "?")
            existing.setdefault("composite", "?")

    # Save auto-test log
    (RESULTS_DIR / "auto-tests.md").write_text(
        "# Auto-Test Results\n\n```\n" + "\n".join(auto_test_log) + "\n```\n",
        encoding="utf-8",
    )

    # Save partial scores (auto-test only)
    scores_path = RESULTS_DIR / "scores.json"
    scores_path.write_text(json.dumps(all_results, indent=2, ensure_ascii=False), encoding="utf-8")

    # Generate report
    report = generate_report(all_results)
    (RESULTS_DIR / "scores.md").write_text(report, encoding="utf-8")

    print(f"\nResults saved to {RESULTS_DIR}/")
    print(f"  scores.md — comparison table")
    print(f"  scores.json — raw scores (edit manually, then re-run with --score-only)")
    print(f"  auto-tests.md — automated test details")
    print(f"  outputs/ — all 16 output files")


if __name__ == "__main__":
    main()
