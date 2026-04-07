#!/usr/bin/env python3
"""do_helper.py -- Multi-round LLM engine caller for /do command.

Usage:
    python do_helper.py easy --engine gemini [--model MODEL] < spec
    python do_helper.py deep --engine gemini [--model MODEL] < spec
    python do_helper.py check --engine gemini

Output (JSON-lines):
    easy:  {"status":"ok","result":"..."}
    deep:  {"round":1,"status":"done","result":"..."}
           {"round":2,"status":"done","result":"..."}
           {"final":"...","rounds":N,"verdict":"pass|fail|fixed","issues":[]}
    check: {"ok":true} or {"ok":false,"error":"..."}
"""

import argparse
import json
import os
import re
import sys


# ---------------------------------------------------------------------------
# System prompts
# ---------------------------------------------------------------------------

EASY_SYSTEM_PROMPT = (
    "你是資深軟體工程師。直接執行以下任務，只輸出交付物（程式碼或文件）。"
    "不要包裝在 markdown code fence 中（除非交付物本身就是 markdown）。"
)

DEEP_R1_PROMPT = (
    "你是資深軟體工程師。按照以下 spec 完成任務。\n\n"
    "要求：\n"
    "- 完整實作所有功能\n"
    "- 包含錯誤處理和邊界條件\n"
    "- 程式碼須包含 type hints 和 docstrings\n"
    "- 確保可直接執行，無需修改\n\n"
    "只輸出交付物，不要解釋。不要包裝在 markdown code fence 中。"
)

DEEP_R2_PROMPT = (
    "你是嚴格的 code reviewer。審核以下程式碼/文件是否符合 spec。\n\n"
    "另外列出 spec 沒提到但你注意到的潛在問題（advisory_notes），例如：\n"
    "- 時鐘選擇是否合適（wall-clock vs monotonic）\n"
    "- import 是否重複\n"
    "- docstring 是否與實作不一致\n"
    "- 是否殘留 dead code\n"
    "advisory_notes 不影響 verdict — 即使有 advisory，只要符合 spec 仍應 pass。\n\n"
    '回應格式（JSON）：\n'
    '{\n'
    '  "verdict": "pass" | "fail",\n'
    '  "issues": [\n'
    '    {"severity": "high|medium|low", "line": N, "description": "..."}\n'
    '  ],\n'
    '  "fix_instructions": "如果 fail，描述如何修正（供下一輪 LLM 使用）",\n'
    '  "advisory_notes": ["spec 外觀察 1", "spec 外觀察 2"]\n'
    '}\n\n'
    "只輸出 JSON，不要其他文字。"
)

DEEP_R3_PROMPT = (
    "你是資深軟體工程師。以下程式碼有問題，請根據審核意見修正。\n\n"
    "輸出完整的修正後程式碼/文件，不要只輸出 diff。不要解釋。"
    "不要包裝在 markdown code fence 中。"
)


# ---------------------------------------------------------------------------
# Engine abstraction
# ---------------------------------------------------------------------------

class GeminiEngine:
    def __init__(self):
        from google import genai
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        self.client = genai.Client(api_key=api_key)

    def call(self, model, prompt):
        r = self.client.models.generate_content(model=model, contents=prompt)
        return r.text


class OllamaEngine:
    def __init__(self):
        import urllib.request
        from urllib.parse import urlparse
        self._urllib = urllib.request
        self.url = os.environ.get("OLLAMA_URL", "http://localhost:11434")
        parsed = urlparse(self.url)
        hostname = parsed.hostname or ""
        if hostname not in ("localhost", "127.0.0.1", "::1") and not hostname.startswith("192.168.") and not hostname.startswith("10."):
            raise ValueError(f"OLLAMA_URL must point to a local/private address, got: {hostname}")

    def call(self, model, prompt):
        data = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode()
        req = self._urllib.Request(
            f"{self.url}/api/generate", data=data,
            headers={"Content-Type": "application/json"},
        )
        resp = json.loads(self._urllib.urlopen(req, timeout=110).read())
        return resp["response"]


class OpencodeEngine:
    def __init__(self):
        import subprocess
        self._subprocess = subprocess

    def call(self, model, prompt):
        result = self._subprocess.run(
            ["opencode", "run", "--format", "json"],
            input=prompt, capture_output=True, text=True, timeout=110,
        )
        if result.returncode != 0:
            raise RuntimeError(f"opencode exited with code {result.returncode}: {result.stderr[:500]}")
        # Parse JSONL, extract text parts
        parts = []
        for line in result.stdout.splitlines():
            try:
                obj = json.loads(line)
                if obj.get("type") == "text" and "part" in obj:
                    parts.append(obj["part"]["text"])
            except json.JSONDecodeError:
                continue
        return "".join(parts)


ENGINES = {"gemini": GeminiEngine, "ollama": OllamaEngine, "opencode": OpencodeEngine}

# Preview model names are transient — update when Google renames/removes them.
# Override via DO_MODEL_EASY / DO_MODEL_DEEP env vars.
DEFAULT_MODELS = {
    "gemini":   {"easy": "gemini-3.1-flash-lite-preview", "deep": "gemini-3-flash-preview"},
    "ollama":   {"easy": "qwen3:8b",                      "deep": "qwen3:8b"},
    "opencode": {"easy": "gemini-3-flash-preview",         "deep": "gemini-3-flash-preview"},
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def emit(obj):
    """Print a JSON object as one line, flush immediately."""
    print(json.dumps(obj, ensure_ascii=False), flush=True)


def resolve_model(engine_name, mode, explicit_model):
    """Resolve model: explicit arg > env var > default."""
    if explicit_model:
        return explicit_model
    env_key = "DO_MODEL_EASY" if mode == "easy" else "DO_MODEL_DEEP"
    env_val = os.environ.get(env_key)
    if env_val:
        return env_val
    return DEFAULT_MODELS.get(engine_name, {}).get(mode, "")


def parse_review(text):
    """Extract JSON verdict from review response. Tolerant of markdown fences."""
    text = text.strip()
    # Strip markdown code fences if present
    m = re.search(r"```(?:json)?\s*\n?(.*?)```", text, re.DOTALL)
    if m:
        text = m.group(1).strip()
    try:
        parsed = json.loads(text)
        parsed.setdefault("advisory_notes", [])
        return parsed
    except json.JSONDecodeError:
        return {
            "verdict": "fail",
            "issues": [{"severity": "high", "line": 0, "description": "Review JSON parse failed — triggering Round 3 as safety fallback"}],
            "fix_instructions": "Review response was malformed. Re-check the code against the spec.",
            "advisory_notes": [],
        }


def strip_full_fence(text):
    """Strip fence only if entire response is exactly one fenced block. CRLF-safe."""
    m = re.match(r"^\s*```[\w+-]*\r?\n(.*)\r?\n```\s*$", text, re.DOTALL)
    return m.group(1) if m else text


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_check(engine_name):
    """Verify engine availability."""
    try:
        ENGINES[engine_name]()
        emit({"ok": True})
    except Exception as e:
        emit({"ok": False, "error": str(e)})
        sys.exit(1)


def cmd_easy(engine, model, spec):
    """Single-shot generation."""
    prompt = EASY_SYSTEM_PROMPT + "\n\n" + spec
    result = strip_full_fence(engine.call(model, prompt))
    emit({"status": "ok", "result": result})


def cmd_deep(engine, model, spec):
    """Multi-round: generate -> review -> fix (max 3 rounds)."""
    # Round 1: Generate
    r1_prompt = DEEP_R1_PROMPT + "\n\n" + spec
    r1 = strip_full_fence(engine.call(model, r1_prompt))
    emit({"round": 1, "status": "done", "result": r1})

    # Round 2: Review
    r2_prompt = DEEP_R2_PROMPT + "\n\n## Spec:\n" + spec + "\n\n## Code:\n" + r1
    r2 = engine.call(model, r2_prompt)
    emit({"round": 2, "status": "done", "result": r2})

    review = parse_review(r2)
    verdict = review.get("verdict", "pass")
    issues = review.get("issues", [])
    advisory_notes = review.get("advisory_notes", [])

    if verdict == "pass":
        emit({
            "final": r1, "rounds": 2, "verdict": "pass",
            "issues": issues, "advisory_notes": advisory_notes,
        })
        return

    # Round 3: Fix
    fix_instructions = review.get("fix_instructions", "")
    r3_prompt = (
        DEEP_R3_PROMPT + "\n\n## Spec:\n" + spec
        + "\n\n## Original Code:\n" + r1
        + "\n\n## Review Issues:\n" + json.dumps(issues, ensure_ascii=False)
        + "\n\n## Fix Instructions:\n" + fix_instructions
    )
    r3 = strip_full_fence(engine.call(model, r3_prompt))
    emit({"round": 3, "status": "done", "result": r3})

    # advisory_notes always sourced from R2 review, even when R3 runs.
    emit({
        "final": r3, "rounds": 3, "verdict": "fixed",
        "issues": issues, "advisory_notes": advisory_notes,
    })


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="do_helper -- LLM engine caller")
    sub = parser.add_subparsers(dest="command", required=True)

    # check
    p_check = sub.add_parser("check")
    p_check.add_argument("--engine", default="gemini")

    # easy
    p_easy = sub.add_parser("easy")
    p_easy.add_argument("--engine", default="gemini")
    p_easy.add_argument("--model", default=None)

    # deep
    p_deep = sub.add_parser("deep")
    p_deep.add_argument("--engine", default="gemini")
    p_deep.add_argument("--model", default=None)

    args = parser.parse_args()

    if args.command == "check":
        cmd_check(args.engine)
        return

    # Initialize engine once
    engine_cls = ENGINES.get(args.engine)
    if not engine_cls:
        emit({"status": "error", "message": f"Unknown engine: {args.engine}"})
        sys.exit(1)

    try:
        engine = engine_cls()
    except Exception as e:
        emit({"status": "error", "message": f"Engine init failed: {e}"})
        sys.exit(1)

    model = resolve_model(args.engine, args.command, args.model)
    spec = sys.stdin.read()

    if not spec.strip():
        emit({"status": "error", "message": "Empty spec"})
        sys.exit(1)

    try:
        if args.command == "easy":
            cmd_easy(engine, model, spec)
        elif args.command == "deep":
            cmd_deep(engine, model, spec)
    except Exception as e:
        emit({"status": "error", "message": str(e)})
        sys.exit(1)


if __name__ == "__main__":
    main()
