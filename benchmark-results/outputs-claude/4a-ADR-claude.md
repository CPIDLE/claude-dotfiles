# ADR-001: Migrate Task Delegation from opencode CLI to LangGraph + Gemini API

## Status

Accepted

## Context

Our current task delegation system uses Claude Code as the decision-maker and opencode CLI as the executor. Claude Code writes a structured spec (L1/L2/L3), pipes it to `opencode run --format json`, and reviews the output against a deliverables checklist.

This architecture has served us well for simple, linear tasks but has reached its limits:

1. **Linear flow only** — opencode executes spec → done. There is no way to branch, retry on failure, or route different task types to different models. A failing task simply fails; there is no conditional recovery.

2. **No state persistence** — Each `opencode run` invocation is stateless. Task history is tracked in a markdown file (`opencode_history.md`) outside the execution engine. There is no way to resume a partially completed task or share context between invocations.

3. **No conditional routing** — All tasks use the same model (`gemini-3-flash-preview`) regardless of complexity. An L1 "create a simple script" task burns the same resources as an L3 architectural task. There is no mechanism to route easy tasks to a cheaper/faster model.

4. **Tight coupling to opencode CLI** — The execution layer depends on opencode's process model, its JSON output format, and its permission system. Moving to a different LLM provider or deployment target (e.g., local Ollama on DGX Spark) requires rewriting the integration.

Benchmark validation confirmed that direct Gemini API calls produce equal or better output than opencode CLI (5.0 vs 4.11 composite score across 8 tasks), establishing that the orchestration layer can be replaced without quality loss.

## Decision

Replace the opencode CLI execution layer with a LangGraph-based directed graph that calls the Gemini API directly.

The graph topology is:

```
classify → execute → validate → report
              ↑          |
              └── retry ──┘ (max 1)
```

**Key components:**

- **Classify node** — Parses the spec, determines L1/L2/L3 level, and routes to fast (`gemini-3-flash-preview`) or full (`gemini-2.5-pro`) model based on complexity.
- **Execute node** — Sends the spec to the selected LLM with tool bindings (file read/write, bash, git). Receives structured output.
- **Validate node** — Rule-based (no LLM). Checks red-line violations (CLAUDE.md/AGENTS.md untouched), L1 file creation constraints, L2 allowed-file constraints. Returns pass/fail/retry.
- **Report node** — Formats results, appends to history, returns structured output to Claude Code.

**State persistence:** SQLite via LangGraph's built-in checkpointer. Tasks survive session restarts. History queryable without parsing markdown.

**Model switching:** Single environment variable (`LLM_PROVIDER=gemini|ollama`) changes the LLM endpoint. The graph, tools, and validation logic remain identical. This enables trial on Gemini API and production deployment on DGX Spark with Ollama without code changes.

## Consequences

### Positive

- **Retry logic** — Failed executions automatically retry once with the validation feedback injected into the prompt, recovering from transient LLM errors.
- **Model routing** — Simple tasks use cheaper/faster models; complex tasks get the full model. Estimated 40-60% cost reduction on mixed workloads.
- **State persistence** — Task state survives across sessions. Partially completed work can be resumed. History is structured data, not markdown.
- **Provider portability** — Switching from Gemini API to local Ollama requires changing one environment variable. No graph or tool code changes.
- **Testability** — Each node is independently unit-testable. The validate node is pure rule-based logic with no LLM dependency.

### Negative

- **Added complexity** — LangGraph introduces a dependency and a new abstraction layer. The team must learn its state management and graph construction patterns.
- **Migration effort** — Estimated 5-6 sessions to build + 2-week parallel validation period before decommissioning opencode.
- **Version coupling** — LangGraph is actively developed; breaking changes in future versions could require migration work. Mitigated by pinning versions in `pyproject.toml`.
- **Debugging difficulty** — Graph-based execution is harder to debug than a linear pipe. Mitigated by LangGraph's built-in tracing and the validate node's explicit pass/fail output.

## Alternatives Considered

### 1. Keep opencode CLI, add retry wrapper

Add a shell-level retry loop around `opencode run`. This addresses the retry problem but not state persistence, model routing, or provider portability. Rejected because it only solves one of four problems and adds fragile shell scripting.

### 2. Direct Gemini API without LangGraph

Call the Gemini API directly from Claude Code commands (no graph framework). This was validated in the benchmark and works for simple cases. Rejected for complex tasks because it requires reimplementing state management, retry logic, and conditional routing in ad-hoc Python — exactly what LangGraph provides as a framework.

### 3. Switch to a different agent framework (CrewAI, AutoGen)

These frameworks target multi-agent collaboration, which is heavier than our single-agent delegation pattern. LangGraph's graph-based approach maps directly to our classify→execute→validate→report pipeline without the overhead of agent role definitions and communication protocols.
