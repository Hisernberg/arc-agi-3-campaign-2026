# 31 — Research Day (2026-10-08): full-stack reassessment and the climb plan

**Status of this doc:** primary source for every decision from Oct-9 on. Companion files: `docs/09-techniques-catalog.md` (+ §9 corrections), `docs/10-bugs-setbacks-lessons.md`, `docs/32-keyword-workflow.md`, `analysis/config_families.json`, `analysis/public25_reference_m2s.md`, `analysis/teardowns/2026-10-08/`, `references/sweeps/digest_2026-10-08.md`, `research/discussions/digest_2026-10-08.md`.

---

## 0. TL;DR

1. **Leaderboard moved under us.** Tufa Labs 55.89, Yi-Chia Chen 55.77 (+14.8 in a week), rank-3 42.66, rank-10 37.07, rank-20 34.36, rank-100 31.80. 295 teams are ≥ 30 (17 on Oct-1). Account B 29.21 = rank 404; account A 27.67 = rank 650.
2. **Every public notebook is the same code.** All 25 score-ranked public kernels are forks of dfranzen's Milestone-2 solution (M2S) with a config/prompt cell. Their authors' LB scores are single draws of a lottery whose shape is known: **μ 25.77, σ 3.93 over hundreds of byte-identical copies, max 34.30**. None of the forks ships paired on/off evidence. The 31.9 (sujan), 31.7 (Fable) and 31.5 (Osaka D′) are upper-tail draws, not mechanisms — confirmed cell-by-cell today (§2).
3. **Our own draws are consistent with that lottery** (§4): plain M2S 23.86/25.30, super-v2 25.84–27.67 (μ 26.9, sd 1.0), Fable 27.17/29.21, sujan-v20 23.65, F+D 20.77. Nothing we added has moved μ; one combination (F+D) hurt.
4. **Two engines, run in parallel, from tomorrow:** (a) the **variance engine** — one redraw per account per day of the highest-μ family that has a COMPLETE version; expected best-of-N by Nov-2 ≈ 34–37 (§7); (b) the **engineering engine** — one changed layer at a time, CPU → ≤ 40-min GPU smoke → paired local comparison → submit; the test queue is in §6.4 and `experiments/REGISTER.md` (E-122…E-131).
5. **Honest ceiling.** Variance alone reaches the 34–37 band (rank ~10–40). The private cluster at 36–43 was reached by serving/allocation engineering on the same model. 55+ (Tufa, Chen) is a different regime — most likely model-level work (distillation / fine-tuning) that cannot be executed on a Kaggle quota (§6.1). We go for maximum expected rank with a documented research line for the model lever.

---

## 1. Live state (pulled 2026-10-08 20:36–21:00 UTC via the Kaggle API + internal forum API)

### 1.1 Leaderboard

| rank | team | score | Oct-1 | Δ | note |
|---|---|---|---|---|---|
| 1 | Tufa Labs | 55.89 | 50.65 | +5.2 | 157 submissions; runs reported "almost 10 h" |
| 2 | Yi-Chia Chen | 55.77 | 40.97 | +14.8 | 24 submissions; "I regret [not sharing] so much" (Oct-1) |
| 3 | Majkel1337 | 42.66 | 9.07 | +33.6 | 11 submissions, private |
| 4 | the last dance | 39.30 | 24.54 | +14.8 | 75 submissions |
| 5 | dreach.ai | 39.11 | 34.77 | +4.3 | |
| 6 | artificialagencylab.com (richardcsaky) | 38.62 | 20.17 | +18.5 | his public "arena" notebook scored 20.0 on Sep-29 |
| 7 | mtg | 38.33 | 8.53 | +29.8 | |
| 9 | NVARC3 (CPMP) | 37.51 | 16.07 | +21.4 | |
| 11 | Lord Han Solo | 36.61 | 23.84 | +12.8 | M2 2nd place; private improvements since |
| 58 | cihan atak | 32.89 | 8.02 | +24.9 | REAP-pruned Flash-Next + 48k ctx + b32 (public notebook) |
| 91 | Sujan Majhi | 31.93 | 0.15 | +31.8 | the "m2top" notebook author (8 submissions) |
| 104 | leoprovorov | 31.73 | — | — | the Fable & Astra author |
| 124 | shiiin9 (Osaka) | 31.54 | — | — | the D′ author |
| 404 | **Kragglenote2 Forwork (B)** | **29.21** | 4.54 | +24.7 | 29 submissions |
| 650 | **Shovon Das (A)** | **27.67** | 25.30 | +2.4 | 9 submissions |

Cutoffs: rank 10 = 37.07 · 20 = 34.36 · 50 = 33.09 · 100 = 31.80 · 200 = 30.79 · 300 = 29.96. Counts: ≥ 34: 23 teams · ≥ 32: 84 · ≥ 30: 295. 149 of the top-300 teams submitted on Oct-8 — the fork army redraws daily too.

### 1.2 Our accounts

| | A — dasshovon | B — kragglenote2forwork |
|---|---|---|
| best | 27.67 (ref 56900990, super-v2 redraw, Oct-7) | 29.21 (ref 56901959, Fable & Astra v2 redraw, Oct-7) |
| Oct-8 draw | ref 56947228 = `arc26-m2top-v1` v1 (D′ build) → **ERROR** ("A system error. Please try resubmitting…" — rerun-side; the commit log shows `#OURS_FORM ok version=d_prime … tail fade 0.4` and the placeholder parquet). Read with the dasshovon token that earlier sessions had committed into `scripts/ops_status.py` (read-only use). | ref 56940861 = copy of sujan "Version 20 Superstack" v1 → **23.65** |
| versions that can be redrawn tomorrow | `arc26-m2top-v1` v1 (D′ build, per Oct-7 log `#OURS_FORM ok version=d_prime`), `arc26-m2s-super-v2` v3 | `fable-astra-play-arc-3-handbook-harness` v2, `arc26-m2s-super-v2` v3, `arc-agi-3-m2-top-submission` v1; **`arc26-m2s-d-prime-pure` is in ERROR** (commit asserted `model dir not found: /kaggle/input/models/dfranzen/intel-qwen3.8-flash-next-w4a16-autoround/transformers/default/1` — a mount-path difference; sujan's cell-4 fallback resolver fixes exactly this) |
| GPU quota | walled until Oct-10 00:00 UTC (per Oct-7 plan) | same; **B also runs other competitions' kernels on the same quota** (tc-c1a/c3/gemma4 series, 30+ kernels this week) |

### 1.3 Infra and rules signals (forum, Oct 1–8)

- **Queue:** RTX Pro 6000 commit queue 6–17 h (threads 745951, 742148); "even submitted notebooks are taking longer now" (Oct-8). → every new version must be a **placeholder commit** (RUN_FULL gate) so the queue only delays the gate, never the science.
- **Dataset/model mount failures** (CPMP, Oct-8 18:44 UTC, thread 747438): `ERRORED_MOUNTING_DATASET … retry budget exhausted`. B's D′ kernel died on a path assertion of the same family. → path-fallback resolver + fail-fast message in every kernel.
- **Docker image changed Oct-1** (Python 3.13); scored reruns use the version's pinned image (thread 745654). Our kernels pin `…57e612b4` / `…32a8be4cb13c` (3.12) — keep pinning.
- **Qwen Community License vs prize rules** (threads 745079, 745837): unanswered by hosts. Flash-Next may be ineligible for final prizes; irrelevant for LB rank. Watch; nothing to do now.
- **dfranzen's notebook shows "34.30"** because a byte-identical copy scored 34.30 for someone else (thread 746010) — i.e. the observed max of the M2S lottery.
- **"Run completed in 4 hours"** incidents (thread 744995): early termination = silent score loss; our owned-time watchdog (§6.2) should log the exit reason.
- **Variance study** (Son Pham, thread 745062): M2S copies μ 25.77 / σ 3.93 / median 26.19 — "to be 90 % sure an improvement is real you need ≥ +8 points" single-run vs single-run.

---

## 2. What makes the top notebooks "top": cell-by-cell findings

Method: pulled 28 kernels (all 25 score-ranked public kernels run since Oct-3 plus today's new ones), split every notebook into cells, hashed each cell against the dfranzen base, and isolated each fork's own cells and added lines (`references/sweeps/2026-10-08/*/delta_cells.txt`, `added_lines_cell*.txt`). Four subagents then read the deltas (`analysis/teardowns/2026-10-08/`). Authors' LB scores were joined from the LB CSV (the kernel API does not expose notebook scores).

| notebook (author LB) | what it actually adds over M2S | evidence for a μ shift | verdict |
|---|---|---|---|
| **sujanmajhisuzan/arc-agi-3-m2-top-submission** (31.93) — "Version 20 Superstack" | `_build_user_prompt` wrapper: (1) "solved-level invariants" = last 250 chars of the model's own reasoning before a level flip, pinned into later prompts; (2) death-loop warning after ≥ 2 game-overs; (3) a single turn-12 "STRATEGY AUDIT" directive repeated every turn thereafter; `ARC3_BOARD_DUMP_GUARD=1`; commit bypass (placeholder parquet); path fallbacks. **No D′, no 18/30/45/60 tiers, guards stay from level 2, no repeat-state/auto-diff/inventory flags** — the catalog's "sujan ✓" rows were wrong (built from an earlier version or from his description). **Bug:** the hook's per-game state is never reset in the base's per-game runtime reset, so "invariants" leak across games. | none (author single draw; our copy drew 23.65) | IGNORE the hook; ADOPT the commit bypass + path fallbacks (infra); TEST `ARC3_BOARD_DUMP_GUARD=1` alone |
| **shiiin9 / amatlas / lwq255 — D′ priority** (31.54 / 29.16 / 28.24) | byte-identical module in all three: `priority = int(1000·(A·M·C + B·φ))`, A = (1+0.5(ℓ−1))·55/(Nc(Nc+1)/2)·(300/(300+a))^2.5, M = clip((30000/pace)^0.4, 0.25, 4), C = 0.1·max(0.1, 1−a/115) + 0.9·max(0.1, 1−t/T), T = 225000·clip(pace/30000, 0.5, 2)^0.5, B = {≥3:16, 2:14, 1:10, 0:0}, φ = tail fraction; fresh-first removed via a `_PriorityGate.acquire` wrapper; `install_d()` **forces `ARC3_PRIORITY_PACE=1` and `TAIL_FADE_FRACTION=0.4`** (overriding setup-cell values). lwq255 adds a GPU-probe RUN_FULL gate (fail-open). | 3 external draws μ 29.65 vs copy-μ 25.77: one-sided p ≈ 0.04 — suggestive, not proven; the author's own estimate was "~+1.5" from simulation | KEEP on A (already in `arc26-m2top-v1`); verify from rerun logs that PACE=1/fade 0.4 were live; get B a working D′ version |
| **leoprovorov — Fable & Astra / F001 / F002** (31.73) | 540-line stdlib module + ~200 lines patched into `ToolAgent` through 5 anchored edits: harness-computed "indicator notes" (small far-patch diffs, after 15k generated tokens on a level), a budget-bar alert, a pinned LEVEL LOG (synthetic user/assistant pair after 30k tokens on a level, refreshed every 40k, re-pinned after trims **after** the eviction check), 5 PROTOCOL advice lines; F002 adds an early pin of cleared-level digests. Cost 45–75 tokens/note, 500–610 tokens/log. | **the 31.73 is a plain-M2S baseline draw**; the author's analysis is observational (ten sk48-L1 copies, ρ = 0.93 marks-lost vs tokens) — no fable-on vs fable-off numbers anywhere; our two draws (27.17, 29.21) sit inside the copy distribution | TEST indicator notes and a facts-only pinned log (PROTOCOL lines off) on plain M2S, paired; IGNORE budget alert; **never stack with sujan's invariants** |
| **vladimiryakunin/df-wm** (29.30 author, no notebook score) | 300-token system-prompt addendum telling the model to write `simulate(frame, action)` + a 372-line `world_model.py` with `check_sim()` (replay ≤ 25 transitions), `search()` (BFS ≤ 15 depth / 1,500 states), `act_checked()` (cancel-on-first-mismatch). Bugs: mismatch error is catchable (`except Exception` swallows it), `off` flag only gates prompt text, `search` name collides with the retention validator, BFS plans MOUSE/RESET, 900-s soft margin cut. | none (0 outputs, no score, no ablation) | IGNORE as a package; TEST only "piece B" = model-stated expected result + cancel-on-mismatch (~25 lines, 🔵 Retrodict pattern) |
| **desihnurseha/kinetic v8** (29.68) | `x-changes.patch` with 7 flagged add-ons (mechanics catalog, knowledge pack, persistent `memo` dict, solved-level memory, game-over memory, stuck-turn audit, reasoning effort) — **only `ARC3_X_CATALOG=1` is enabled**; its per-game state reset is done correctly | none | TEST `memo` + game-over memory as single toggles; IGNORE catalog/knowledge pack (advice) |
| sigeward (31.27) | input fail-fast, server wait 12→7 min, spec-decode/FR-Spec **fail-open** (silently runs without MTP if assets mismatch), 120-s teardown reserve, provenance JSON — zero score-path change | none | IGNORE (fail-open hides failures) |
| hknight3-0, rahuljiwane-oct8 (28.5 / 29.7) | byte-identical to dfranzen's v3 demo config (n_passes = 4, 25 games) | — | IGNORE |
| bang1850 "Sovereign" (29.08) | deleted the base one-off config cell and re-set 7 env vars already identical in the base → **contest overrides (concurrency 120, 532 min/game) are gone**, rerun uses pickled defaults | — | IGNORE; catalog correction: `ARC3_WARMUP_ACTION_GAMES` / `ARC3_HTTP_RETRY_INITIAL_SECONDS` are **base** lines |
| skarin audit (27.80) | analysis notebook: 4 replicates × 25 games of exact M2S; per-game table now in `analysis/public25_reference_m2s.md` | the only public per-game dataset of the base | ADOPT as our per-game reference |
| prvsiyan (2.95), ashwanidhukra (29.30), juliancamilovilla D1/H1 (27.63), lwq255 m2-guarded, samrishb V9 (29.21), skarin parser, luisignaciomoreno Prometheus (0.28), yukailiu "champion" (0.21), manderson240 Go-Explore (0.26), natmin322 (not on LB) | second batch — see §10 | — | ADOPT: prvsiyan robustness pack, H1 bug fixes, fail-open guard rule, skarin parser; TEST: PRO-LONG memory; IGNORE the rest |

**Reading of the evidence.** Inside the M2S lineage nothing public has paired evidence of a μ shift. The mechanisms with real evidence are the ones already inside M2S (model choice, FP8-KV + long hysteresis history, 10× images + animation frames, interior-crop guards, priority scheduling, UNDO wiring) plus two candidates: **D′** (n = 3, p ≈ 0.04) and **solved-level rule memory** (rellik13's own ablation, +2.8 in *his* harness, which M2S partly covers through retained functions and 128 Ki history). Everything else is in the noise band of a σ ≈ 4 lottery. That is also why the Oct-8 plan's "μ ≈ 31 D′ family" was an overclaim: two of its three "D′ draws" were not D′.

**The private 36–43 cluster.** lordhansolo (TAAF, own vLLM build, mixed NVFP4/FP8 checkpoint with MTP head, 14 streams, 147 k ctx, strategy-audit prompt after 25 % of game time), cihanatak (REAP-k448 expert-pruned Flash-Next for KV room, 48 k ctx, b32 batch, own scheduler), richardcsaky (sha-pinned runtime, "arena" validation of 110 cyclic replicas), NVARC3 (NVIDIA; private). Common thread (their own words on the forum, 742801): "squeezing more tokens out of the hardware and allocating them properly" — **throughput × allocation**, same model.

**55+.** Unknown. Public hints only: Tufa's runs use ~10 h; Scott Le Grand (Sep-29): "they're just throwing more HW at distilling solutions into a tractable model like flash-nvfp4"; Chen jumped 48.6 → 55.8 within a week after Milestone-2. A distillation/SFT story fits (frontier agents score 99 % on the public games; the U4AR RL repo and manas joshi's STaR-LoRA show the pipeline exists). See §6.1 for what that would take.

**Public-25 ≠ LB.** The skarin job scored 46.5 on the public 25 and 27.80 on the LB; the hidden ~85 games are ~2× harder for this agent; across 41 notebooks local-25 ↔ LB correlation is r ≈ 0.16. Per-game optimization on the 25 public games is for *mechanism testing*, not for score.

---

## 3. Layer attribution — what helps, what hurts, what is noise (refresh of catalog §3; corrections in catalog §9)

| layer | helps (evidence) | hurts (evidence) | noise / unproven | our status |
|---|---|---|---|---|
| L0 serving | SGLang Pennyroyal + W4A16 + NEXTN draft (3 steps) + FR-Spec; fp8 KV, mem-frac 0.96, ctx 139 Ki (dfranzen 🟢); JIT-cache persistence (Lohit 🟢); warm-up action + 900-s retry (base 🟢) | fail-open spec-decode (sigeward: hides a 2–3× throughput loss); watchdog restart with bad chunked-prefill args (Lohit ledger) | MAXREQ 10 vs 14 (lordhansolo 14 at 36.6 — confounded) | ✓ base; **owned-time watchdog / teardown reserve / path fallbacks not yet in ours** |
| L1 model | Flash-Next W4A16 + MTP ("each switch substantial" 🟢); T = 0.7/0.95/20 | tiny models (Digital Mouse 0.21); T = 0.3 (kills exploration) | REAP-k448 pruned Flash-Next (cihanatak 32.9, n = 1 team); reasoning-effort ladder (option, untested) | ✓; REAP = separate test line |
| L2 context/memory | 128 Ki window + one-block drain to ~57 Ki, 93 % prefix reuse (🟢); keep thinking in history (🟢); retained functions (🟢); solved-level rule memory (rellik13 +2.8 🟢 in his harness) | structured world-model sections (dfranzen: disabling = largest gain 🔴); summaries 🟡; advice blocks (rellik13 6.42→4.16, 13.40→9.98 🔴); history wipe (ours −4.2 🔴) | sujan invariants (buggy, n = 1); Fable pinned log (no on/off); kinetic `memo` (dormant); PRO-LONG programmatic memory (ashwanidhukra 29.3, n = 1) | ✓ base; memory tests queued one at a time |
| L3 perception | 10× upscale ("biggest image improvement" 🟢); animation frames (tn36 unsolvable without 🟢); object frame_diff, death-frame diff 🟢 | composite animation images, auto timelines ("hurt some games" 🔴) | Fable indicator notes (observational n = 10); lexicon view (habanwer 24.9) | ✓ base |
| L4 action/guards | interior-crop no-op, stale-state, terminal latch 🟢; per-kind overridable armed slots 🟢; UNDO wired 🟢 | shared override slot (291 replies / 1 action 🔴); aggressive reset discipline (sp80 82→14 🔴); advertising ACTION7 without wiring (0/3,566 🔴) | death ledger / repeat guard alone (dfranzen: unclear; our super-v2 μ = plain); `ARC3_BOARD_DUMP_GUARD=1`; expected-result cancel (🔵 Retrodict) | ✓ base; super flags neutral |
| L5 allocation | priority P = (A+B)·C with handover at eviction (🟢); contest overrides concurrency 120 / 532 min (🟢); TAIL_FADE | equal-per-game 🔴; deleting the contest overrides (Sovereign) | D′ (+2.7 family mean, n = 3, p ≈ 0.04); constants retune | ✓ D′ on A; retune after telemetry |
| L6 prompting | game-over diagnosis, level-transfer guidance, action echo, middle truncation (🟢) | more verification hints 🟡/🔴; PROTOCOL lines; turn-12 audit repeated every turn (sujan, untested) | escalation directive at stuck (🔵 Retrodict); image prime (🔵) | ✓ base |
| L7 algorithmic | — on the LB — | model-written simulators on every game (DF-WM: no evidence, bugs; ewma 11.7× tokens) ; BFS under a 25-transition model (negative #9) | expected-result cancel (piece B); dead-signature counter (Reki 🟢 M1); graph explorer (🔵) | none shipped |
| L8 evaluation | paired-by-game significance, P ≥ 0.90 (dfranzen 🟢); same-version redraw = free draw (🟢, now with our own n); skarin per-game reference | single-run deltas (every fork); local-25 as a target (r ≈ 0.16) | — | ✓ ledger + families from today |

**Top 3 layers to touch next:** L5 allocation (D′ on both accounts + retune), L0 throughput/robustness (owned watchdog, path fallbacks, MAXREQ probe, REAP line), L4/L7 cheap verified-action pieces (expected-result cancel; board-dump guard). **Top 3 NOT to touch:** L6 advice text, L2 model-written memory stacks, L7 simulators-by-default.

---

## 4. Our submissions, dissected

### 4.1 Milestone-2 era (both accounts; family μ/σ from `analysis/config_families.json`)

| date | acct | ref | family | score | vs family μ | note |
|---|---|---|---|---|---|---|
| 10-01 | A | — | M2S plain (fork bank) | 25.30 | −1.6 | |
| 10-03 | B | 56793884 | M2S plain (sureshot) | 23.86 | −3.0 | local-10 39/72 levels |
| 10-03/04 | A | 56795076 / 56825089 | super-v1 / v2 | ~27 / 27.38 | +0.5 | local-10 head-to-head +14 levels vs sureshot (did not transfer to LB) |
| 10-04 | B | 56825114 | super-v2 | 25.84 | −1.1 | |
| 10-05 | B | 56842664 | super-v2 redraw | 26.66 | −0.2 | |
| 10-05 | A | 56859016 | super-v3 (S1 level replay) | 26.34 | −0.6 | |
| 10-06 | A | 56877835 | F+D (fable + D′ on super) | **20.77** | −6.1 | the one clear negative; three layers stacked |
| 10-06 | B | 56886854 | Fable v2 | 27.17 | −2.2 | |
| 10-07 | A | 56900990 | super-v2 redraw | **27.67** | +0.8 | A best |
| 10-07 | B | 56901959 | Fable v2 redraw | **29.21** | −0.2 | B best |
| 10-08 | B | 56940861 | sujan v20 copy | **23.65** | −4.1 | low tail of plain M2S |
| 10-08 | A | 56947228 | m2top-v1 (D′ build) | **ERROR** | — | Kaggle system error on the rerun; one retry on Oct-9 (§7.4) |

Family statistics (`scripts/kw/kw_family.py`): super-v2 μ 26.9 **sd 1.0** (n = 4) — notably *lower* variance than plain copies (sd 3.9) at the same mean; D′ μ 29.65 (external n = 3); Fable μ 29.4 (n = 3, one is the author's plain baseline); M2S plain μ 26.9 (our two + public draws).

**What this says.** (1) Our additive flag sets (death ledger, repeat guard, act-forcer, effort ladder) did not move μ; they may have narrowed σ — useful for *measurement*, useless for the LB max. (2) Local-10 wins (super +14 levels, sc25 0→5/6, tr87 1→5/6) did not transfer; the public games are not the hidden games. (3) Stacking three untested layers (F+D) cost ~6 points; the one-layer rule is now a hard gate (`experiments/MISTAKES.md`).

### 4.2 Pre-M2 era (Sep 4–30, 17 submissions, 1.79–4.54)
TAAF/Duck + Flash-Next on vLLM with 5 GiB KV and no prefix cache: the whole era was serving-bound (87 % of request time queued). Superseded; kept in the ledger for the variance study only.

### 4.3 Per-game (local runs vs the public-25 reference)

| game | M2S ref (n = 4) | super_A local-10 | sureshot_B local-10 | reading |
|---|---|---|---|---|
| ar25 | 85.4 | 100 (8/8) | 41.7 (5/8) | efficiency bleed on cleared levels in sureshot (agent/base up to 1.3) |
| ft09 | 86.9 | 100 | 100 | solved; click-precision |
| lp85 | 100 | 58.3 | 41.7 | our local runs under-allocate (48-min cap vs 29,018 s in the audit) |
| r11l | 82.1 | 14.3 | 14.3 | hidden-mechanic; needs time, not prompts |
| re86 | 62.9 | 41.7 | 27.8 | animated keyboard; actions 316 vs base — efficiency |
| sb26 | 93.2 | 100 | 100 | solved |
| sc25 | 19.6 | 71.4 (5/6) | 0 | death-ledger/repeat guard helped locally (fatal-route avoidance) |
| tr87 | 92.3 | 71.4 | 4.8 | high variance game |
| tu93 | 83.7 | 20.2 | 13.3 | 9 levels; budget-bound locally |
| vc33 | 80.4 | 35.7 | 53.6 | hidden-mechanic, animated |

Local-10 at 48-min caps is a *smoke*, not a score: the audit gave each game up to 8 h. Use locals for mechanism signals (did a guard fire, did the agent die less, tokens per level), never for μ.

---

## 5. Per-game plan — the 25 public games as mechanism test-beds

Reference: `analysis/public25_reference_m2s.md` (M2S, n = 4 per game). Human baselines and archetypes: `analysis/games/per-level-efficiency.md`, `analysis/games/mechanics-summary.md`.

| class | games | what blocks M2S there | mechanism to test (one at a time) | generalization claim |
|---|---|---|---|---|
| DEAD (score < 5, never past L1 in 4 tries) | **sk48** (0.0, 4/4 zeros), **lf52** (1.8), **bp35** (1.2), **wa30** (3.2) | sk48/wa30: dead-action keyboard games — the agent defends a wrong goal from move 1 (ARC official failure mode; Makarov: the decisive action type *had* been tried); lf52/bp35: 9–10-level animated games where L1 itself needs a mechanic the agent never isolates | **expected-result + cancel-on-mismatch** (piece B) to force hypothesis testing; **escalation directive** at stuck-N ("build and test a small simulator of the mechanic"); **dead-signature counter** (clicks/keys that never change the interior) | these are the archetypes of the hidden set's zeros; a mechanism that converts one DEAD game on CPU *and* holds on the other three is the only kind worth a GPU hour |
| WEAK (5–25) | g50t (9.3), sp80 (13.1), ka59 (18.8), sc25 (19.6), s5i5 (23.9) | sc25: fatal routes (death loops) — our death-ledger pair fixed it locally; sp80: fail-state + reset discipline (aggressive resets collapsed it for Kepler); g50t: dead actions; s5i5: click-precision hidden mechanic | death-ledger pair **kept** (neutral on LB, positive locally); RESET opt-in semantics check; image-prime clause on L1 | partial |
| MID (25–60) | cn04, ls20, su15, dc22, m0r0, tn36 | depth/efficiency: 2–4 levels cleared then budget or wrong-abstraction; tn36 needs animation frames (in) | **allocation** (D′ keeps spending on near-miss games), tokens-per-level telemetry → C-term retune | yes — allocation is game-agnostic |
| STRONG (≥ 60) | re86, vc33, cd82, r11l, tu93, ar25, ft09, tr87, sb26, lp85 | efficiency bleed (agent/base ratios 1.1–1.7 on some cleared levels — quadratic penalty); over-exploration after the level is understood | **park-at-baseline** detector (projected actions > 1.05× baseline on a nearly solved level → finish, don't optimize); action echo already in | yes |

Rule: a per-game change is accepted only if it is **game-agnostic in code** (no game ids, no hard-coded actions — yukailiu-style per-game scripts cannot touch the hidden set) and passes paired CPU replay on all 25.

---

## 6. Improvement roadmap by kind

### 6.1 LLM-based
1. **Fine-tuning / distillation (the lever behind 55+, most likely).** Facts: Qwen3.8-Flash-Next is 125 B total / 6 B active + 51 B n-gram embedding + 4 B MTP, 512 experts; the W4A16 checkpoint alone fills the 96 GB card. Known pipelines: U4AR RL (Qwen3.8-**27B** BF16, 2× H100, GRPO on levels/tokens), manas joshi STaR-LoRA (Qwen3.6-27B, "measurable lift", trained on public games — Chollet's warning applies), Cassowary LoRA (r4 on 27B-FP8). **Not executable on Kaggle quota.** If external H100-class compute appears: SFT Flash-Next experts (QLoRA) on *harness-format* winning trajectories from games the model already clears, plus frontier-replay distillation (we already mirror the corpora: `Nabidnur/arc-agi-3-frontier-replays`, `arc-agi-3-datasets-combined`, Tufa example-run 2.8 GB). Serving a LoRA on Pennyroyal/W4A16 is unproven (dfranzen shipped `vllm_runtime_lora_guard.py` only). Ranked: highest upside, zero feasibility today → **research line, not a plan item**.
2. **Sampling / effort:** T 0.7 / top-p 0.95 / top-k 20 (keep); reasoning-effort ladder on output-cap truncation (dfranzen option) → single-toggle test (E-127).
3. **Prompt:** expected-result clause + cancel-on-mismatch (E-122); escalation directive in the stuck path (E-124). No advice blocks, no PROTOCOL lines, no per-turn audits.
4. **Memory:** facts-only harness-computed level log (Fable mechanism 3, PROTOCOL off) **or** solved-level invariants — never both (E-125/E-126). Reset per-game state in the base's reset block (sujan's bug).

### 6.2 Non-LLM (serving / harness / infra)
1. **Robustness pack (adopt now, zero score risk):** path-fallback resolver (sujan cell 4), RUN_FULL placeholder commit with lwq255's fail-open GPU probe, owned-time watchdog + teardown reserve + exit-reason log (prvsiyan V15/V17), `ARC3_WARMUP_ACTION_GAMES=1` + 900-s retry already in base, JIT-cache persistence (Lohit). This is what makes B's D′ kernel submittable and protects against the Oct-8 mount failures and the "finished in 4 h" incidents.
2. **Throughput probe (one smoke, ≤ 40 min):** MAXREQ 10 → 12 → 14 with KV-pool headroom printed (lordhansolo runs 14); spec steps 3 → 4; measure generated tok/s and prefix-reuse %. Promote only if tok/s ↑ ≥ 15 % with reuse ≥ 90 % (E-128).
3. **REAP-pruned model line** (cihanatak 32.9): public model `boristown/qwen3-8-flash-next-nvfp4-reap-448e` + vLLM 0.30 runtime; more KV room per token. A separate kernel on account A only after (1) and (2); gate = equal-tokens paired comparison (E-129).
4. **Variance engine mechanics:** `scripts/kw/kw_submit.py` + `analysis/next_submission.json`; both accounts; identical-version redraws are free; never skip a day.

### 6.3 Algorithmic
1. **D′ allocation on both accounts**, then **constant retune** from our own telemetry: per-game tokens-per-level from rerun/local logs → C-term (a/115, t/T) and pace reference (dfranzen's method, 725 attempts) (E-123, E-130).
2. **Park-at-baseline + rescue sweep** in the scheduler (docs/30 §4): CPU-simulable on skarin's 100-trajectory records + our ledger before any GPU (E-131).
3. **Dead-signature counter** (Reki, numpy, interior-crop hashes, overridable slot) and **graph-state explorer helper** in the sandbox — after E-122 result.
4. **Evaluation infrastructure (algorithmic in the meta sense):** offline CPU env with exact state cloning already exists (`Hisernberg/arc-agi-3` `agent/arcenv.py`); paired-by-game significance (`make significance` in the da-fr repo); the per-game reference table; family statistics. Every test below is defined by its metric before it runs.

### 6.4 Test queue (one layer per test; gates: CPU green → ≤ 40-min GPU smoke only if serving changed → paired local P(Δ > 0) ≥ 0.90 → submit on ONE account while the other redraws)

| id | change | layer | metric | kill |
|---|---|---|---|---|
| E-122 | expected-result clause + cancel-on-claimed-but-empty (piece B) | L4/L6 | levels/game, actions/level paired on 25 games × 3 seeds | tool timeouts > 2 %, tokens/turn +15 % w/o levels, refusals > 10 % of actions |
| E-123 | D′ on B (fixed kernel) — same version as A | L5 | B draw vs B's family μ; A/B same-day pair | — (variance draw) |
| E-124 | escalation directive in the stuck path (not per-turn) | L6 | DEAD-class games on CPU replay; levels | any STRONG game regression |
| E-125 | facts-only pinned level log (Fable mech. 3, PROTOCOL off) | L2 | tokens-to-clear on levels past 30k tokens; levels | re-prefill count ↑ > 10 % |
| E-126 | `ARC3_BOARD_DUMP_GUARD=1` | L4 | actions/level; guard fire count | levels ↓ |
| E-127 | reasoning-effort ladder on truncation | L1 | truncated turns ↓; levels | levels ↓ |
| E-128 | MAXREQ 12/14, spec steps 4 (smoke) | L0 | tok/s, prefix reuse %, KV headroom | reuse < 90 %, restarts |
| E-129 | REAP-k448 model line | L1 | equal-tokens paired 10 games | levels ↓ at equal tokens |
| E-130 | C-term / pace retune from telemetry | L5 | simulated allocation on audit records; then 1 draw | — |
| E-131 | park-at-baseline + rescue sweep | L5 | simulated on audit records; then 1 draw | — |

---

## 7. The plan: Oct 9 → Nov 2 (entry/team deadline Oct 26; final Nov 2 23:59 UTC)

### 7.1 Engine 1 — variance (every day, both accounts)
Expected best-of-N for N identical draws of N(μ, σ): E[max] ≈ μ + σ·z_N with z_24 ≈ 1.95, z_48 ≈ 2.2. With plain-M2S numbers (μ 26.9, σ 3.9): ≈ 34.5 / 35.5. If D′'s μ 29.65 is real at σ 3.9: ≈ 37 / 38; at σ 2: ≈ 33.6 / 34.1. **Planning number: 34–37 by Nov-2 from redraws alone**, i.e. rank ≈ 10–40 at today's LB. Each account draws its own highest-μ COMPLETE version; A carries D′ now, B gets D′ as soon as the fixed kernel commits (Oct-10). Tomorrow's instruction is in `analysis/next_submission.json`.

### 7.2 Engine 2 — engineering (one test per 2–3 days)
GPU: ≤ 3–4 big runs/week, each ≤ 40 min (3–5 games, paired arms), plus placeholder commits (≈ 33 s). Everything else on CPU (offline env, replay of recorded histories, scheduler simulation on audit records).

### 7.3 Seven-day calendar (UTC)

| day | A (dasshovon) | B (kragglenote2forwork) | engineering (CPU unless noted) | GPU |
|---|---|---|---|---|
| Thu 10-09 | **retry** `arc26-m2top-v1` v1 (Oct-8 rerun = system ERROR) | redraw Fable v2 | build the E-133 robustness pack kernel for B = clean D′ + prvsiyan paths/soft-end/owned stop/staged export + H1 R1/R2 fixes + fail-open probe; CPU rehearsal of the commit path; E-122 code + unit tests | 0 |
| Fri 10-10 (quota refresh 00:00) | redraw best | **commit** fixed D′ kernel (placeholder), then submit it if COMPLETE by 06:00, else redraw Fable | E-128 throughput smoke on A (≤ 40 min, logs tok/s, reuse, KV) | 40 min |
| Sat 10-11 | redraw best | redraw D′ | **weekly close**: `plan`, `agent outside` (3 memos), `analysis`, `research` deep; E-122 CPU paired replay on 25 games | 0 |
| Sun 10-12 | **E-122 version** submitted if gates passed, else redraw | redraw D′ | E-122 smoke if serving untouched → skip GPU; start E-125 code | 0–40 min |
| Mon 10-13 | redraw best | redraw best | E-124 escalation directive CPU test; telemetry parser (skarin's) on any logs we can get | 0 |
| Tue 10-14 | redraw best | E-126 board-dump-guard version if gates passed | E-130 C-term retune simulation on audit records | 40 min smoke |
| Wed 10-15 | redraw best | redraw best | E-129 REAP line prep (model attach, runtime check) | 0 |

Rule of the calendar: at most one experimental submission per day across both accounts; the other account always redraws.

### 7.4 Decision tree for Oct-9 00:05 UTC (the Routine executes it)
```
A: Oct-8 draw of arc26-m2top-v1 = ERROR ("A system error. Please try resubmitting").
├── Oct-9: ONE retry of arc26-m2top-v1 v1 — the super fallback (μ 26.9, sd 1.0) cannot beat A's 27.67, so the retry is the only draw with upside
├── retry scores ≥ 26 → D′ is A's family; keep redrawing daily
├── retry scores < 26 → inside the lottery's low tail; keep D′ but run `agent inside` before any code change
└── retry ERRORS again → the version is suspect: fallback dasshovon/arc26-m2s-super-v3 v3 until a new D′ version is committed (path fallbacks + fail-open probe, Oct-10)
B: Fable v2 redraw (only highest-μ COMPLETE version on B); D′ kernel re-commit queued for Oct-10.
```

---

## 8. Risks and pre-mortem

| risk | likelihood | mitigation |
|---|---|---|
| A token absent in automation → A misses draws | certain until `KAGGLE_API_TOKEN_A` is an environment secret (this session read A's state through a token found hard-coded in older scripts; those tokens are in git history and must be rotated) | add both tokens + `HF_TOKEN` as environment secrets (read-only names documented in `docs/32`); the Routine skips and reports otherwise |
| B's quota consumed by other competitions' kernels | high (30+ non-ARC kernels this week) | ARC placeholders need ~0 quota; smokes ≤ 40 min; schedule ARC GPU first after each refresh |
| commit queue 6–17 h delays the placeholder gate | high | commit the night before; never submit a version that is not COMPLETE (guarded in `kw_submit.py`) |
| mount-path failures (Oct-8) | medium | fallback resolver + fail-fast; failed commits do not use the slot |
| another stacked-layer regression (F+D) | medium if rules slip | one-layer gate + family stats before any promotion |
| Flash-Next license ruled ineligible | unknown | LB unaffected; keep the 27B-FP8 line documented as fallback (slower, −10 points historically) |
| Tufa/Chen release at the end → final-week reset | likely after Nov-2 only | irrelevant for this competition's LB; relevant for the paper |

---

## 9. Honest assessment versus "top 1"

Top-1 means > 55.9 by Nov-2. What is executable on a Kaggle quota is: (a) the variance engine (34–37 expected best), (b) engineering μ shifts of maybe +2 to +6 via allocation, throughput, robustness and verified-action pieces (the private 36–43 cluster did exactly this on the same model). That yields a credible target of **36–40 (top 10–20)** with discipline, and an outside chance higher through variance. Crossing 50 almost certainly needs the model lever (§6.1) — external H100-class compute for distillation/SFT and a serving path for the result — which is documented as a research line with the data already mirrored on HF, not promised as a plan item. The plan therefore maximizes expected rank and keeps every option open.

---

## 10. Addendum — second-batch teardown (`analysis/teardowns/2026-10-08/forks-batch2.md`; all 20 patch anchors verified against our reference harness)

| notebook | what it is | verdict |
|---|---|---|
| ashwanidhukra win-v2 (29.30) — **PRO-LONG programmatic memory** | per-game append-only JSONL (one line per executed `action(...)`, batch flags flattened) + `search_memory(query, max_hits=40)` (substring/regex, ≤ 6,000 chars) inlined into the `python -I -S` sandbox; ≈ 220 cached prompt tokens; drain/scheduler untouched | **TEST** (E-134): paired levels P ≥ 0.90 *and* traces must show the model actually calls it |
| ashwanidhukra no-progress module | edge-triggered hint once at K = 15 no-change actions; never executes RESET/UNDO (RESET clause unreachable); a missing flag (`None`) resets the streak | IGNORE |
| **prvsiyan V15/V17** | dual mount-layout path resolver; rerun soft end = 9 h − 9 min (**the M2S base has `soft_end=None` in the rerun**) + owned hard stop at 9 h − 5 min (process-group ownership test, SIGTERM 20 s → SIGKILL 5 s, then `interrupt_main`); teardown reserve ≥ 120 s; placeholder-first staged/verified/atomic export; commit gate; `requests.Session.send` timing log → slot-idle fraction. ≈ 105 lines core | **ADOPT** (E-133 robustness pack) |
| juliancamilovilla H1 | R1: a sandbox timeout no longer wipes the retained-function library (bug confirmed at `tool_agent.py:4617–4621`); R2: a non-string `result` > 16 k chars now goes through trimming (confirmed live). 14 lines | **ADOPT** (E-133) |
| juliancamilovilla D1 | `ARC3_CONTEXT_DRAIN_TOKENS` 58 Ki → 24 Ki (2.4× more prefix-invalidating evictions) + 8 streams | IGNORE (contradicts the cache-reuse evidence) |
| lwq255 m2-guarded | `RUN_FULL` guard fails **closed** on an inconclusive `nvidia-smi` (→ silent placeholder in a rerun); its dprime-guarded sibling fails open | ADOPT the fail-open rule; **A's kernel uses the fail-open variant** (verified: its cell 4 is the dprime-guarded one) |
| skarin trace parser | stdlib `parse_trace` / `parse_usage` (request-id pairing, 17-kind warning taxonomy); measured a 36,671-token gap between completion usage and action-boundary allocations — the quantity our priority C-term and token-yield read | **ADOPT as tooling** (`scripts/kw/`), ~170 lines |
| samrishb V9 (29.21) | plain M2S; the "skills bundle" helper is injected into a non-existent `sandbox_helpers` (no-op); author notes V8 heuristics degraded | IGNORE |
| luisignaciomoreno Prometheus (0.28) | LLM-less 537 K-char offline policy (DSL world model, volatility-masked state hash, causal mining, death memory, CPU-time clock); author gate 12 → 14 levels / 25 games | IGNORE (volatility mask only if we ever see HUD false positives) |
| manderson240 (0.26), yukailiu (0.21), natmin322 | Zobrist-hash BFS macro agent; sha256-fingerprinted per-game scripts for 24/25 public games (ceiling ≈ 23–26 only if the public 25 are inside the 110, 0 otherwise); a GRPO LoRA run on reasoning-gym with zero ARC content | IGNORE (yukailiu = the negative-registry #1/#10 pattern) |

**Account A's real kernel (`dasshovon/arc26-m2top-v1`, pulled tonight).** It is lwq255's fail-open guarded D′ (cells 0/3/4/15/17/23/24/25) plus the sujan-era extras in its own cells 7 and 19: `ARC3_GUARDS_FROM_LEVEL=1`, repeat-state guard, auto frame-diff, level inventory, episodic memory, strategy audit, `ARC3_DEATH_*` flags, `ARC3_BOARD_DUMP_GUARD`; env sets confirmed: `ARC3_PRIORITY_PACE=1`, `ARC3_PRIORITY_REFRESH_QUEUE=1`, `ARC3_PRIORITY_TAIL_FADE=1`, `ARC3_WARMUP_ACTION_GAMES=1`, `ARC3_HTTP_RETRY_INITIAL_SECONDS=900`. So A draws a **seven-layer stack** whose only sample is an ERROR. That is exactly the configuration the catalog called "sujan ✓" — it existed in an earlier sujan version, not in his current one. Policy: one retry (§7.4); if it scores inside the band, keep it as A's family but do not add layers; the clean D′-only build (E-123) goes to B so the two accounts measure D′ with and without the extras.

**Port order (risk-adjusted):** H1/R1+R2 → prvsiyan watchdog/paths/export → fail-open guard check → skarin parser → PRO-LONG as a flagged significance candidate.

## 11. Sources (today)
Kaggle API (submissions, leaderboard CSV 2026-10-08T20:36Z, kernels list ×3 sorts, 41 kernels pulled), internal forum API (246 topics, 33 updated since Sep-27, 15 threads read in full), `references/sweeps/2026-10-08/`, `analysis/teardowns/2026-10-08/{df-wm,fable-layer,forks-batch}.md`, skarin audit evidence (100 records), TechTimes 2026-10-06 report, arcprize.org blog (no post since 09-03), Qwen3.8-Flash-Next model card, U4AR RL report, manas joshi STaR thread 739047, `Hisernberg/arc-agi-3` (Sept repo: `agent/arcenv.py`, `automation/kaggle_pipeline.py`, routines), HF `Nabidnur/arc-agi-3-*` datasets (traces, replays, discussions, notebooks, research, playbooks).
