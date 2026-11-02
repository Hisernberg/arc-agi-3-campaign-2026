# 14 — dasshovon Submission Plan: 27B Route Today, R11 Merge Tomorrow

*2026-09-27. Account: **dasshovon** (token KGAT_REDACTED…62), new submission account by user instruction
("from now submit her"). No submissions yet on the account; competition attached.*

## 1. Today's submission — LB-9 27B repro (running)

**Kernel:** `dasshovon/arc26-qwen3-8-27b-lb9-v1` (v1, private, RTX Pro 6000, internet off)
**Code:** byte-identical to `lb-9-arc3-duck-v12-with-qwen-3-8-27b` (our research cache copy) —
the Duck v12 + Qwen3.8-27B-FP8 notebook that scored **LB ~9** for the AIRIS deleted member.

Inputs (all verified public/attachable):
- datasets: `jakobbrggen/taaf-kaggle-source-anim-20260807-anim`, `driessmit1/arc3-vllm-h100-wheelhouse-v3` (516 MB)
- model: `foysalemonshanto/qwen3-8-27b-fp8-repacked-v1/pyTorch/hf-fp8/1` (20+ files, 16 layer shards, mtp+outside)
- competition: `arc-prize-2026-arc-agi-3`
- served name `Qwen/Qwen3.8-27B-FP8`; 25 games × 1 pass; concurrency 28; per-game cap 7920 s

Flow: kernel RUNNING → watcher `scripts/watch_dasshovon_lb9.sh` (PID logged in logs/) polls every
5 min → on COMPLETE downloads outputs, health-checks 4 signals (submission.parquet, score.json,
benchmark.json, vllm identity contains 27B) → ≥3/4 submits `kaggle competitions submit … -k slug -v 1`
→ polls score. Unhealthy outputs ⇒ NO submit, exit 3 (protects the daily submission).

**Why this is the highest-EV move:** model capability is the single biggest lever (NVIDIA 100% RHAE
on Opus-class; AIRIS's own 27B run drew ~9 vs their 8B 4.68). Zero code change ⇒ proven pipeline.

## 2. Risk register (today)

| Risk | Mitigation |
|---|---|
| vLLM/wheelhouse incompat with current kaggle image | unpinned docker like the original run; if setup fails, pin urad's `57e612b4…` sha and re-push |
| GPU quota exhaustion on dasshovon | fresh account ≈30 h/wk; run needs ≈3–4 h; run started fine |
| Competition join missing | submit step will fail loudly; user clicks Join once in web UI |
| 27B slower per token (13.3:1 ratio on 8B) | per-game cap 7920 s; original 27B run completed within Kaggle caps |
| Score draw variance (2.78→4.68 on identical 8B code) | LB keeps best draw; re-submit same kernel on later days if no better version |

## 3. R11 — the merged "most advanced" kernel (tomorrow's candidate)

Base: **LB-9 27B serving stack** (proven ~9) + **urad R9/R10 fix set** (proven +Δ on 8B) + our
validated v4/v5 add-ons. Port order by value-per-risk:

1. **P4 history compression** (−35% prompt tokens; pure harness, no model change) — port to the
   anim-bundle tool_agent; our replay suite validates on real traces.
2. **P6 persistent defs store** (−32% repeated code lines; sandbox prelude) — port with our
   sandbox tests (by-value import trap mirrors our TA-namespace lesson).
3. **P20 HUD/no-impact detector** (+1.6 internal on thui's public run) — solver.py EOF append;
   wrap session `_execute_action`; our 25-game offline engine validates.
4. **P21 weighted gate** (KV fits 4–6 requests; level-weighted fairness) — critical for 27B
   (bigger KV pressure): slots tuned for 27B KV budget.
5. **P9 board diff + P22 level-up reset + P2 UNDO name + P7 sandbox imports** — small, surgical.
6. **P15/R10 rescue + P19 supervisor** — keep, env-tunable, P19 budget re-tuned for 27B latency.
7. **Our differentiators on top:** runtime-effects ledger (v4), human-budget prior
   [30,54,51,54,96,80,86,92,163] as a per-level pacing note, dead-action flags, numeric
   action-id normalization, wm discipline prompt — all env-var switchable, fail-open, idempotent
   (reuse test harness: 41-check preflight + 8k real-action replay).

2026-innovation additions (each net-token-negative or neutral, switchable):
- **Tokenizer-level:** Qwen thinking-block note mining (P1 generalization) + tokenizer-aware
  truncation of reasoning blocks (never split inside a `</think>` token span; strip reasoning
  before history, keep last block) — P4 on steroids.
- **ASCII engine:** harness-side grid diff/region tracker (P9) extended to *object* level:
  connected components per colour, motion vectors between consecutive frames, `expect:` vs diff
  verdict line ("matched/mismatched") — VISTA-style world-model check without extra calls.
- **Segmented pipeline:** per-level segmentation of history (completed-level records P14/P16)
  + append-only searchable JSONL log (NOOA v7 plan) as the memory substrate.
- **LLM + non-LLM hybrid:** deterministic probe generator on stalls (non-LLM) feeding the
  rescue path; LLM only for hypothesis selection — saves calls at 27B latency.
- **Token+action+frame budget optimizer:** per-level token ledger; when a game exceeds its
  budget share, shrink history (P4 harder) before shrinking actions.

Validation gate before ANY submission: 30+ checks green (patch apply exact-once, imports,
25-game offline smoke, replay of real 27B-run actions through patched wrapper, budget flags,
fail-open, idempotency) — same bar as v4's 41/41.

## 4. Day-by-day scoring plan

| Day | Action | Expected |
|---|---|---|
| 9/27 | 27B LB-9 repro submit (running) | draw ≈ 6–9 (LB keeps best) |
| 9/28 | R11 build + preflight; if 27B drew <8, re-submit same kernel (fresh draw) | validate fixes; variance ratchet |
| 9/29 | R11 submit (27B + P4/P6/P9/P20/P21/P22 + our add-ons) | ≈ 9–12 |
| 9/30+ | variance re-submits; Milestone-2 go/no-go (deadline 9/30, needs open-source — user decision) | best-of ratchet |
| Oct | tokenizer/ASCII-engine/segmented upgrades as R12+; target silver ≥ top 6% | climb toward 15+ |

Rule reminders: never submit an unhealthy run; 1 submission/day cadence; every new piece
env-var switchable so a bad draw can be A/B'd against the frozen control on the same day.
