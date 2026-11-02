# ARC-AGI-3 Kaggle Competition Campaign

**Team:** Kragglenote2 Forwork · **Kaggle:** kragglenote2forwork / dasshovon (same team) · **GitHub:** Hisernberg
**Competition:** [ARC Prize 2026 - ARC-AGI-3](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3)
**Status (2026-10-26):** B best **33.50** (`arc26-b-dprime-clean-v1`, rank ~106/4799) · gold cutoff ~38.2-40 (rank 20, drifting) · top-50 line ~34 · **weapon: apex-v13 RUNNING** (Qwen3.8-27B-FP8 + D3) · **KEYWORD: GOLDRUSH** (docs/49)
**Master writeup:** [arc-agi-3-campaign-writeup](https://github.com/Hisernberg/arc-agi-3-campaign-writeup) (private)

---

## Mission

Build systems that learn and adapt to novel, human-solvable tasks and maximize the ARC-AGI-3
leaderboard through disciplined, evidence-first iteration: ratchet-only scoring (LB takes max),
fail-open additive deltas, receipts-as-truth, verdict councils, and honest odds on every plan.

## Current weapon stack (apex-v13, Oct-27 fire)

| Layer | Detail | Receipt |
|---|---|---|
| Model | **Qwen3.8-27B-FP8** primary (saltb0x mirror) → 3.5-FP8 fallback → Flash-Next-W4A16 incumbent | `#OURS_V38 served=` |
| D2 (v12) | stall-knee priority fold (knee 80/halflife 40/floor 0.1) + act_checked world-model batching + guard-v2 (120-min gateway patience, DNS-escape 3600s, smoke fast-path) | `#OURS_V12` `#OURS_ACTCHECKED` |
| D3 (v13) | transition-graph action priors (8 games cheatsheet-dead → x0.65) + human-par pace table (25/25 parsed) + endgame exploit switch + XPACK tools heal | `#OURS_V13 hits=` |
| Data | dossier v3: 25 games, 6 mechanic families, tgraph priors + pace + endgame triggers + SFT (Qwen template) — **live on both accounts** | `#OURS_DOSSIER ok games=25` |
| Core | D' priority form (level_pow x pace x eff_decay x headroom), wastepack dedup, python-tool transforms (13 fns) | `#OURS_FORM ok version=d_prime` |

Proof standard: 13/13 dataset gates + 19/19 kernel gates + 13/13 CPU tests before any GPU fire.
Idea pool: **1,515** (docs/44). Plans: docs/48-51. Keyword protocol: DAILY_PROTOCOL.md.

---

## Mission

Build systems that learn and adapt to novel, human-solvable tasks and maximize the ARC-AGI-3
leaderboard score through disciplined, GPU-efficient iteration: local-first development,
daily submissions, evidence-driven harness improvements.

## Current stack

| Component | Detail |
|---|---|
| Harness | Tufa Labs **Duck** (CodeAct-style python-REPL agent), fork with Qwen3.8 serving |
| Model | `RadixArk/Qwen3.8-Flash-Next-NVFP4` via pinned vLLM (MTP=3, 8 seqs, 8K batch, CUDA graphs) |
| Concurrency | 28 games in parallel, 7920 s/game budget, analyzer timeout 900–1200 s |
| Serving profile | `kv5-bf16-mtp3-c8-cg32` (winner of A/B profile sweep, notebook 12) |

Key files (Duck solver source available in `data/duck_bundle/`):
`src/ARC3-Inference/inference/agent/{tool_agent,prompts,python_tool_sandbox,action_names,runtime_state,vision_context}.py`

## What we know (topline)

- **Scoring (RHAE):** per-level `(human_actions / agent_actions)²` capped at 1.15; per-game
  weighted average by level index; completion-capped; total = mean over 110 hidden games.
- **Local CPU development works:** all 25 public games run offline via `arc_agi` + `arcengine`
  wheels — agent iteration does not need GPU.
- **UNDO (ACTION7) is a trap** — Tufa deliberately withheld it; our notebook 11 patched it in
  (experiment), do not ship unless ablation shows gains.
- **Winner pattern 2026:** executable world models + backtesting + BFS in the simulator
  (Schema 99% RHAE public; NVIDIA AVO 100% text-only). Hand-built per-game tools *lose* to
  generic code execution + strong model.
- **Variance is real:** identical reruns swing ±0.4; submit the same notebook 2× and keep the best.

## Repo layout

```
docs/        Campaign documentation (read 01 → 08 in order)
notebooks/   Kaggle submission notebooks + variants
scripts/     Automation (Kaggle API, daily loop) + local dev tooling
analysis/    Game analysis outputs, traces, scorecards
data/        (gitignored) datasets, duck bundle, wheels
```

## Docs index

1. [Competition overview](docs/01-competition-overview.md)
2. [Scoring methodology & implications](docs/02-scoring-methodology.md)
3. [State-of-the-art research](docs/03-sota-research.md)
4. [Duck harness deep-dive (our stack)](docs/04-duck-harness-analysis.md)
5. [Public games analysis](docs/05-games-analysis.md)
6. [Improvement roadmap (harness + RL + tokenization)](docs/06-improvement-roadmap.md)
7. [Week plan (Sept 19–26)](docs/07-week-plan.md)
8. [Daily automation protocol](docs/08-automation-protocol.md)
9. [Campaign summary (setup day)](docs/09-campaign-summary.md)

**Milestone-2 era (Oct 2026):**

25. [Final week plan — two accounts, 32h](docs/25-final-week-plan-two-accounts-32h.md) · 26. [Workflow OS](docs/26-workflow-os.md) · 27. [AgentFix 6.0 teardown](docs/27-agentfix-6point0-teardown.md) · 28. [M2 wave deep analysis](docs/28-m2-wave-deep-analysis.md) · 29. [SUPERBRAIN v10 plan](docs/29-superbrain-v10-plan.md) · **30. [Milestone-2 complete deconstruction — 4→27 thought process, per-notebook serving configs, LB factors, gap analysis, 30–40+ fusion plan](docs/30-milestone2-deconstruction.md)**

## Start here (from 2026-10-08)

**[docs/31 — Research Day: full-stack reassessment and the climb plan](docs/31-research-day-2026-10-08.md)** · **[docs/32 — Keyword workflow + routines](docs/32-keyword-workflow.md)** · runbooks in [`agents/keywords/`](agents/keywords/README.md) · scripts in `scripts/kw/` · tomorrow's instruction in `analysis/next_submission.json` · families in `analysis/config_families.json` · per-game base in `analysis/public25_reference_m2s.md` · notebook teardowns in `analysis/teardowns/`.

Keywords: `status` · `submit` · `plan` · `agent inside` · `agent outside` · `analysis` · `research` · `search`.

## Weekly outside-view board

Three independent reviewer agents audit the campaign every Monday and generate falsifiable ideas:

- **A — Systems Sceptic** (serving/throughput/cache limits) · `agents/outsider/AGENT-A-systems-sceptic.md`
- **B — Adversarial Strategist** (meta, slot economics, variance) · `agents/outsider/AGENT-B-adversarial-strategist.md`
- **C — Cognition Detective** (wrong-goal defense, UNDO discipline) · `agents/outsider/AGENT-C-cognition-detective.md`

Cadence + memo template: `agents/outsider/RUNBOOK.md` · memos: `agents/outsider/weekly/YYYY-WW-{A,B,C}.md` (Week-1 = 2026-W40 seeded).

## Operating cadence (see docs/32 for the current version)

- **Daily (from Sat Sept 20):** 1 new/submission pair; resubmit best when GPU is exhausted.
- **Each submission:** same notebook 2× (variance averaging), keep best public score.
- **Weekly:** milestone review in `docs/07-week-plan.md`, results logged in `analysis/results.md`.
- **Weekly (from Oct 5):** outside-view agent memos (see board above) → REGISTER entries with falsification criteria; M2-era target: every submission from the 27+ family, fusion notebook to 30–40+ (docs/30 §5).
