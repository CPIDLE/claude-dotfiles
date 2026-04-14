#!/usr/bin/env python3
"""llm_fix.py — Reference implementation for the ascii-align LLM fix pipeline.

This script is NOT used directly by the skill. The actual LLM fix step is
performed by Claude subagent as described in SKILL.md.

This file documents the proven pipeline architecture:
  1. ascii_align.py (rule-based pass)
  2. Claude subagent with precise prompt (structural fixes)
  3. ascii_align.py (re-align after LLM)

Benchmark results (a01, 8 files):
  - Rule-based only:              0/8 exact match
  - Rule-based + Claude subagent: 8/8 exact match
  - Rule-based + Gemini:          0/8 exact match (Gemini lacks display-width understanding)
"""
