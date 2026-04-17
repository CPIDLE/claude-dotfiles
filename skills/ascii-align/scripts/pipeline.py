#!/usr/bin/env python3
"""pipeline.py — Multi-round ASCII art fix pipeline state manager.

Pipeline per file (max 6 rounds):

  Round 1:
    sample_XXX.md  → copy → _sample_XXX.md
    gen_prompt     → sample_XXX.prompt.txt
    fix agent      → modifies _sample_XXX.md (self-verify with --check)
    rename         → v_sample_XXX.md
    review agent   → reads v_ + sample_XXX.review.txt
      PASS         → p_sample_XXX.md   (done)
      FAIL         → x_sample_XXX.md  + append issues to prompt.txt

  Round 2:  x_  → fix agent → vv_    → review → pp_    or  xx_    + update prompt
  Round 3:  xx_ → fix agent → vvv_   → review → ppp_   or  xxx_
  Round 4: xxx_ → fix agent → vvvv_  → review → pppp_  or  xxxx_
  Round 5: xxxx_→ fix agent → vvvvv_ → review → ppppp_ or  xxxxx_
  Round 6: xxxxx_→fix agent →vvvvvv_→ review → pppppp_ or  xxxxxx_ (STOP)

  NOTE: after-fix N automatically globs the correct source prefix for round N.
  E.g. after-fix 2 picks up x_sample_*.md (not _sample_*.md).

Usage:
    python pipeline.py status [dir]          # show current state of all files
    python pipeline.py prep   [dir]          # copy sample_*.md → _sample_*.md + gen_prompt
    python pipeline.py after-fix  <round> [dir]  # rename _→v/vv/vvv after fix agent runs
    python pipeline.py after-review <round> [dir] <results_file>
                                             # apply review results (PASS/FAIL) → rename + update prompt
    python pipeline.py gen-review [dir]      # generate .review.txt for pending v_/vv_/vvv_ files
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# ---------------------------------------------------------------------------
# State prefix conventions
# ---------------------------------------------------------------------------

# Maps (round, state) → prefix
#   state: 'pending_fix' | 'pending_review' | 'pass' | 'fail'
_PREFIX = {
    (1, "pending_fix"):    "_",
    (1, "pending_review"): "v_",
    (1, "pass"):           "p_",
    (1, "fail"):           "x_",
    (2, "pending_fix"):    "x_",   # x_ files feed into round 2 fix
    (2, "pending_review"): "vv_",
    (2, "pass"):           "pp_",
    (2, "fail"):           "xx_",
    (3, "pending_fix"):    "xx_",
    (3, "pending_review"): "vvv_",
    (3, "pass"):           "ppp_",
    (3, "fail"):           "xxx_",
    (4, "pending_fix"):    "xxx_",
    (4, "pending_review"): "vvvv_",
    (4, "pass"):           "pppp_",
    (4, "fail"):           "xxxx_",
    (5, "pending_fix"):    "xxxx_",
    (5, "pending_review"): "vvvvv_",
    (5, "pass"):           "ppppp_",
    (5, "fail"):           "xxxxx_",
    (6, "pending_fix"):    "xxxxx_",
    (6, "pending_review"): "vvvvvv_",
    (6, "pass"):           "pppppp_",
    (6, "fail"):           "xxxxxx_",
}

_ALL_PREFIXES = ("pppppp_", "xxxxxx_", "ppppp_", "xxxxx_", "pppp_", "xxxx_", "vvvvvv_", "vvvvv_", "vvvv_", "ppp_", "xxx_", "pp_", "xx_", "vvv_", "vv_", "p_", "x_", "v_", "_")


def _strip_prefix(name: str) -> str:
    for pfx in _ALL_PREFIXES:
        if name.startswith(pfx):
            return name[len(pfx):]
    return name


def _detect_prefix(name: str) -> str:
    for pfx in _ALL_PREFIXES:
        if name.startswith(pfx):
            return pfx
    return ""


def _prompt_path(base_name: str, directory: Path) -> Path:
    """Return path to the .prompt.txt file for a given base filename."""
    stem = Path(base_name).stem  # e.g. sample_123
    return directory / f"{stem}.prompt.txt"


def _review_path(base_name: str, directory: Path) -> Path:
    stem = Path(base_name).stem
    return directory / f"{stem}.review.txt"


# ---------------------------------------------------------------------------
# status
# ---------------------------------------------------------------------------

def cmd_status(directory: Path) -> None:
    counts: dict[str, int] = {}
    for p in sorted(directory.glob("*.md")):
        pfx = _detect_prefix(p.name)
        if pfx:
            counts[pfx] = counts.get(pfx, 0) + 1

    print(f"Directory: {directory}")
    order = [
        "_",
        "v_", "vv_", "vvv_", "vvvv_", "vvvvv_", "vvvvvv_",
        "p_", "pp_", "ppp_", "pppp_", "ppppp_", "pppppp_",
        "x_", "xx_", "xxx_", "xxxx_", "xxxxx_", "xxxxxx_",
    ]
    label = {
        "_":        "R1 pending fix",
        "v_":       "R1 pending review",
        "p_":       "R1 PASS",
        "x_":       "R1 FAIL → R2 fix",
        "vv_":      "R2 pending review",
        "pp_":      "R2 PASS",
        "xx_":      "R2 FAIL → R3 fix",
        "vvv_":     "R3 pending review",
        "ppp_":     "R3 PASS",
        "xxx_":     "R3 FAIL → R4 fix",
        "vvvv_":    "R4 pending review",
        "pppp_":    "R4 PASS",
        "xxxx_":    "R4 FAIL → R5 fix",
        "vvvvv_":   "R5 pending review",
        "ppppp_":   "R5 PASS",
        "xxxxx_":   "R5 FAIL → R6 fix",
        "vvvvvv_":  "R6 pending review",
        "pppppp_":  "R6 PASS",
        "xxxxxx_":  "R6 FAIL (manual)",
    }
    for pfx in order:
        n = counts.get(pfx, 0)
        if n:
            print(f"  {pfx:10s}  {n:3d}  {label[pfx]}")

    done = sum(counts.get(p, 0) for p in ("p_", "pp_", "ppp_", "pppp_", "ppppp_", "pppppp_"))
    manual = counts.get("xxxxxx_", 0)
    inflight = sum(counts.get(p, 0) for p in (
        "_", "v_", "x_", "vv_", "xx_", "vvv_", "xxx_",
        "vvvv_", "xxxx_", "vvvvv_", "xxxxx_", "vvvvvv_",
    ))
    print(f"\n  DONE={done}  IN-FLIGHT={inflight}  MANUAL={manual}")


# ---------------------------------------------------------------------------
# prep: copy sample_*.md → _sample_*.md + gen_prompt
# ---------------------------------------------------------------------------

def cmd_prep(directory: Path) -> None:
    from gen_prompt import gen_file_prompt, RULES_FILENAME, _RULES_CONTENT
    from symbol_fix import replace_symbols, find_illegal

    sources = sorted(directory.glob("sample_*.md"))
    if not sources:
        print("No sample_*.md files found.")
        return

    rules_out = directory / RULES_FILENAME
    rules_out.write_text(_RULES_CONTENT, encoding="utf-8", newline="\n")
    print(f"RULES  {rules_out.name}")

    for src in sources:
        dst = directory / f"_{src.name}"
        if dst.exists():
            print(f"SKIP   {dst.name} (already exists)")
            continue
        shutil.copy2(src, dst)
        # Apply symbol_fix to the working copy so illegal w2 symbols
        # don't cause alignment oscillation during the fix rounds.
        content = dst.read_text(encoding="utf-8")
        fixed = replace_symbols(content)
        if fixed != content:
            dst.write_text(fixed, encoding="utf-8", newline="\n")
        prompt_text = gen_file_prompt(dst)
        prompt_out = _prompt_path(src.stem, directory)
        prompt_out.write_text(prompt_text, encoding="utf-8", newline="\n")
        print(f"PREP   {dst.name}  →  {prompt_out.name}")


# ---------------------------------------------------------------------------
# after-fix: rename _ → v/vv/vvv based on round
# ---------------------------------------------------------------------------

def cmd_after_fix(directory: Path, rnd: int) -> None:
    target_prefix = _PREFIX[(rnd, "pending_review")]
    source_prefix = _PREFIX[(rnd, "pending_fix")]  # "_" for R1, "x_" for R2, etc.
    pending = sorted(directory.glob(f"{source_prefix}sample_*.md"))
    if not pending:
        print(f"No {source_prefix}sample_*.md files to rename.")
        return
    for p in pending:
        base = _strip_prefix(p.name)
        new = directory / f"{target_prefix}{base}"
        if new.exists():
            new.unlink()
        p.rename(new)
        print(f"RENAME {p.name} → {new.name}")


# ---------------------------------------------------------------------------
# gen-review: generate .review.txt for pending v_/vv_/vvv_ files
# ---------------------------------------------------------------------------

def cmd_gen_review(directory: Path) -> None:
    from llm_review import gen_review_prompt

    pending: list[Path] = []
    for prefix in ("vvvvvv_", "vvvvv_", "vvvv_", "vvv_", "vv_", "v_"):
        pending.extend(sorted(directory.glob(f"{prefix}sample_*.md")))

    if not pending:
        print("No v_/vv_/vvv_/vvvv_/vvvvv_/vvvvvv_ files pending review.")
        return

    for p in pending:
        prompt = gen_review_prompt(p)
        out = _review_path(_strip_prefix(p.name), directory)
        out.write_text(prompt, encoding="utf-8", newline="\n")
        print(f"REVIEW {out.name}")


# ---------------------------------------------------------------------------
# after-review: parse results file, rename files, update prompt.txt
# ---------------------------------------------------------------------------

# Results file format (one entry per file):
#
# === sample_XXX ===
# PASS
#
# === sample_YYY ===
# FAIL
# - L13: Rule D: CJK label row misalignment...
# - L39: Rule B: Stray connector...
#
# Corrections:
# L13: `    可平行         └─────────────┘        循序`

_SECTION_RE = re.compile(r"^=== (\S+) ===$", re.MULTILINE)


def _parse_results(text: str) -> dict[str, dict]:
    """Parse results file → {base_name: {status, issues, corrections}}"""
    results: dict[str, dict] = {}
    sections = _SECTION_RE.split(text)
    # sections = ['', name1, body1, name2, body2, ...]
    it = iter(sections[1:])
    for name, body in zip(it, it):
        name = name.strip()
        body = body.strip()
        status = "PASS" if body.startswith("PASS") else "FAIL"
        issues: list[str] = []
        corrections: list[str] = []
        in_corrections = False
        for line in body.splitlines():
            if line.startswith("Corrections:"):
                in_corrections = True
                continue
            if in_corrections:
                if line.strip():
                    corrections.append(line.strip())
            elif line.startswith("- L"):
                issues.append(line.strip())
        results[name] = {
            "status": status,
            "issues": issues,
            "corrections": corrections,
        }
    return results


def cmd_after_review(directory: Path, rnd: int, results_file: Path) -> None:
    text = results_file.read_text(encoding="utf-8")
    results = _parse_results(text)

    pass_prefix = _PREFIX[(rnd, "pass")]
    fail_prefix = _PREFIX[(rnd, "fail")]
    review_prefix = _PREFIX[(rnd, "pending_review")]

    for pending in sorted(directory.glob(f"{review_prefix}sample_*.md")):
        base = _strip_prefix(pending.name)
        stem = Path(base).stem  # sample_XXX

        r = results.get(stem, None)
        if r is None:
            print(f"SKIP   {pending.name} (no result in file)")
            continue

        if r["status"] == "PASS":
            new_path = directory / f"{pass_prefix}{base}"
            if new_path.exists():
                new_path.unlink()
            pending.rename(new_path)
            print(f"PASS   {pending.name} → {new_path.name}")

        else:
            # Rename to fail prefix
            new_path = directory / f"{fail_prefix}{base}"
            if new_path.exists():
                new_path.unlink()
            pending.rename(new_path)
            print(f"FAIL   {pending.name} → {new_path.name}")

            # Append review issues to prompt.txt
            prompt_path = _prompt_path(stem, directory)
            _append_review_issues(prompt_path, rnd, r["issues"], r["corrections"])
            print(f"       updated {prompt_path.name}")


def _append_review_issues(
    prompt_path: Path,
    rnd: int,
    issues: list[str],
    corrections: list[str],
) -> None:
    existing = prompt_path.read_text(encoding="utf-8") if prompt_path.exists() else ""
    section = f"\n\n## Review Issues — Round {rnd}\n\n"
    section += "\n".join(issues) + "\n"
    if corrections:
        section += "\n**Suggested corrections:**\n"
        section += "\n".join(corrections) + "\n"
    section += f"\n## Task — Round {rnd + 1}\n\n"
    section += (
        f"Fix the specific issues listed in 'Review Issues — Round {rnd}' above.\n"
        "Do NOT change any part of the diagram not mentioned in those issues.\n"
        "After fixing, verify with: python ascii_align.py --check <file>\n"
    )
    prompt_path.write_text(existing + section, encoding="utf-8", newline="\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    cmd = args[0]

    if cmd == "status":
        d = Path(args[1]) if len(args) > 1 else Path(".")
        cmd_status(d)

    elif cmd == "prep":
        d = Path(args[1]) if len(args) > 1 else Path(".")
        cmd_prep(d)

    elif cmd == "after-fix":
        rnd = int(args[1]) if len(args) > 1 else 1
        d = Path(args[2]) if len(args) > 2 else Path(".")
        cmd_after_fix(d, rnd)

    elif cmd == "gen-review":
        d = Path(args[1]) if len(args) > 1 else Path(".")
        cmd_gen_review(d)

    elif cmd == "after-review":
        if len(args) < 3:
            print("Usage: pipeline.py after-review <round> <results_file> [dir]")
            sys.exit(1)
        rnd = int(args[1])
        results_file = Path(args[2])
        d = Path(args[3]) if len(args) > 3 else Path(".")
        cmd_after_review(d, rnd, results_file)

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
