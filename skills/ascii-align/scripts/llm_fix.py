#!/usr/bin/env python3
"""llm_fix.py — Reference documentation for the ascii-align pipeline.

This script is NOT used directly by the skill. The actual LLM fix step is
performed by Claude subagent as described in SKILL.md.

Pipeline architecture (linter + LLM agent):
  1. ascii_align.py --prompt (linter: hrule fix + rich diagnostic prompt)
  2. Claude subagent reads diagnostic prompt → fixes all structural issues
  3. ascii_align.py --check (verify: report any remaining issues)

The rule engine acts as a linter — it detects and reports issues, but only
performs safe hrule fills. All structural fixes (content padding, inner box
alignment, off-by-1 resolution) are delegated to the LLM subagent.

Benchmark results (a01, 8 files):
  - Linter only:              0/8 exact match
  - Linter + Claude subagent: 8/8 exact match
  - Linter + Gemini:          0/8 (Gemini lacks display-width understanding)
"""
