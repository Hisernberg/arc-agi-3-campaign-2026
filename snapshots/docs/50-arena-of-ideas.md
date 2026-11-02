# docs/50 — Arena of Ideas: public-kernel intel sweep + council verdicts (Oct-26)

"Go through everything public, debate, build an arena, test, finalize." — directive record.

## 1. Intel sweep (what the public meta actually is)

Pulled + mined 6 top public kernels (kaggle kernels/list by votes, `kernels/pull` sources to /tmp/pub_intel):

| Kernel | Votes | Score-era | Core technique | Steal / reject |
|---|---|---|---|---|
| `dfranzen/arc-agi-3-milestone-2-solution` | 1128 | M2 baseline | sandbox bootstrap verdict loop, rendered boards, history trim | we already exceed it (guard/priors/dossier); verdict-loop ≈ our act_checked |
| `nihilisticneuralnet/0-46-...-persistent-memory-bfs` | 153 | [0.46] | BFS + persistent memory + PER + expert demos + `_unproductive` pruning + "fewer colors = closer" heuristic | steal: pruning concept (E-006), color heuristic (E-007); reject: full rewrite (E-284) |
| `mbmmurad/arc-agi-3-lb-0-86-...` | 105 | LB 0.86 (3rd at milestone) | **Gemma-4-31B vision policy**, rendered STEP frames, JSON repair, reflection memory | steal: JSON repair (E-004), reflection memory (E-005), STEP-frame idea for v15 vision; reject: Gemma (Qwen-only directive, E-285) |
| `foysalemonshanto/lb-9-arc3-duck-v12-with-qwen-3-8-27b` | 296 | LB-9 | **Qwen3.8-27B on duck harness**, game_weights buckets | confirms our v13 model swap is the meta (E-002 bucket idea) |
| `keithtyser/duck-qwen3-8-flash-next-nvfp4-mtp` | 211 | — | **Flash-Next NVFP4 MTP spec-decode** | v15 serving upgrade path (E-055, E-360) |
| `heliosli/try-merging-it-...-win-gold` | 122 | — | byte-clone of dfranzen M2 + merge | validates merge-plagiarism meta; we don't need it (E-010) |

**Meta conclusion**: the public top is (a) duck/taaf harness + Qwen3.8 family, (b) M2-lineage
forks, (c) one algorithmic BFS branch. Our differentiators (receipts law, guard-v2, tgraph
priors, dossier layers, fail-open build system) are in **no** public kernel — writeup moat.

## 2. Model debate (constraint: Qwen 3.8 + 3.8 Flash only — user directive)

- PRO 3.8-27B-FP8: built on qwen3_5 arch (HF tag) → our SGLang FP8 stack accepts it
  unmodified; public meta uses it; "substantial gains in long-horizon agentic tasks".
- PRO Flash-Next: already attached since v11 as incumbent tier + drafter (albucino drafter
  + intel W4A16); NVFP4-MTP public proof for v15 spec-decode.
- CON any non-Qwen (Gemma-4-31B has LB-0.86 evidence) → **rejected** per directive (E-285).
- VERDICT: 3.8-27B-FP8 primary + 3.5 fallback + Flash-Next tiers. Wired in v13. (docs/51)

## 3. Architecture debate (D3)

ACCEPTED (all fail-open, bounded ×0.65-1.35, additive tails only):
1. Qwen3.8-27B-FP8 swap (path-priority + fingerprint prefer + served-name receipt).
2. #48 tgraph priors: 8 games have cheatsheet-measured dead actions → 0.0 prior (×0.65);
   family defaults otherwise; RESET floor 0.05.
3. #66 pace: 25/25 human pars parsed; behind-pace ×0.88.
4. #67 endgame: per-family thresholds; known-good ×1.20, unknown ×0.93.
5. XPACK tools heal: dual-name module ship + exec self-heal (kills v12's tools=False).

REJECTED / DEFERRED (with reasons):
- Full BFS/PER rewrite → v15 research branch (risk to ratchet; budget model unproven).
- Parquet-early-write semantics change → needs competition-rule verification.
- Gemma vision policy → directive. Spec-decode now → v15 after watchdog lands.

## 4. Dataset debate

- v2 classifier was degenerate (17/25 → one bucket). v3 replaces with **mechanic-true
  taxonomy**: CLICK-PRECISION 3 / HIDDEN-SEQUENCE 5 / DEAD-ANIM-HYBRID 2 / DEAD-ACTIONS 4 /
  ANIMATED-TIMING 8 / BUDGET-PACED 3 — derived from cheatsheet signals, validated 6 families.
- v2 files verbatim preserved; v3 = additive layers (tgraph/pace/endgame/SFT-v3/transforms
  dual-name + manifest). 13/13 gates. Live on both accounts.

## 5. Idea arena

Batch E = **500 new ideas** (E-001..E-500, schema-complete, deduped, validated JSONL)
→ pool **1,515**. Sources: public-kernel mining, grandmaster practice norms, expert domains
(serving/RL/eval/infra), qwen3.8 intel, campaign law codification. Promotion path fixed:
pool → CPU test → gates → GPU → verdict (E-290).

## 6. Proof standard today (arena "test" requirement)

13/13 dataset gates · 19/19 kernel gates · 13/13 CPU factor-math tests (T6: dead→65,
T7: stacked→117, T8:→113, T9:→79, T11: fail-open) · push verified (v1 RUNNING, kernelId
140991512) · v12 byte-identity maintained (G16/G18).

## 7. Teardown arena (docs/52, Oct-26)

| Idea | Verdict | Basis |
|---|---|---|
| Solved-level memory (M85 design) | **ACCEPT → v14 core** | +2.8 LB, cache-safe 94.3% hit, fail-open |
| D′ scheduler | **ALREADY IN v13** | shipped as #OURS_FORM d_prime |
| noop-repeat guard | **AUDIT at G2** | upstream +16 levels; ours has own guard |
| HTTP retry 3600 / startup 55min | **ACCEPT if weaker** | vickyfym env delta |
| Redraw farm max-of-N | **ACCEPT → farm v1** | romantamrazov 86 versions doctrine |
| Concurrency 10→24 admission | **REJECT** | private-set 15.67 vs 19.53 |
| Official-formula priority | **REJECT** | private-set 13.37 vs 18.07 |
| Throughput pushing | **REJECT** | tokens invariant ±12% |
| Public-neutral efficiency tweaks | **QUARANTINE** | hidden-set cost 7–8 pts (vickyfym) |
