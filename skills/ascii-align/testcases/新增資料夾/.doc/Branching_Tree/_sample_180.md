## Sample 180

**Source**: `opencode-bench\ARCHITECTURE.md` L9

```
┌──────────────────────────────────────────────────────────────┐
│                     使用者（Laptop）                          │
│                   RTX 5060 · 8GB VRAM                        │
│                                                              │
│   ┌─────────────────────┐    ┌─────────────────────────┐     │
│   │    Claude Code CLI  │    │     opencode CLI         │     │
│   │   (Anthropic API)   │    │    (@ai-sdk providers)   │     │
│   │                     │    │                          │     │
│   │  /do easy → Gemini  │    │  Providers:              │     │
│   │  /do deep → Gemini  │    │  ├ google/gemini-3-flash │     │
│   │                     │    │  ├ 4090-litellm/*        │     │
│   │  主力開發 +         │    │  └ dgx/*                 │     │
│   │  bench baseline     │    │                          │     │
│   └────────┬────────────┘    └──┬──────────┬────────────┘     │
│            │                    │          │                   │
└────────────┼────────────────────┼──────────┼──────────────────┘
             │                    │          │
             │ Anthropic API      │          │
             ▼                    │          │
  ┌────────────────┐              │          │
  │  Claude Cloud  │              │          │
  │  opus-4.6      │              │          │
  │  sonnet-4-6    │              │          │
  └────────────────┘              │          │
                                  │          │
          ┌───── Gemini API ──────┘          │
          ▼                                  │
  ┌────────────────┐                         │
  │  Google Cloud  │                         │
  │  gemini-3-flash│                         │
  │  gemini-3.1-pro│                         │
  └────────────────┘                         │
                                             │
          ┌──────────────────────────────────┘
          │
          ▼
  ┌─────────────────────────┐     ┌──────────────────────────┐
  │   RTX 4090 Server       │     │     DGX Spark            │
  │   10.63.138.16          │     │     10.63.138.198        │
  │   24GB VRAM             │     │     Grace CPU 128GB      │
  │                         │     │                          │
  │   Ollama :11434         │     │   Ollama :11434          │
  │     │                   │     │     │                    │
  │   LiteLLM :4000/v1     │     │   Traefik →              │
  │     │                   │     │   LiteLLM /litellm/v1    │
  │   fix-proxy :4001/v1   │     │                          │
  │     (index bug fix)     │     │   Models:                │
  │                         │     │   ├ qwen3-coder-next     │
  │   Models:               │     │   │  (80B MoE, 52GB)    │
  │   ├ qwen3-coder:30b    │     │   ├ qwen3-coder:30b      │
  │   ├ mistral-nemo        │     │   ├ gemma4:31b           │
  │   └ gemma4:e4b          │     │   └ mistral-nemo         │
  └─────────────────────────┘     └──────────────────────────┘
```

---
