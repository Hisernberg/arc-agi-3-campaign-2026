# 04 · Duck Harness Deep-Dive (Our Current Stack)

Source of truth: `data/duck_bundle/src/ARC3-Inference/` (downloaded Kaggle dataset
`keithtyser/duck-qwen38-nvfp4-mtp-vllm-smoke-v1`, sha-verified via SOURCE_IDENTITY.json).

## Architecture

```
Kaggle notebook (our fork)
 └─ serving_setup.py          vLLM server: RadixArk/Qwen3.8-Flash-Next-NVFP4
 │                            MTP=3 (NEXTN spec-decode), 8 seqs, 8K batched tokens,
 │                            CUDA graphs cap 32, prefix caching OFF, watchdog (2 restarts)
 └─ TAAF framework            Benchmark/GameAPI, 28-way concurrency, 7920 s/game
     └─ ARC3-Inference/agent/tool_agent.py   THE AGENT (2,063 lines)
         ├─ CodeAct loop: model ↔ python-REPL tool (30 s/call, 4096-char cap)
         ├─ Runtime state: current_frame(.ascii/.step/.level/.shape/.segmentation),
         │   history, transitions, last_action_result, valid_actions
         ├─ World model: labeled blocks extracted from assistant text
         │   ("World model:", "Goal model:", "Action model:", "Recent findings:",
         │    "Open questions:", "Plan:", "Cross-level notes:")
         ├─ Context: 32k window (LOCAL_ANALYZER_CONTEXT_WINDOW), evict oldest user turn
         └─ Action mapping: UP/DOWN/LEFT/RIGHT/SPACE/MOUSE(row,col)/RESET
```

## Verified tuning surface (env vars → behavior)

| Env var | Default | Effect |
|---|---|---|
| `LOCAL_ANALYZER_CONTEXT_WINDOW` | 32768 | context budget for eviction |
| `LOCAL_ANALYZER_TOOL_STEPS` | 12 | max tool-calls per turn |
| `LOCAL_ANALYZER_TOOL_TIMEOUT` | 30 | s per python call (hard-capped 30) |
| `LOCAL_ANALYZER_TOOL_OUTPUT_TOKENS` | 1024 | tool output cap |
| `LOCAL_ANALYZER_MAX_OUTPUT` | 0 (=off) | completion token cap |
| `LOCAL_ANALYZER_TEMPERATURE` | 0.6 | sampling |
| `LOCAL_ANALYZER_TOP_P / TOP_K` | 0.95 / 20 | sampling |
| `LOCAL_ANALYZER_ENABLE_THINKING` | True | Qwen3 thinking mode |
| `LOCAL_ANALYZER_SEED` | -1 | sampling seed |
| `LOCAL_ANALYZER_MODEL_ID/BASE_URL/PROVIDER` | — | endpoint |
| serving `TAAF_VLLM_*` (notebook) | profile `kv5-bf16-mtp3-c8-cg32` | serving knobs |
| solver (`bm.solver.*` in notebook cell 13) | 7920 s/game, conc 28, analyzer 900–1200 s | budget |

## What our fork changes vs upstream Tufa Duck

1. Model swap: Qwen3.6-27B-FP8 → **Qwen3.8-Flash-Next-NVFP4** (8B-class, NVFP4, MTP native).
2. vLLM serving stack pinned + `sglang-rtxpro6000` sources + RadixArk NVFP4 PLE patch.
3. Watchdog on owned server (`/v1/models`, 4-failure restart, max 2 restarts).
4. Notebook 11 (experiment arm): ACTION7→UNDO patch + A/B MTP arm (not in production arm).
5. analyzer_timeout 900 → 1200 in tuned variant.

## Risks / open questions found in source review

- **Model size tradeoff:** 8B-Flash vs Tufa's 27B — faster serving (more turns/hour, more
  parallel games) but weaker per-turn reasoning. Our 3.45 vs their 18.81 is partly model
  capability. Levers: (a) more/better-shaped turns per game, (b) harness compensations
  (world-model backtesting, probe discipline), (c) consider a bigger served model if
  VRAM allows (RTX Pro 6000 = 96 GB → Qwen3.6-27B-FP8 fits; Qwen3.8-27B if it exists in
  the RadixArk line; verify availability as offline dataset).
- **Prefix caching disabled** (profile winner) — re-serving the growing system+history
  prompt every turn costs prefill time. The profile won on throughput, but re-test after
  any context-window change.
- **Action mapping has no ACTION7** in current source (matches Tufa's deliberate UNDO
  removal). Notebook 11's patch re-adds it — keep OUT unless ablated.
- **Eviction drops oldest user turn** — world-model notes are re-injected (labeled blocks),
  but *tool outputs* older than the retained window vanish. Schema-style backtesting would
  persist a compact transition table outside the evicted region.
- **`full_reset` flag** exists on frames — confirm RESET semantics per game locally.
