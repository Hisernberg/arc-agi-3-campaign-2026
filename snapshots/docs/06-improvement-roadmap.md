# 06 · Improvement Roadmap (Harness + RL + Tokenization)

Design principle (from research): **generic code execution + strong model + smart context**
beats hand-built tools; **executable world models with backtesting** is the single biggest
confirmed lever (+56 pts controlled, Schema). Ranked by expected score-per-GPU-hour.

---

## Track A — Harness & serving (safe, high certainty)

| # | Item | Expected | Effort | Risk |
|---|---|---|---|---|
| A1 | **Two-pass validation run discipline**: submit each candidate 2×; keep best | +0.3–0.8 (variance harvest) | 0 | none |
| A2 | **Probe-budget governor** (in-repo patch): cap wasteful repeated no-op actions; detect "HUD-only change" programmatically; force plan-then-act when 5 consecutive actions changed nothing | +0.5–1.5 | med | low |
| A3 | **Per-game budget triage**: allocate analyzer/game budget by marginal progress signal (levels/hour), not flat 7920 s; move time from dead games to progressing games | +0.5–2.0 | med | low |
| A4 | **Context engineering**: raise LOCAL_ANALYZER_CONTEXT_WINDOW 32k→48k if serving allows; compact transition table injected every turn (Schema-lite); keep world-model block | +0.5–2.0 | med | med |
| A5 | **Serving sweep** on Kaggle: MTP tokens {2,3,4}, seqs {8,12,16}, batched tokens {8k,12k}, prefix-caching on/off — pick winner on public-25 locally before burning submission | +0.2–0.5 | high (GPU) | low |
| A6 | **ACTION7/UNDO ablation**: keep OFF (Tufa evidence) unless local A/B says otherwise | 0 (guard) | low | low |

## Track B — Agent cognition (Schema/AVO-style, differentiating)

| # | Item | Expected | Effort | Risk |
|---|---|---|---|---|
| B1 | **Executable world-model loop**: after each level-1 exploration burst, prompt the agent to persist `hypothesis.py` (game `step()` model + `is_goal()`); backtest against recorded transitions; auto-flag mismatches; plan with BFS in the model when confidence ≥ threshold | +2–5 | high | med |
| B2 | **Discriminating probe selector**: when ≥2 hypotheses survive, choose real action maximizing outcome-divergence between hypotheses (information per real action) | +0.5–2 | med | low |
| B3 | **Level-transition re-grounding**: on level_completed, inject fresh-scene prompt (no carryover plan) + reset search state | +0.3–1.0 | low | low |
| B4 | **Cross-level mechanic transfer**: persist per-game notes file across levels ("mechanics learned in L1–L2 apply to L4"); Duck has "Cross-level notes:" tag — strengthen with structured memory keyed by object-hash signatures | +0.5–2 | med | med |
| B5 | **Dead-end detector + RESET policy**: when state is provably unrecoverable (backtest says no goal path from current state), RESET level early instead of burning budget | +0.3–1.0 | med | med |

## Track C — RL / learning (research, staged)

| # | Item | Expected | Effort | Risk |
|---|---|---|---|---|
| C1 | **Replay mining → prompt patching**: mine successful trajectories from local runs; distill recurring successful patterns into 3–5 generic prompt addenda (not per-game tools) | +0.5–1.5 | med | low |
| C2 | **GRPO-style finetune of Qwen3.8 on self-play traces** (LoRA offline; ship as adapter dataset attached to notebook): reward = level progression + efficiency vs human baseline; train on public-25 self-play | +1–4 | high | med |
| C3 | **Tokenization/action-channel efficiency**: Mouse/keyboard action encoding audit — ensure model emits compact action JSON; measure malformed-action rate from request logs; add grammar-constrained decoding (vLLM guided_json) for action calls | +0.2–0.8 | low–med | low |
| C4 | **Test-time training lite**: per-game adaptation via in-context example replay (append top-k own successful transitions to context when re-planning) | +0.3–1.0 | med | med |

## Track D — Perception (Duck keeps multimodality)

| # | Item | Expected | Effort | Risk |
|---|---|---|---|---|
| D1 | **Segmentation quality audit**: verify object-hash stability under animation (sb26/tn36 are animation-heavy); patch hash if identity flickers | +0.3–1.0 | med | low |
| D2 | **Multi-frame motion context**: 2–3 frame strip image instead of 1 (small models struggled with more; test 2) | +0.2–0.8 | low | low |

---

## Sequencing (this week)

- **Sat 9/20 (submission 1):** A1 + A3-lite (safe triage) on current best notebook → baseline
  variance harvest.
- **Sun 9/21 (submission 2):** A2 probe-budget governor + B3 re-grounding → ship if local
  public-25 CPU dry-run passes (LLM-free logic tests only).
- **Mon–Wed:** B1 world-model loop prototype tested LOCALLY against offline engine with
  mocked/proxy LLM where possible; then one GPU smoke run; ship Tue/Wed submission.
- **Thu–Fri:** A4 context engineering + B2 probes; second half-week GPU window for A5 sweep
  if quota allows.
- **C2 (LoRA finetune)** = next week's flagship once harness stabilizes; needs accumulated
  self-play replay data from this week's runs.

## Local-first verification protocol (no GPU burn)

1. Every harness patch → unit-test against offline engine (`scripts/local_play.py`).
2. LLM-dependent logic → record/replay mocked model responses (deterministic tests).
3. Serving changes → 1-game local GPU-less sanity via `--dry-run` paths, then a single
   short Kaggle interactive run before any submission.
