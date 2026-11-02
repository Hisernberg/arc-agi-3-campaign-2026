# Kaggle Sweep 2026-09-24 — All Public Notebooks vs Our Score

Sweep method: full leaderboard CSV (3,296 teams) + kernel inventory (1,104 unique
notebooks via votes/dateCreated/dateRun) + team-member-username cross-reference +
30 top notebooks downloaded and deep-analyzed (sources in `analysis/sweep/sources/`,
converted text in `analysis/sweep/text/`, raw JSON in `data/sweep/`).

## 1. Our position

- **Team**: Kragglenote2 Forwork — **3.85, rank 214 / 3,296** (16 submissions)
- Previous reference point 3.45 → now 3.85 (v4 worldmodel-v1)
- **213 teams above us**; the score cliff is steep: top 10 = 8.65–19.40

## 2. Top of the leaderboard (2026-09-24)

| Rank | Team | Score | Note |
|---|---|---|---|
| 1 | Lord Han Solo | 19.40 | passed Tufa on Sep 23 |
| 2 | Tufa Labs | 18.81 | duck harness authors |
| 3 | NVARC3 | 16.07 | NVIDIA (AVO-related, see §6) |
| 4 | Yi-Chia Chen | 15.98 | |
| 5 | Daniel Franzen | 13.12 | |
| 6 | Matija Ludvig & Zhongwei Wang | 11.64 | |
| 7 | the last dance | 11.09 | |
| 8 | Tong Hui Kang | 10.78 | |
| 9 | Ebi | 8.68 | |
| 10 | Fususu | 8.65 | |

## 3. Teams > 3.85 WITH public notebooks (our study set)

Caveat: "score" = the author team's best LB. For #2–#10 below the notebook IS the
submission that produced (a large part of) that score; for Tufa the public ones are
lineage/infra versions.

| Team score | Team | Key public notebook(s) | What it is |
|---|---|---|---|
| 18.81 | Tufa Labs | jeroencottaar: `taaf-duck-harness-kaggle`, `simplified-submission-approach`, `...june-30-milestone-winner` | duck harness + infra; **submission = 110 test games** |
| 7.37 | Kyutai | thomasferraz `arc-agi-3-td-jepa-first-submission-5k-bfs` | **no LLM**: TD-JEPA world model + BFS-expert distillation |
| 7.10 | Tanaka Ai24 | `arc3-qwen3-6-duck-lb117-safety-v1`, `pathfinder-v2`, `...compact-trajectory-v1` | duck + **Qwen3.6-27B-FP8** + ledger/guards; plus a pure-CNN+search agent |
| 5.57 | (ruichardliu) | `milestone1-2nd-solution` | **Gemma-4-31B multimodal** + reflection + DEADSIG veto |
| 5.36 | THUI (yocybercode/sahasawatt) | `thui-animfast-b71-full25-r1`, `thui-v1-1-r2` (+~80 experiment grid) | **anim branch** (`animation_awareness`+`hard_noop_guard`) + analyzer yield 180 + uncapped output |
| 5.23 | 暗黑AGI (boristown) | `agi-duck-harness-fast-eval` | **stock Tufa bundle + Qwen3.6-27B-FP8**, no NVFP4 caps |
| 4.50 | Akagha Chimgozirim | chiakazirim `duck-qwen3-8-tuned` | NVFP4 profile + `analyzer_timeout` 900→1200 (twin-test +0.17) |
| 4.33 | wuliao_0 | `duck-qwen3-8-anim-base` | keithtyser NVFP4 control |
| 4.33 | Søren Ravn Andersen | `arc-agi-3-0-46-persistent-memory-bfs` | **pure search cascade**, no LLM (identical code also scored 0.46 elsewhere!) |
| 4.25 | (databasecsv555) | `bfs-pipeline-arc-agi-3-agent-v16` | offline game-family-dispatched solvers |
| 4.25 | zhengxuyu | `arc26-v1-give-up` | **BFS-only** + status-bar masking + hidden-field probing + give-up |
| 4.17 | keithtyser | `duck-qwen3-8-flash-next-nvfp4-mtp`, `duck-qwen3-8-27b-fp8` | the profile we run |
| 4.08 | Aman Atar | `arc-agi-3-hybrid-repl-agent` (+ `worldmodel-graph-...`) | NVFP4 + **KV 16 GB / batched 16K** profile |
| 4.03 | Ghazaros | `duck-qwen3-8-anim-base` | NVFP4 + GEPA prompt artifact + StateGraphExplorer |
| 3.95 | Julian Camilo Villa | `arc-agi3-nvfp4` family (~30 variants) | carry/ctx/long ablation grid |
| 3.91 | jakobbrggen | `taaf-anim-arc-agi-3-solver`, `taaf-model-20260815-q38-p1` | **anim branch author**, Qwen3.8-27B-FP8 snapshot |
| 3.71 | yanggod | `duck-flash-next-mtp`, `learn-on-a-run-you-throw-away` | NVFP4 control; no-LLM scout/trim/replay agent |
| 3.70 | shreyas4 | `lb-9-arc3-duck-v12-with-qwen-3-8-27b` | 27B FP8 duck v12 |
| 3.68 | bang1850 | `duck-balanced-ternary-10d-int4sp-v6`, `deep-reasoning-agent-179-183-levels` | ternary state hash; **EvidenceDecisionKernel** |
| 3.66 | mbmmurad | `lb-0-86-3rd-place-candidate-milestone` | milestone candidate |
| 3.62 | samrishb | `sam solver` + 2 more | flash-next variants |
| 3.58 | foysalemonshanto | `lb-9-arc3-duck-v12-with-qwen-3-8-27b` (288 votes) | 27B FP8 |
| 3.57 | nihilisticneuralnet | `[0.46] PM-BFS`, `graph-exploration-w-value-learning`, `MCTS` | pure search + small nets |
| 3.50 | XiaoYan12 | `lb-9-arc3-duck-v16-with-gpt-oss-120b` | **GPT-OSS-120B** + harmony parser fix |
| 3.46 | woguoat | `arc3-keith-repro-qwen38next` | keith repro |

Full machine-readable map: `data/sweep/notebook_score_map.json` (808 mapped kernels).

## 4. The score ladder — what actually separates the tiers

1. **3.7–4.3 (we are here): keithtyser NVFP4 profile ceiling.**
   `MAX_NUM_SEQS=8` vs 28 game workers (own diagnosis by ghazaros: "a queueing
   problem"), KV capped 5 GiB, prefix caching off, 8B model. wuliao 4.33 / ghazaros
   4.03 / yanggod 3.71 = same chassis, spread is variance + micro-knobs.
2. **4.3–5.4: two independent escapes.** (a) Drop the caps / bigger model:
   暗黑AGI 5.23 = stock Tufa bundle + Qwen3.6-27B-FP8, amanatar 4.08 = KV 16 GB
   profile; (b) **anim branch**: THUI 5.36 = `animation_awareness=True` +
   `hard_noop_guard=True` (intermediate-animation metadata in
   `last_action_result`, lets the guard tell a true no-op from an animated
   non-progress action) — works on both 27B-FP8 and NVFP4-8B.
3. **5.5–7.5: harness-level state discipline + multimodality.** tanakaai24 7.10 =
   duck + trajectory ledger + batch no-op guard + per-action `board_changed`;
   ruichardliu 5.57 = Gemma-4-31B image observations + reflection memory +
   DEADSIG dead-class veto (vetoing even LLM clicks).
4. **7.4+ (Kyutai): learned world models with exact-search distillation** —
   and, above all, **Tufa 18.81 / Han Solo 19.40: LLM reasoning hybridized with
   exact offline search infrastructure**.

## 5. THE single biggest discovery: offline game simulation

Five independent teams ≥ 4.25 load the shipped game source (`{gid}.py`, class
`ARCBaseGame`) from `/kaggle/**/environment_files/**` and solve levels **exactly**
on a `deepcopy`'d simulator: dijkstra-transfer → beam → IDA* → BFS (15–500k
states) → A* → MCTS, then either replay the solution (Pathfinder, zhengxuyu,
databasecsv555) or distill it into a learned policy (Kyutai TD-JEPA: BFS
solutions injected as priority-5–10 expert replay + warmup training).

Required supporting tricks (all discovered independently):
- **State identity**: md5 of pixels + **hidden-field probing** (diff scalar
  `game.__dict__` numeric attrs across simulated actions, fold into hash) +
  **status-bar masking** (HP/timer bars otherwise fragment dedup)
- **Level seeding fix**: `set_level(0)+RESET+RESET` then `set_level(N)`
  (RESET at N wipes `_current_level_index`)
- **Click candidates from objects**: centroids + bbox corners + dense non-bg +
  6px grid, deduped by effect hash — not blind 4096 clicks
- **Plan-length cap** `len(sol) ≤ max(8, 1.5×prev_level_sol)` (scoring is
  (human/actions)² — long plans regress) + greedy solution shortening
- **Background-thread solver** so `choose_action` never blocks

**OPEN QUESTION for our next run (zero-risk probe):** whether hidden-test games
also ship `.py` sources in the rerun container, or only the 25 public ones.
Tufa's own notebook says the submission evaluates **110 test games**; if sources
are unavailable there, the BFS side-channel still works as a local research tool
and the distillation path (Kyutai-style) is the deployment-safe variant.

## 6. External technique intel (web)

- **TD-JEPA** (Bagatella et al., ICLR 2026 / arXiv 2510): latent-predictive
  representations for zero-shot RL via goal-conditioned successor features —
  Kyutai's exact recipe: φ/ψ CNN encoders (latent 128, ‖z‖=√dim), ActionEmbedding
  (ACTION1-5/7 type + click x/y), SuccessorPredictor MLP, GoalConditionedActor,
  EMA target 0.995, GPI over ≤8 goals in one batched GPU pass; reward-shaped
  exploration (+0.5 changed, +0.5 new, −0.2 revisit, −0.35 no-change, +5 level,
  −8 death); family prior learned per action family; BFS as expert generator.
- **NVIDIA AVO** (Aug 2026): harness pushed Claude Opus 5 from ~30% → 100% RHAE
  on the public set in 6,624 actions; "built for GPU kernels, not games".
  NVARC3 (#3, 16.07) is NVIDIA. Confirms harness >> model quality.
- **Grid-JEPA public checkpoint**: `huggingface.co/guychuk/arc-agi-3-grid-jepa`
  — JEPA world model weights for ARC-AGI-3, reusable as encoder init/prior.
- **Tycho** (arXiv 2607, Jul 2026): active abstraction with programmatic world
  models — actor requests model-building; matches our P2/P3 plan.
- **Qwen3.6-27B** (Apr 2026, Apache 2.0): dense 27B, 262K ctx, gated
  delta-net hybrid attention; FP8 snapshot in use by 7.10/5.23 teams.
- Negative evidence (consistent with earlier community intel): advisory-only
  small-model critics add nothing (lucifer19 BlackCat 1.47 parent, no gain;
  iamjasonfeng 6-proposer Sandwich 1.22, latency-bound). Small models must
  **filter/act/veto**, not advise.

## 7. Operational findings

- **GPU quota is being consumed by non-ARC jobs** on kragglenote2forwork:
  `ch-unet-r34-f0..f4/full2` (Sep 23), `umud-seg-finetune-cpu`, `cha22-agent`
  (Sep 24 14:23 UTC). This is the direct cause of the Sep 23 quota exhaustion
  ("Maximum weekly GPU quota of 30.00 hours reached") and blocks v5.
- Hidden eval = **110 games** (Tufa notebook) → per-game budget math and
  wave-based caps must assume 110, not 25.
- Identical code scoring 4.33 vs 0.46 (sorenravn vs nihilisticneuralnet) proves
  **binary failure modes** (threading, budget math, gateway waits) dominate this
  agent class → watchdogs + health canaries + assert-teeth are score-critical.
- gpt-oss-120b lesson (xiaoyan12 v16): server parser crashes 500 whole requests;
  patch the parser + pre-flight canary probes before burning a 9h run.
