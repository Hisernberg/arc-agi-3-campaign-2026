# 09 — ARC-AGI-3 Engineering Techniques Catalog (competition-wide sweep)

**Date:** 2026-10-07/08 · **Scope:** every public source we could reach — all 25 unpinned LB notebooks (20–34.3), the Gold solution repo (github.com/da-fr/arc-agi-3-solution), Tufa Labs Duck harness + writeup, ARC Prize official milestone-1 analysis + official docs, 14 arXiv papers (Tycho, Kepler, RGB, ewma/twma, OPINE-World, PRO-LONG, MAP, Graph-Based Exploration), API-league agent blogs (Retrodict, Symbolica/Agentica, INT21), Kaggle discussions.

**Evidence classes:** 🟢 proven on ARC-AGI-3 LB · 🔵 proven in adjacent benchmark (API league / ARC-AGI-1-2 / RL games) · 🟡 neutral / no measurable effect · 🔴 documented as harmful.

---

## 1. Executive summary — what actually wins

1. **Model choice is the biggest single lever.** dfranzen: each model switch (Qwen3.6-27B → 3.8-27B → 3.8-Flash-Next) was "a substantial improvement". API league confirms (GPT-5.6 Sol + max effort = 99.86%). No harness trick replaces this.
2. **Variance is the second-biggest lever.** Same immutable version scored twice = **6.79 points apart** (skarin audit). Plain M2S copies spread **20.0–27.63 (μ≈25.8)**. A μ≈31.5 config redrawn daily is the cheapest path to 31+.
3. **Compute reallocation is the third lever.** The D′/dfranzen priority schedulers (P=(A+B)·C / A·M·C+B·φ) convert wasted compute on dead games into completions on near-miss games. D′ family draws: 29.16 / 31.54 / **31.93** vs plain-copy μ≈25.8.
4. **Perception wins are real and cheap:** 10× image upscale ("biggest image improvement"), animation-frame exposure ("strongest of all perception changes" — tn36 unsolvable without it), object-level frame_diff.
5. **The prompting cluster that jumped the competition set:** UNDO exposure + action info + level-transfer guidance + game-over diagnosis + persistent functions.
6. **Most elaborate machinery HURTS or does nothing:** structured world-model sections, summarization, generator+arbiter voting, composite animation images, extra verification hints — all neutral-to-negative in the Gold solution's own ablations.
7. **Prefix-cache engineering ≈ free score** on a fixed GPU budget: 93.43% prompt-token reuse = 3–5× more effective actions per hour than naive trimming.
8. **Keep model thinking in history** — removing it is a "large regression".
9. **Guards: interior-board no-op + stale-state + terminal latch are proven; memory-based guards (no-op/death ledgers) are only safe with per-kind overridable armed slots** (else: 291 model replies, 1 executed action).
10. **Honest evaluation discipline** (paired-by-game significance, P≥0.90) exists because single-run deltas are noise.

---

## 2. The two named techniques — definitions and verdicts

### 2.1 "Greedy anchored voting"

**What the user hoped it was:** vote on the single next action across k parallel rollouts anchored at the current state; greedily take the argmax (majority) action, re-anchor, repeat.

**What actually exists in the competition:**

| Relative | Technique | Mechanism | Evidence |
|---|---|---|---|
| 🟢 | **First-divergence cancellation** (Retrodict / RGB plan executor / Kepler `commit.py`) | model emits a k-action plan, each action annotated with its **expected result**; after each executed action, predicted vs observed frame is compared; on first mismatch the rest of the batch is cancelled and the counterexample logged | Retrodict: 99.86% RHAE at 5.5× fewer tokens; "a missed prediction cancels the rest of the batch" |
| 🔴 | **Generator + arbiter candidate voting** (forge, Milestone-1 3rd) | generate multiple candidate actions, score with arbiter, pick best | "the top-scoring run used a profile that turns **off** all of the extra machinery" |
| 🔴 | **Consensus voting over k full samples** (static ARC-AGI-1 solver trick) | majority vote on final grids | never shown to transfer to interactive ARC-AGI-3; rollouts diverge on hidden state so votes are decorrelated noise |

**Verdict:** naive "greedy anchored voting" is a documented trap (forge's arbiter; static-ARC voting). The **proven neighbor** is *expected-result annotation + cancel-on-mismatch* — it is plan-time anchoring with self-verification, not voting. Adopt that.

**Concrete adoption (prompt+guard, ~30 lines):** system-prompt addendum: "For each batched action state the expected board change in one line. Batches whose first action's expectation is falsified will be truncated." Guard-side: if the existing interior-board no-op/diff check shows the outcome contradicts the model's stated expectation, cancel remaining batch actions (we already have the batch-cancel machinery in the M2S harness — this only changes *when* it fires).

### 2.2 "Categories alignment" (game-class → per-class strategy)

**What exists:**

| Relative | Technique | Evidence |
|---|---|---|
| 🔴 | **Mapping a game to a known family (Tetris/Frogger/Sokoban/…) and importing that strategy** | ARC Prize's own 160-replay analysis: "**Wrong Level of Abstraction From Training Data**" — literal analogies hijack action selection; a documented top failure mode |
| 🟢 | **Per-object-type strategy switch** (Reki's dead-signature + click heuristic) | object types whose clicks never changed anything are skipped for the rest of the level; exploratory clicks prioritized on small/rare/button-like shapes — pure numpy |
| 🟢 | **Per-stuck-state strategy switch** (Retrodict escalation ladder) | after 300 actions or 2 self-resets on one level, inject directive to build & test an executable simulator → solved 3 of 4 remaining unsolved games |
| 🟢 | **Per-game harness decision** (Tycho orchestrator) | per game, decide build/repair/use/bypass world-model — 79.07 → 88.49 RHAE |
| 🔵 | **Object-type adequacy (ontology-error) steering** (OPINE-World) | Bayesian per-object-type "how badly do I understand this" score steers probing → 1.5% → 78.40% RHAE |

**Verdict:** coarse category alignment into game families is **documented harmful**. Fine-grained alignment — per *object type*, per *stuck-state tier*, per *game progress* — is where the proven wins live. In our stack this already exists partially (sujan's level-inventory + 4-tier watchdog = the stuck-state ladder); the missing piece is **dead-signature** (§6, ranked #4).

---

## 3. Layer-by-layer catalog (L0 → L8)

Legend: ✓ = in our submitted kernel (`arc26-m2top-v1`); ○ = available in the M2S codebase, off; ✗ = not present.

### L0 — Serving / infrastructure

| Technique | Mechanism | Verdict | In ours |
|---|---|---|---|
| Pennyroyal SGLang fork v2.5.3 + 5 patches (low-M BF16 GEMM, spec-state memory budget, Marlin scale fix, Mamba prefix-cache checkpointing, prefetch lookahead) | serving throughput + cache correctness | 🟢 Gold-solution base | ✗ (sujan serves via own stack) |
| Weight resharding into small shards | startup reliability (one huge shard breaks prefetch alignment) | 🟢 | ✗ |
| **JIT-kernel cache persistence** (M87) | tar Triton/TileLang compile caches into working dir, re-attach as dataset → W4A16 boot JIT 142.6 s → 6.0 s per cold start | 🟢 (Lohit duck-18) | ✗ |
| **Weight mixing** (M82): W4A16 experts + FP8 PLE tables symlinked into one model dir | host-RAM + VRAM headroom without quality loss | 🟢 (Lohit) | ✗ |
| vLLM path: KV cache 10 GiB explicit bytes, MTP=1, cudagraph 32, max_num_seqs 8 | alternative to SGLang; KV pool sized blind (profiling skipped) — measure before raising | 🟢 (Lohit) | — |
| KV-cache dtype FP8 E4M3, mamba cache 60 slots, static mem frac 0.96 | more KV tokens per GiB | 🟢 | ○ |
| CUDA-lib repair (libcudart symlink repair, borrowed toolkit) | boot robustness on Kaggle image | 🟢 (Lohit) | ✗ |
| **Server-alive watchdog + `ARC3_WARMUP_ACTION_GAMES=1`** | harness starts even if backend not ready; first game auto-RESETs so Kaggle doesn't kill an idle run | 🟢 | ○ |
| `ARC3_HTTP_RETRY_INITIAL_SECONDS=900` | survive long serving boot without burning retry budget | 🟢 (Sovereign) | ○ |
| Server-context 136 Ki > harness 128 Ki window | headroom so prefill never overflows | 🟢 | ✓ |

### L1 — Model

| Technique | Mechanism | Verdict | In ours |
|---|---|---|---|
| Bigger/better open model (Qwen3.8-Flash-Next) | raw capability | 🟢 "each switch substantial" | ✓ |
| NVFP4 / Intel W4A16 AutoRound quant; **BF16 PLE unquantized, offloaded to host RAM** | throughput + KV headroom without quality loss | 🟢 | ✓ (via datasets) |
| **Speculative decoding, MTP draft, steps=3** | decode throughput | 🟢 | ✓ |
| FRspec / autotune flags | spec-decode tuning | 🟢 (hknight/Lohit) | ○ |
| Reasoning-effort ladder (step down on output-cap truncation) | fewer wasted turns | 🔵 (dfranzen option) | ○ |

### L2 — Context / memory

| Technique | Mechanism | Verdict | In ours |
|---|---|---|---|
| 128 Ki window, **blockwise drain to ~57 Ki (hysteresis)** | rare large evictions; front-removal invalidates whole prefix so frequency must be minimized | 🟢 93.43% cache reuse | ✓ |
| **Calibrated token accounting** (chars/token clamp [1.0, 3.3] vs backend reports; images from PNG dims, 32-px patches + 2 markers) | trim decisions match reality; enables 10× images | 🟢 | ✓ |
| **Keep model thinking in history** | evidence retention | 🟢 removal = "large regression" | ✓ |
| Assistant-turn cap + turn-drain + coalesce | second binding limit besides tokens | 🟢 | ✓ (150/30) |
| **Retained Python functions** (AST + dis-validated: no decorators, literal defaults, no STORE_GLOBAL; scope=game) | model rebuilds helpers once | 🟢 | ✓ |
| **No-op repeat guard** (per-level LRU of (interior_state_hash, action_signature), 512 states × 16 actions; **overridable armed slots, per guard kind**; deaths don't clear) | stop re-trying provably dead actions | 🟢 in sujan draw 31.93 (dfranzen left it off — unclear benefit alone) | ✓ |
| **Death ledger / death repeat guard** (per-attempt action list + index-aligned pre-action hashes; lookahead variant) | "this action from this exact board killed us" is a lookup | 🟢 in sujan draw | ✓ |
| Repeat-state guard + auto frame-diff (budget 300) + level inventory | sujan extras | 🟢 | ✓ |
| **Episodic memory across levels** (cleared-level rules carried into later-level prompts) | level-transfer learning | 🟢 (sujan) | ✓ |
| Programmatic memory: searchable interaction log queried by code, **instead of summarizing** (PRO-LONG) | +18.0 pts avg in coding agents; 76.1% pass@1 at 4–6× fewer tokens | 🔵 | ✗ |
| Structured world-model sections (World/Goal/Action model parsing) | — | 🔴 **"largest improvement came from disabling"** | ✓ off |
| Summarization (append or replace) | — | 🟡 "neither gave a clear improvement" | ○ off |
| Textual world model (durable rules, no simulator) | twma 95.97% RHAE at ⅓ tokens of executable | 🔵 | partial (episodic rules) |
| Executable world model + exact replay verification | ewma ~99% but 11.7× tokens; pixel-perfect = 307 LOC rendering vs 85 mechanics | 🔵 (works, expensive) | ✗ |
| Playbook file across resets, framed as "working model" not "confirmed" | Retrodict: 4+ games fell after reframing (avoid hypothesis lock-in) | 🔵 | ✗ |

### L3 — Perception

| Technique | Mechanism | Verdict | In ours |
|---|---|---|---|
| **10× nearest-neighbor upscale** | bigger, readable boards | 🟢 "biggest image improvement" | ✓ |
| **Animation-frame exposure** (`last_animation_frames` + compressed timeline; capture per-internal-step, dedup with pre-action board prepended, **transient-pixel detection** = cells changing ≥2×) | an action's effect can live only in intermediate frames | 🟢 **"strongest of all perception changes"; tn36 unsolvable without** | ✓ |
| Object segmentation (4-connected components, rotation-aware shape/pose hashes), raw grid hidden | compact object identity | 🟢 | ✓ |
| `frame_diff()` with Jonker-Volgenant minimum-cost object matching | moved/rotated/appeared/disappeared/recolored/resized | 🟢 | ✓ |
| Diff images (changed cells true palette, unchanged dimmed navy) + death-frame diff | model sees what changed / why death | 🟢 | ✓ |
| Composite animation images + auto-inserted timelines | — | 🔴 "hurt some games" (keep frames on-demand) | ✓ on-demand only |
| Image prime (first frame → describe + hypothesize) | unlocks stuck first levels | 🔵 (Retrodict) | ✗ |

### L4 — Action path & guards

| Technique | Mechanism | Verdict | In ours |
|---|---|---|---|
| **Batch no-op guard** (interior board, 4-cell HUD border excluded) | budget-bar pixels ≠ progress | 🟢 | ✓ |
| **Stale-state guard** (block later actions in snippet after an ineffective one; first returns) | don't chain off stale frames | 🟢 | ✓ |
| **Terminal latch** (no actions after death/complete within snippet) | — | 🟢 | ✓ |
| Guards from **level 1** (sujan) vs level 2 (dfranzen) | earlier protection | 🟢 (31.93 draw) | ✓ L1 |
| **Per-kind overridable armed slots** for memory guards | first refusal arms one slot; immediate reissue executes (no self-sealing foreclosure of hidden-state mechanics) | 🟢 critical detail — shared slot = 291 replies / 1 action | ✓ |
| **UNDO exposure (ACTION7 fully wired)** | "helped substantially… might be very important on the competition set" | 🟢 | ✓ on |
| **ACTION7 mapping bug fix** | raw duck fork advertises ACTION7 but `to_engine_action` returns None → 0 executions in 3,566 actions while advertised in 6 games (4 of which are perpetual-zero: g50t, sk48, sp80, tn36) | 🟢 bug fix | ✓ (dfranzen codebase routes UNDO→ACTION7) |
| RESET opt-in, first-action-only, own follow-up prompt (not framed as death) | recovery without exhausting the bar | 🟡 (off in all 31+ kernels) | ✓ off |
| **Expected-result annotation + cancel-on-mismatch** | plan self-verification | 🔵 proven API-league, unproven here | ✗ → v2 candidate |
| **Dead-signature** (per-object-type click-futility counter) | stop clicking inert sprites | 🟢 (Reki, Milestone-1 2nd) | ✗ → v2 candidate |
| Consecutive-RESET guard / 5×-baseline cutoff | stop grinding dead levels | 🟡 (Kepler added it; sp80 fell during "added discipline" — correlation unclear) | ✗ |
| Yield-by-tokens (2,048) not seconds | every serving change silently retunes a time yield | 🟢 | ✓ |

### L5 — Scheduling / compute allocation

| Technique | Mechanism | Verdict | In ours |
|---|---|---|---|
| **D′ priority** `A·M·C + B·φ` (Osaka): depth×efficiency × pace × stall-decay + upside; **removes fresh-first**; PACE off / REFRESH_QUEUE on / TAIL_FADE 0.2–0.4 | spend on near-miss games | 🟢 +3.4 to +6.2 over plain copies | ✓ |
| **dfranzen priority** `P=(A+B)·C`: A = ℓ·(25/(25+a))²·55/(N(N+1)/2); C = 0.25·2^-(a/115)² + 0.75·2^-(t/62000)² (calibrated on 725 attempts); B = {≥3:8, 2:7, 1:5, 0:0} | same goal, different math | 🟢 34.3 author | ✓ (D′ replaces) |
| **Cache-aware priority bands** (+1M warm / +2M untrimmed), admission ≤ 10 = server slots, **slot handover only at context eviction** | never evict a hot prefix for a marginal priority gain | 🟢 93.43% reuse | ✓ |
| **REFRESH_QUEUE** (recompute all waiting priorities against one shared clock before every admission) | no stale priorities | 🟢 | ✓ |
| **TAIL_FADE** final 20% runtime: B·min(1, r/(0.2T)) | near deadline, finish current level > future potential | 🟢 | ✓ |
| Pace adjustment (KM per-level token costs, EMA 0.6/0.4, clip [0.5, 2.0]) | adapt scale to game cost | 🟡 ablated out (not clearly better than constant tail) | ✓ off (PACE=0) |
| Empirical continuation lookup TAIL_LOOKUP_80K (KM from 336 passes) | better B | 🟡 ablated out | ✓ off (`remaining` used) |
| **Equal-per-game allocation** | the thing the schedulers replace | 🔴 "wastes tokens on stalled games" | ✗ |
| Local-run parity math: per-game cap = budget×lanes/games (Lohit: 7,920 s ⇒ 899 GPU-s/game at 110 games) — **don't "use the whole session" locally** | inflated local scores mislead | 🟢 | ✓ |
| Per-game budget caps: dfranzen contest = 532 min/game, concurrency 120 | full-trajectory runs | 🟢 | ✓ |

### L6 — Prompting loop

| Technique | Mechanism | Verdict | In ours |
|---|---|---|---|
| **Game-over diagnosis block** (flag semantics: game_over = attempt FAILED, auto-reset, levels kept; BAR RULE: shorter bar normal, death only when bar fully depleted in death frame; point at history[-2/-3]; forbid resubmitting the falsified deterministic series) | stops the "the game is over" confusion loop | 🟢 | ✓ |
| **Level-transfer guidance** (carry mechanics as hypotheses; expect new-mechanic elements; reassess goal) | part of the competition-set jump | 🟢 | ✓ |
| "No actions were executed" clarifications; reminder labeling | — | 🟢 | ✓ |
| Tool output 3,072 tokens with **middle truncation** (head+tail kept; guard messages at end) + action echo | — | 🟢 | ✓ |
| **4-tier tactical watchdog** (sujan: stuck 18 → tactical shift, 30 → hypothesis falsified, 45 → urgent RESET, 60 → compulsory RESET) | anti-tunnel-vision | 🟢 (31.93) | ✓ |
| **Escalation ladder** (Retrodict: 300 actions or 2 self-resets → "build & test an executable simulator" directive) | escape hatch from world-model failure | 🔵 3 of 4 unsolved games solved | ✗ → v2 candidate (extend watchdog tier) |
| Hypothesis-discipline addendum (our own) | anti lock-in | 🟢 (ours) | ✓ |
| Prefer-tool-calls hint (after an 18k-char reasoning turn executed nothing) | — | 🟢 (optional in dfranzen) | ○ |

### L7 — Verification / world-model / exploration (algorithmic layer)

| Technique | Mechanism | Verdict |
|---|---|---|
| **Builder-delegating orchestrator** (actor decides *when* to request model build/repair; auto-repair worse) | 79.07 → 88.49 RHAE | 🔵 (Tycho) |
| **Ontology-error-guided exploration** (Bayesian object-type adequacy steers probing) | 1.5% → 78.40% RHAE | 🔵 (OPINE-World) |
| **Graph-based state-space exploration** (visited-state graph; prune loops; prioritize actions on shortest path to untested (state, action) pairs) | preview #2 (6.71%) without any LLM | 🔵 |
| **Action-change learning** (small CNN predicts which actions change frames → exploration priority) | preview #1 (12.58%) | 🔵 (StochasticGoose) |
| **Map-then-act** (global exploration → cognitive map → knowledge-augmented execution) | 22/25 games above near-zero baseline | 🔵 (MAP) |
| Simplification/refactoring loop under green verifiers (MDL proxy) | beat executable-only in 3 of 4 settings | 🔵 (RGB) |
| Two API settings: retained reasoning + compaction (GPT-5.6 Sol 13.3→38.3) | pure API settings | 🔵 |
| Orchestration swarms sharing learnings (Sol 13.3→100, Luna 0→56) | heavy compute | 🔵 (INT21) |

### L8 — Evaluation / meta

| Technique | Mechanism | Verdict |
|---|---|---|
| **Paired-by-game significance testing**, P(true_delta>0) ≥ 0.90 + bootstrap 90% CI before promoting a candidate | dfranzen `make significance` | 🟢 |
| **Same-version repeat submits = free variance draws** (Kaggle reruns the immutable version on competition GPU; commit output only gates) | the quota-free redraw engine | 🟢 (skarin audit + our own ref 56900990: 27.38→27.67 same config) |
| **Quota-free submission kernel** (`RUN_FULL` = rerun ∧ ≥40 GiB gate; commit writes placeholder parquet in ~33 s on 2×T4) | score runs don't consume our GPU quota | 🟢 (sujan design, verified) |
| Paired-trial honest qualification (Digital Mouse: 24 trials / 6,144 actions / replay audit) | methodology positive even when score is 0.21 | 🟢 (process) |
| Official scorer mirror: `min(115, (baseline/actions)²·100)`, weight = level index+1, cap `max_weights/total·100` | every decision can be value-priced | 🟢 |

---

## 4. Formula vault

**Official per-level score:** `min(115, (baseline_actions / ai_actions)² · 100)` — quadratic efficiency penalty; game score = level-weighted mean (weights 1..N ⇒ later levels worth more); total = mean over 25 games. **A deep level (N=10, L10) ≈ +0.73 total points.** 27→31 = 4–6 extra deep levels or efficiency-equivalent.

**dfranzen priority:** `P = (A + B) · C`
- `A = ℓ · (25/(25+a))² · 55/(N(N+1)/2)` (N clipped 6–10)
- `C = 0.25·2^(-(a/115)²) + 0.75·2^(-(t/62000)²)` (Gaussian; fitted on 725 attempts / 557 completed — Gaussian beat exponential)
- `B = {≥3 remaining: 8, 2: 7, 1: 5, 0: 0}`; TAIL_FADE: `B_eff = B · min(1, r/(0.2T))`

**D′ priority (our kernel):** `priority = A·M·C + B·φ` — M = pace multiplier, φ = stall-decay; fresh-first removed; TAIL_FADE=1 @ 0.2.

**Context hysteresis:** trigger at budget → drain one block to ~57 Ki retained (128 Ki window, 12 Ki output reserve). Never trim in small increments.

**Lohit local-parity:** `per_game_cap ≈ total_budget × lanes / n_games` (7,920 s ⇒ 899 GPU-s/game at 110 games / 3.11 lanes).

---

## 5. Negative-results registry (do NOT adopt)

| # | Anti-technique | Evidence |
|---|---|---|
| 1 | Hand-crafted hard tools ("counterintuitively, they hurt") | Tufa milestone-1 blog |
| 2 | Generator+arbiter candidate voting; confidence prompts | forge's own top run disabled it |
| 3 | Structured world-model sections parsing | dfranzen: disabled = largest improvement in that area |
| 4 | Summarization (append or replace) | "neither gave a clear improvement" |
| 5 | Composite animation images; auto-inserted timelines | "hurt some games" |
| 6 | More prescriptive verification hints / more guard kinds beyond overridable pair | "without sufficiently clear benefit" |
| 7 | Pixel-perfect executable world models as default | 11.7× token cost, same score |
| 8 | Aggressive reset discipline | sp80 82.16 → 14.29 during "added-discipline" stage |
| 9 | Search under an incompletely-fitted world model | 4.1×10⁸ candidates wasted on 15/4,670 unexplained transitions (Kepler) |
| 10 | Category-into-family strategy import | ARC official: "Wrong Level of Abstraction" hijacks action selection |
| 11 | Removing model thinking from history | "large regression" |
| 12 | Time-based turn yielding | silently retuned by every serving change |
| 13 | Small/frequent context evictions | each front-removal invalidates the entire cached prefix |
| 14 | Sharing one override slot across guard kinds | 291 replies / 1 executed action (mouse-only game) |
| 15 | Whole-board change as progress signal | ticking HUD bar defeats it; use interior crop |
| 16 | Raising local-run budgets "to use the whole session" | 4.3× competition budget → every local score inflated |
| 17 | Tiny-model policies for this task (Digital Mouse 0.21, Smol 0.16) | honest, but orders of magnitude off |

---

## 6. Points-per-effort ranking for OUR stack (kernel `arc26-m2top-v1` base, μ≈31.5)

1. **Redraw the same kernel version daily** (zero cost, zero risk) — variance engine. μ≈30.9/σ≈1.5 over 3 known D′ draws ⇒ P(≥31 per draw) ≈ 0.55–0.6; two draws ⇒ ≈ 0.8.
2. **Verify UNDO path end-to-end in logs after first rerun** (it's wired, but confirm `UNDO executed > 0` in rerun logs; Lohit proved a silent 0/3,566 is possible). Cost: one grep.
3. **Extend watchdog tier-3/4 with Retrodict's escalation directive** ("build a small executable simulator of the mechanic and test it in the sandbox") — prompt-only, ~15 lines. 🔵-proven pattern, low regression risk.
4. **Dead-signature counter** (per object-type click-futility, interior-crop state key, overridable armed slot like existing guards) — ~60 lines numpy, no model change.
5. **Expected-result annotation + cancel-on-mismatch** — prompt clause + reuse batch-cancel machinery. 🔵-proven in API league; medium risk (may cancel too eagerly → gate on interior-diff only).
6. **Escalation-ladder arithmetic alignment**: watchdog tiers 18/30/45/60 vs official 5×baseline cutoff ≈ 115+ actions — our RESETs are far more eager than the official cap; safe because guards are overridable, but consider tier-4 = RESET to level start (not game) to preserve progress. (Only with paired evidence.)
7. **JIT-cache persistence + boot hardening** (M87-style) — matters only when GPU quota returns Oct-10; saves ~2–5 min per commit run (irrelevant for scored rerun but derisks the output gate).
8. **Image prime on L1** (one clause: first frame → "describe + hypothesize before acting") — cheap, 🔵.

Everything else in the catalog is either already in our kernel, proven-neutral, or negative.

---

## 7. Sources

- github.com/da-fr/arc-agi-3-solution (WRITEUP.md, CONFIGURATION.md, priority_scheduler.py, tool_agent.py, noop_repeat_guard.py) — Gold 34.3 author's own docs
- Tufa Labs Duck harness + writeup (discussion/717133, tufalabs.ai/research/duck-harness/) — Milestone-1 winner
- Kaggle LB notebooks pulled Oct-7/8: sujanmajhisuzan (31.93), shiiin9/affectify (31.54), skarin audit (31.66), fable-astra (31.73), amatlas D′ (29.16), Sovereign Agent (29.08), hknight3.0 (28.52), sirikilohit duck-18 (22.53, Milestone-2 3rd author), manwithacat Digital Mouse (0.21), dfranzen M2S (27.89 open-sourced)
- ARC Prize official: milestone-1 analysis blog, docs.arcprize.org (scoring, LLM agents, swarms), ARC-AGI-3 paper (2603.24621)
- Papers: RGB (2605.05138), Tycho (2607.28287), Kepler (2610.00834), OPINE-World (2607.01531), PRO-LONG (2607.20064), MAP (2605.13037), Graph-Based Exploration (2512.24156), baseline1 paper02 (2607.15439)
- Blogs: blog.ryanbbrown.com (Retrodict), symbolica/agentica day-1, INT21 SwarmOS, TechTimes milestone-2 report

---

## 9. Corrections (2026-10-08 research day — from cell-level teardowns in `analysis/teardowns/2026-10-08/`)

1. **sujan rows (L2/L4/L6):** the pulled `arc-agi-3-m2-top-submission` ("Version 20 Superstack", run 2026-10-08) contains **no D′ priority, no 18/30/45/60 watchdog tiers, guards stay from level 2, and none of repeat-state guard / auto frame-diff / level inventory / no-op repeat guard / death ledger** (those are base flags defaulting off and never set). It has a `_build_user_prompt` hook (solved-level "invariants" = last 250 chars of reasoning; death-loop warning; a single turn-12 "STRATEGY AUDIT" repeated every turn), `ARC3_BOARD_DUMP_GUARD=1`, a commit bypass and path fallbacks. The hook never resets per game (state leaks across games). The 31.93 is a single draw; our copy drew 23.65.
2. **L0 attribution:** `ARC3_WARMUP_ACTION_GAMES=1` and `ARC3_HTTP_RETRY_INITIAL_SECONDS=900` are dfranzen base lines, not Sovereign additions. Sovereign deleted the contest overrides (concurrency 120 / 532 min per game).
3. **L5 D′ row:** the D′ module (byte-identical in shiiin9 / amatlas / lwq255) sets `ARC3_PRIORITY_PACE=1`, `REFRESH_QUEUE=1`, `TAIL_FADE=1`, `TAIL_FADE_FRACTION=0.4` itself — "PACE off / fade 0.2" was wrong. Exact formula in docs/31 §2 and `analysis/teardowns/2026-10-08/_dprime_lwq255_decoded.py`.
4. **Fable layer:** no on/off evidence exists in any of the three notebooks; the author's 31.73 is a plain-M2S baseline draw. Mechanisms, thresholds and detector limits in `analysis/teardowns/2026-10-08/fable-layer.md`.
5. **DF-WM:** no score, no outputs, no ablation; shipped bugs listed in `analysis/teardowns/2026-10-08/df-wm.md`. Only the cancel-on-mismatch fragment is worth a test (catalog §2.1 verdict stands).
6. **§6 ranking item 1** ("μ ≈ 30.9/σ ≈ 1.5 over 3 known D′ draws"): two of the three were not D′. D′ family = 31.54 / 29.16 / 28.24 (μ 29.65, n = 3); plain copies μ 25.77 σ 3.93 (Son Pham). Planning numbers now in docs/31 §7.

### 9.1 Corrections 2026-10-09 (account B, v3 throughput smoke + mount-layout finding)
- **L0 serving — MAXREQ 14 on the W4A16 Pennyroyal stack is 🔴, not 🟡.** Measured on the competition RTX (14 games, 22 min, concurrency 14): KV pool 1,011,264 tokens, usage peak 0.99, at most 12 requests ever ran, prefix reuse 93–96 % → 75.7 %, completion 512 tok/s over the wall (10-stream reference ≈ 525–626). The private cluster's "14 streams" sits on a bigger pool (NVFP4 weights, own vLLM) — the lever is KV room, not the flag. dfranzen's 10 is tuned to this pool's edge (≈ 94 % subscribed at the 58→128 Ki hysteresis mean).
- **Infra — the competition data mount moved.** From 2026-10-09 the wheels + environment files mount at `/kaggle/input/arc-prize-2026-arc-agi-3/…`; the `/kaggle/input/competitions/…` path every M2S fork hard-codes was absent in three sessions today. A resolver with fallbacks + glob (E-135) is now a required layer; a version without it ERRORs at the runtime install, in commit and rerun alike.
- **L4/L6 — E-122 "cancel on claimed-but-empty" is redundant** with `ARC3_BATCH_NOOP_BLOCK=1` (solver stops a batch after any `gameplay_changed=False` action, ungated by level); only the mismatch form (claimed change ≠ observed change) adds anything, and it is model-visible.
- **L5 — park-at-baseline is not implementable on the hidden set** (no human baseline is exposed at runtime; the scheduler only has `ARC3_PRIORITY_HUMAN_ACTIONS=25`).

