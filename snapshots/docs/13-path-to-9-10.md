# 13 — Path to 9–10: Descriptive Research & Plan (2026-09-25)

Mission: from **3.85 (rank 214/3,296)** to **LB 9–10 ≈ rank 9–11 of 812 scored teams = top ~1.3%**, by competition end (2026-11-02). This document lists **everything found that could achieve a high score**, with evidence, expected impact, cost, risk, and a sequenced execution plan. Sources: full LB pull today (`research/lb_full_2026-09-25.json`), 808-kernel sweep + 29 deep-dive analyses (docs/10), competitive intel (docs/12), scoring methodology (docs/02).

---

## 1. Target reality check (LB pulled 2026-09-25)

| Rank | Team | Score | Note |
|---|---|---|---|
| 1 | Lord Han Solo | **19.40** | passed Tufa Sep 23; no public notebook |
| 2 | Tufa Labs | 18.81 | duck authors; public infra lineage |
| 3 | NVARC3 (NVIDIA) | 16.07 | |
| 4 | Yi-Chia Chen | 15.98 | private |
| 5 | Daniel Franzen | 13.12 | private |
| 6 | Matija Ludvig & Zhongwei Wang | 11.64 | private |
| 7 | the last dance | 11.09 | private |
| 8 | Tong Hui Kang | **10.78** | private |
| 9 | Third Intelligence | 8.81 | new Sep 24; private |
| 10 | Ebi | 8.68 | private |
| 11 | Fususu | 8.65 | private |
| … | | | |
| **214** | **Kragglenote2 Forwork (us)** | **3.85** | dense cluster 3.85–3.87 (dozens of teams) |

**Key structural fact: the 9–10 zone is EMPTY.** There is a clean gap between 10.78 (rank 8) and 8.81 (rank 9). A score of 9–10 lands at rank **9–11 = top 1.3% of all scored teams**. Distribution: 19–20: 1 · 18–19: 1 · 16–17: 1 · 15–16: 1 · 13–14: 1 · 11–12: 2 · 10–11: 1 · 9–10: 0 · 8–9: 3 · 7–8: 8 · 6–7: 7 · 5–6: 21 · 4–5: 116 · 3.5–4: 206.

**None of the nine teams above 8.81 publishes a competitive notebook.** Their approaches are private. The public evidence for how to get there comes from: Tufa (18.81 infra), Kyutai (7.37, full no-LLM pipeline public), tanakaai24 (7.10, full 27B pipeline public), and five simulator teams ≥4.25 (public). Plus title-claims: two public notebooks named `lb-9-arc3-duck-v12-with-qwen-3-8-27b` and `lb-9-arc3-duck-v16-with-gpt-oss-120b` (authors' private runs with those configs reportedly hit ~9; their own teams' visible scores are lower — treat as weak-but-consistent signal).

---

## 2. Score math — what 9–10 actually requires

Formula (docs/02): per-level `min(human/agent, 1.15)²` if completed else 0, weighted by level index; per-game normalized by `Σ(1..N)`; total = mean over **110 hidden games** × 100.

Anchors: we complete 36/183 public levels ≈ 0.2 levels/game → 3.85. Leader ≈ L3–L4 at ~1–1.5× human actions on most games → 18.8–19.4.

Concrete scenarios that produce **9–10** (assume N≈8 levels/game avg, Σ weights = 36, efficiency e ≈ human parity i.e. level score ≈ 1):

- **Scenario A (breadth):** reach L2 on ~all 110 games → per-game ≈ (1+2)/36 = 0.083 → **9.2**.
- **Scenario B (balanced):** L3 on ~60 games (0.167 each) + L1–2 scattered elsewhere → **~10**.
- **Scenario C (depth):** L4–L5 on ~30 games with 1.15× efficiency → **~9–11**.

**Translation: 9–10 = "complete levels 2–3 with near-human efficiency across MOST of the 110 hidden games", or fewer games one level deeper.** Versus today: we must roughly 10× the completed-level mass (0.2 → 2–2.5 levels/game equivalent) and hold efficiency near human parity (waste is quadratically punished). No incremental knob does this; it requires the tier jumps documented in §3.

---

## 3. The evidence ladder (what separates the tiers — all from public kernels)

| Tier | LB band | Teams (evidence) | What they have that the tier below lacks |
|---|---|---|---|
| T0 | 0–3.5 | ~600 teams | broken/naive pipelines |
| T1 | 3.7–4.3 | **us 3.85**, wuliao 4.33, ghazaros 4.03, keithtyser 4.17, yanggod 3.71 | same keithtyser NVFP4-8B chassis: `MAX_NUM_SEQS=8` vs 28 workers (queueing bottleneck), KV 5 GiB, prefix-cache off |
| T2 | 4.3–5.6 | 暗黑AGI 5.23 (stock bundle + **27B-FP8**), THUI 5.36 (**anim branch**), ruichardliu 5.57 (Gemma-4-31B + DEADSIG), amanatar 4.08 (KV 16 GB) | (a) bigger model OR (b) `animation_awareness` + `hard_noop_guard` OR (c) bigger KV |
| T3 | 5.6–7.5 | tanakaai24 **7.10** (27B + trajectory ledger + batch no-op guard + per-action board_changed), Kyutai **7.37** (no LLM: TD-JEPA + BFS distillation) | harness-level state discipline / learned world models with exact-search distillation |
| T4 | 8–11 | Third Intelligence 8.81, Ebi 8.68, Fususu 8.65, THUI-person 10.78 | private; inferred: T3 stack + search/simulation at scale |
| T5 | 11–19.4 | Han Solo 19.40, Tufa 18.81, NVARC3 16.07, Yi-Chia 15.98, Franzen 13.12 | LLM reasoning **hybridized with exact offline search infrastructure** (Tufa documented: 110 test games, REPL + analysis) |

**The 9–10 target = clearing T3 fully and buying a seat in T4.** Every documented jump uses one of: bigger model, animation-aware no-op discipline, KV/queueing fix, exact simulation, learned world-model distillation, state-ledger discipline. All are in our lever matrix (§5).

---

## 4. THE master lever: offline game simulation (five independent teams ≥ 4.25)

The shipped competition data contains game source `{gid}.py` (class `ARCBaseGame`) under `/kaggle/**/environment_files/**`. Teams load it and **solve levels exactly** on a `deepcopy`-ed simulator: dijkstra-transfer → beam → IDA* → BFS (15–500k states) → A* → MCTS, then **replay the solution** into the real environment (or distill it into a learned policy — Kyutai).

Required supporting kit (all independently discovered by ≥2 teams — treat as mandatory):
1. **State identity**: md5 of pixels + hidden-field probing (diff scalar `game.__dict__` attrs across simulated actions, folded into hash) + status-bar masking (HP/timer bars fragment dedup otherwise).
2. **Level seeding fix**: `set_level(0) + RESET + RESET` then `set_level(N)` (RESET at N wipes `_current_level_index`).
3. **Click candidates from objects**: centroids + bbox corners + dense non-bg + 6 px grid, deduped by effect hash — not blind 4096 clicks.
4. **Plan-length cap** `len(sol) ≤ max(8, 1.5 × prev_level_sol)` + greedy solution shortening (score is `(human/actions)²` — long plans regress).
5. **Background-thread solver** so `choose_action` never blocks the env loop.

**The open question that decides everything: do the 110 hidden-test games also ship `.py` sources in the rerun container?**
- If YES → exact search on hidden games = the single path to T4/T5 (this is what Han Solo/Tufa's 19 looks like).
- If NO → the deployment-safe variant is **Kyutai-style distillation**: BFS-expert solutions generated offline on the 25 public games → train TD-JEPA policy (φ/ψ CNN encoders, ActionEmbedding incl. click x/y, successor predictor, EMA 0.995, GPI over ≤8 goals; reward-shaped exploration) → run the learned policy on hidden games. Kyutai: **7.37 with zero LLM**.
- **Probe plan (zero-risk):** v6 kernel logs `os.walk('/kaggle')` + environment file inventory to stdout during the rerun → we read it from the run log and KNOW, one run, which branch to build.

---

## 5. Exhaustive lever matrix — everything found that could achieve a high score

Impact = expected ΔLB at our current position (3.85), calibrated from the evidence teams. Cost in GPU-days of our 30 h/week quota. All levers are additive; the order in §7 sequences them.

| # | Lever | Evidence | ΔLB | Cost | Risk | Dependency |
|---|---|---|---|---|---|---|
| L1 | **Qwen3.6-27B-FP8 chassis swap** (replace NVFP4-8B). Public datasets: `jeroencottaar/taaf-kaggle-source(-share)` + `driessmit1/arc3-vllm-h100-wheelhouse-v3` + `driessmit1/vrfai-qwen3-6-27b-fp8-hf-snapshot`. Verified attachable today. | 暗黑AGI 5.23 stock+27B; tanakaai24 7.10; `lb-9` title claims | **+1.5–3** | 0.5 d build, 1 run | Med: slower decode (~40–60 t/s single stream); KV budget actually improves (96 GB GPU) | — |
| L2 | **Anim branch flags** `animation_awareness=True` + `hard_noop_guard=True` (distinguishes true no-op from animated non-progress; kills wasted env actions — quadratically punished) | THUI 5.36 (+ our local runs: anim-base 9.91 local), works on 8B and 27B | **+0.5–1.5** | 0.2 d | Low: flag + guard, toggleable | — |
| L3 | **KV/queueing fix**: raise `MAX_NUM_SEQS`, KV 16 GB batched 16K, prefix caching ON; align serving slots with 28 workers (ghazaros: "a queueing problem") | amanatar 4.08; own v14 telemetry (52.6% zero-action decisions) | **+0.3–1** | 0.2 d | Low-med: OOM watch on 27B | co-design with L1 |
| L4 | **Offline simulation + exact search replay** (BFS/IDA*/A* + kit above) | zhengxuyu 4.25 BFS-only(!), databasecsv555 4.25, pathfinder, 5 teams | **+2–6 if hidden sources ship** (this is the T4/T5 mechanism) | 2–4 d CPU build (no GPU) | Med: unknown hidden availability; threading bugs are score-fatal | probe (P0) |
| L5 | **Hidden-source probe**: log full `/kaggle` walk + env inventory in rerun | own design (sweep doc §5 open question) | informational | 0 | None | run v6 |
| L6 | **TD-JEPA distillation fallback**: BFS experts on 25 public games → train tiny policy → run on hidden | Kyutai 7.37 public end-to-end; TD-JEPA ICLR 2026; `guychuk/arc-agi-3-grid-jepa` checkpoint free | **+1.5–3.5** (deployment-safe world-model path) | 2–3 d CPU+1 GPU train | Med: generalization to hidden games | BFS data (from L4 build) |
| L7 | **Trajectory ledger + batch no-op guard + per-action board_changed** (state discipline at harness level; extends our worldmodel-v2 diff/zones) | tanakaai24 7.10; ruichardliu 5.57 reflection+DEADSIG | **+1–2** | 1 d | Low (toggleable) | L1/L2 chassis |
| L8 | **NOOA-lite memory + verification** (typed model-callable memory, sync_state prediction-match, world-model skill prompt, append-only searchable log) | docs/12: +11.8 / +8.5 pts on frontier; verification #1 in 2607.15439, helps most at LOW capability = us | **+0.5–1.5** | 1–2 d CPU | Low: fail-open design | L1 chassis |
| L9 | **GPT-OSS-120B chassis** (official template model; public; harmony parser fix from xiaoyan12 v16; MXFP4 ≈ 60 GB fits 96 GB) | xiaoyan12 notebook + `lb-9` claim; official template | alt to L1 (not additive) | 0.5 d | Med-high: parser 500s, slower decode | — |
| L10 | **Click-candidate generation from objects** (centroids/corners/dense/6px grid, effect-hash dedup) for MOUSE games | pathfinder + simulator teams | **+0.5–1.5** on click games | 0.5 d | Low | — |
| L11 | **Plan-length caps + solution shortening + RESET discipline** | simulator teams; docs/02 (1.15 cap → no over-optimization; RESET only on provable dead-end) | **+0.3–1** (protects, not adds) | 0.2 d | Low | L4 |
| L12 | **Ops teeth**: watchdogs, canaries, background threads, give-up, 110-game budget math, quota protection (no non-ARC GPU jobs) | identical code 4.33 vs 0.46 (binary failure modes); our v14 telemetry; sweep §7 | **+0.5–2 (variance floor)** | 0.5 d | None | — |
| L13 | **Multimodal VLM perception** (Gemma-4-31B image obs + reflection) | ruichardliu 5.57 milestone-2nd; ko0kip | **+0.5–1** but conflicts with L1 chassis | 1 d + new serving | Med-high | only if L1 fails |
| L14 | **Small-model router/critic** (our M-series JEPA-lite: pre-action sanity, novelty signal) | Agentic-JEPA/TD-JEPA recipes; NEGATIVE evidence for advisory-only critics (lucifer19 1.47, iamjasonfeng 1.22 — critics must filter/act/veto, not advise) | **+0.5–1** late-stage | 2–3 d | Med | after L4/L6 |
| L15 | **Ensemble/parallel games strategy** (wave-based caps by expected completion value, aging credit) | our scheduler design; Tufa 110-game budget | **+0.3–0.8** | 0.5 d | Low | L3 |

Explicit **non-levers** (evidence-backed): efficiency tuning beyond human parity (1.15 cap), advisory small-model critics, mandatory executable world-model deliverables (2607.15439: textual won twice at gpt-5.5), auto-repair-to-transition-match loops (Tycho 88.49→83.07), heavy hand-built perception pipelines (Tufa: tools hurt; forge: best run disabled everything).

---

## 6. Chassis decision

**Primary: L1 (27B-FP8) — not L9 (GPT-OSS-120B).** Reasons: three independent teams score 5.2–7.1 on it; full public recipe (datasets verified attachable today); FP8 serving is our known territory; KV headroom improves vs 8B. GPT-OSS-120B stays as a contingency branch if 27B throughput disappoints (parser patch already documented).

Hybrid final state (T4 shape): **27B-FP8 LLM harness (ledger + anim guard + NOOA-lite) + exact-search replay where sources exist + TD-JEPA distilled policy where they don't.**

---

## 7. Sequenced plan (6 weeks to Nov 2; 30 h GPU/week; 1 scored run/day possible)

| Wave | When | Build (CPU-first) | Run | Gate → next |
|---|---|---|---|---|
| **v6 "chassis swap"** | Sep 26–28 | Attach 3 public datasets; port worldmodel-v2 patch to 27B bundle; anim flags ON; KV/queueing fix; **hidden-source probe logging**; ops teeth (L12) | 1st GPU window | **LB ≥ 5.0** → continue; <4.2 → rollback to 8B + L2/L3 only |
| **v7 "discipline"** | Sep 29–Oct 3 | Trajectory ledger + batch no-op guard + board_changed (L7); NOOA-lite memory + sync_state verification (L8); click candidates (L10); plan caps (L11); scheduler waves (L15) | 1–2 runs | **LB ≥ 6.5** → T3 reached |
| **v8 "search"** | Oct 4–14 | Branch on probe result: (a) sources ship → integrate exact-search replay + caps (L4, kit from §4); (b) no sources → BFS experts on 25 public games + TD-JEPA distill (L6) | 2–3 runs | **LB 8–10.5** → T4 |
| **v9 "polish"** | Oct 15–Nov 1 | Router for per-game strategy selection (L14), efficiency hygiene, variance damping (multi-run best-of via daily slots), final submissions on best 2 variants | daily runs | **hold 9–10 / rank ≤ 11** |

GPU budget: ~5 h/run × ~5 runs/week ≈ 25 h — inside quota **only if non-ARC GPU jobs stop consuming the account** (sweep §7 documented `ch-unet-r34-f0..f4`, `umud-seg-finetune-cpu`, `cha22-agent` eating the weekly 30 h — this remains the #1 operational risk; it alone blocked v5).

Fallback ladder if a wave misses its gate: 27B fails → 8B + L2+L3+L7+L8 (est. 5.5–6.5) → still add L6 distillation (est. 7–8.5) → 9–10 needs L4 to pay off; if neither probe branch pays, realistic landing is 6.5–8 (rank ~20–40) — still top 3%.

Milestone-2 (Sep 30, open-source): orthogonal bonus track; only viable if v6 lands green by Sep 28 — decision needed from user.

---

## 8. Variance doctrine (why identical code scores 4.33 and 0.46)

sorenravn vs nihilisticneuralnet: identical BFS code, 4.33 vs 0.46 — binary failure modes (threading, budget math, gateway waits) dominate this agent class. Consequences: (1) every run ships watchdogs + health canaries + assert-teeth; (2) we never burn a run on an untested patch (30+ green preflight); (3) expect ±1 LB run-to-run variance — plan gates on bands, not points; (4) daily slots are best-of-N sampling: always keep the best-confirmed kernel as the standing submission.

## 9. Immediate next actions (this week, CPU-only until GPU frees)

1. Build v6 notebook: dataset swap + anim flags + KV fix + probe logging (CPU-testable patch logic against real bundle).
2. Port worldmodel-v2 patch to the 27B taaf bundle (idempotent, fail-open, 20+ unit tests).
3. Start BFS expert generation on 25 public games (CPU, background) — needed by BOTH v8 branches.
4. Keep v5 push-retry armed (worldmodel-v2 on 8B) as the variance-floor submission.
5. User decisions: (a) stop non-ARC GPU jobs on the account; (b) Milestone-2 go/no-go by Sep 28.
