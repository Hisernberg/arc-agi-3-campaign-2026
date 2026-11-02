# 12 — Competitive Intelligence Deep Dive (2026-09-25)

Scope: every major public work on ARC-AGI-3 — Tufa Labs, NVIDIA (NOOA/AVO/NVARC), OpenAI (GPT-5.6 Sol / GPT-6 Astra), ARC Prize official analyses, the four core arXiv papers, Milestone-1 winners, PRO-LONG, Symbolica, Tycho, and the JEPA/world-model research line. Goal: extract what is **usable under our constraints** (single L4-class GPU, Qwen3-8B NVFP4, 32K ctx, Kaggle hidden set) and fold it into the v7/v8 roadmap.

---

## 1. Executive Summary

The frontier has effectively saturated the ARC-AGI-3 **public** set in the last 60 days:

| System | Model | Public-set result | Cost | Key mechanism |
|---|---|---|---|---|
| GPT-6 Astra + Provider Adapter | Astra (high) | **99.9%** (Semi-Private) | $18.8K | opaque reasoning state retained + compaction |
| GPT-6 Astra + Standard harness | Astra (max) | 62.7% (Semi-Private) | $26.1K | model-curated visible notes |
| NVIDIA AVO | Claude Opus 5 | **100.00 RHAE, 183/183 levels** | API | agent system ("harness beats model") |
| NVIDIA NOOA | GPT-5.6-sol | **85.1% mean RHAE, 19/25 games** | $13.3/game | 6 capabilities incl. typed memory, pass-by-reference |
| Tycho (actor-requested policy) | Opus 5 / GPT-5.6 Sol | **100.00 RHAE, 183/183** | API | actor-requested programmatic world models |
| PRO-LONG | Fable 5 | **97.4% best@2** (76.1% pass@1 small models) | $1,750 total | append-only log searched by code |
| Verification variant (2607.15439) | GPT-5.6-sol xhigh | all public levels, ~99% human-relative efficiency | API | exact replay verification |
| Tufa Duck (Milestone-1 winner) | Qwen 3.6 27B FP8 | 36.08% (day 1, orchestration era); duck mean 1.60±0.45 on 25 games × 20 tries | local GPU | REPL coding agent |
| **Us (best LB)** | Qwen3-8B NVFP4 | **3.85 hidden LB** (210/3277), 36/183 public levels | 1×GPU | Duck + worldmodel ledger |

**The single biggest lesson of 2026 so far: the surrounding harness — context management, memory, verification — moved scores more than model upgrades did.** OpenAI's own controlled experiment: identical GPT-5.6 Sol went 13.3% → 38.3% purely from *retained reasoning + compaction* (and by their own account 7.8% → 38.3% across evaluation conditions) while using 6× fewer output tokens. NVIDIA's AVO lifted Claude Opus 5 from 30% to 100% "without the model getting smarter". NOOA's ablations quantified the harness components: **world-modeling skill +8.5 pts, model-callable typed memory +11.8 pts** over file-based notes.

For us, three constraints matter: (1) our 8B model is far below the frontier models in these studies, so capability-dependent effects (e.g., "textual beats executable at gpt-5.5") may invert — verification helped *most* at lower effort/capability; (2) we have no provider adapter — our "opaque reasoning state" equivalent is an externalized, append-only state file + compaction policy we fully control; (3) KV budget (~3.2 full contexts) makes token-efficiency the binding resource — every published harness that won also *reduced* tokens.

**Ten transferable principles** (evidence in §5, roadmap mapping in §6):

1. Context management is the harness's main job (OpenAI 3×; NOOA half-tokens; PRO-LONG 4–5× fewer tokens).
2. Append-only structured log + code-based retrieval (PRO-LONG) — cheap, cache-valid, and lets the model decide what is relevant.
3. Model-callable typed memory (records with importance/tags/`supports`/`contradicts`/`derived-from`) — NOOA +11.8 pts.
4. A small "world-modeling skill" (NOOA's was **45 lines**) gives +8.5 pts; our worldmodel ledger is the same idea.
5. Prediction verification (exact replay against recorded observations) ranks #1 in every study that measured it (2607.15439; Astra's `sync_state.py`; ASSAY) — and helps *most* for weaker models/lower effort.
6. **Actor-requested** model building beats automatic repair (Tycho: 88.49 vs 83.07 RHAE). Transition-match ≠ right abstraction; the agent must be able to *bypass* its own model.
7. Hand-crafted tools can hurt — Tufa: "hand-crafted tools actually hurt the model; letting it improvise worked better"; 2607.15439: textual beat flexible-interface executable. All new tools must be optional, model-initiated, and ablation-toggleable.
8. Symbolic shorthand notes with high information density (Astra's `extend8 to3; retract10 to2`, `9−=(39,4)`) — teach/encourage compact notation for state and plans.
9. Cheap CPU heuristics still win wasted actions back: Reki's dead-signature + button-like click heuristics (Milestone-1 #2) — exactly our dead-action flags; keep and extend.
10. Efficiency and score go together: at frontier, higher reasoning effort *cost less* because fewer actions → fewer calls. For us: fewer wasted actions = more games advanced within the 7920 s/game and KV envelope.

---

## 2. The Frontier Picture (ARC Prize official)

### 2.1 GPT-6 Astra on ARC-AGI-3 (Greg Kamradt, arcprize.org/blog/astra, 2026-09-03)

- **Semi-Private results (score % / cost):**
  - Standard harness: max **62.7%**/$26,098 · xhigh 59.3% · high 54.8% · medium 38.6% · low 17.5% · none 35.2%
  - Provider Adapter: max **98.6%**/$17,332 · xhigh 98.4% · high **99.9%**/$18,817 · medium 98.4% · low 98.0% · none 96.7%
  - Reading: with state-retention, even *low* reasoning beats *max* reasoning without it. The harness floor (96.7% at **none**) exceeds the best Standard result (62.7%).
- **Human parity on action efficiency:** Astra (max, PA) used fewer actions than the median human on **96.0% of levels** and **51.7% fewer actions per level on average**. ARC Prize's earlier hypothesis (AI will always need more exploration) is now falsified for frontier systems — "once frontier AI 'understands' the mechanics, it executes within human efficiency".
- **Observed behavior — the thing to copy at 8B scale:** Astra *chooses* which notes to carry forward and invents a **custom algebraic notation**: `L8: hub q2 (8↓). Lengths: 14=1…`; `extend8 to3; retract10 to2; shorten8 to1`; `9−=(39,4), rotate=(49,18), 14+=(59,11)`; `Turn 5: P=(24,20), empty, facing west`. Distilled, code-like, dense.
- **In PRO-LONG harness** (sandboxed code execution) Astra wrote **per-game tool libraries**: `maze_solver.py`, `combat_solver.py`, `patrol_solver.py` (tu93) and **`sync_state.py` — checking its own model's predictions against observations**. Board parsers, game-state models, search, planners, persistent notes.
- Two-harness framing ARC Prize will now report: **Standard** (provider-neutral, model keeps visible notes — "a future AGI should solve it this way") vs **Provider Adapter** (provider's own context management). PA runs: **3.66× faster, 49% fewer tokens** across 167 game-reasoning pairs.

### 2.2 Milestone Prize #1 (arcprize.org/blog/arc-prize-2026-milestone-1, 2026-07-06) — $37.5K

1. **Tufa Labs "The Duck"** — the only "agent-writes-code" winner; REPL; Qwen 3.6 27B FP8; "infinite play via eviction"; perception = rendered image + raw ASCII + segmentation zoom, model picks representation. **"Counterintuitively, hand-crafted tools actually hurt the model; letting it improvise worked better."** Gains attributed to multimodality + base models, not hand-built tools.
2. **Reki** — Gemma-4-31B vision-as-policy, 1 JSON action/turn, reflection memory refreshed ~10 steps, JSON self-repair, legal-action constraints, 1–4 action plan queue, **numpy click heuristic** (prefer small/rare-colored/button-like shapes), **dead-signature** (clicks that never change anything are retired for the level). Everything toggle-able via env vars — designed for ablation.
3. **forge** — same core, profile-driven framework with candidate generator + arbiter + confidence prompt; **the top-scoring run used the profile that turned ALL extra machinery OFF**. Author: local public-game checks are not a reliable LB proxy (matches our v3 lesson).

⚠️ **Milestone 2 ends September 30 (5 days).** It rewards top **open-source** mid-competition submissions. Our repo is private — decision needed from user if we want to compete for it (open-sourcing the harness is compatible with keeping the campaign repo private by extracting a clean OSS snapshot).

### 2.3 ARC-AGI-3's four tested components (official framing)

Exploration (information is not passive) · Modeling (observations → predictive model) · Goal-setting (sparse rewards) · Planning & execution (course-correcting path). Our ledger + dead-flags + budget-prior covers 1/3/4; the modeling leg is where NOOA/Tycho/2607.15439 all put their wins.

---

## 3. NVIDIA Deep Dive

### 3.1 NOOA — NVIDIA Labs Object-Oriented Agents (blog 2026-07-27; GitHub `NVIDIA-NeMo/labs-OO-Agents`; paper by P. Furgale et al. 2026)

Model-agnostic, open-source Python framework ("an agent is a single Python class"). **Six model-facing interface ideas**:

1. **Typed input/output**
2. **Pass by reference** — tool results become *live Python variables* composed in code instead of text round-trips; transcripts stay append-only and cache-valid; **no compaction needed**; SWE-bench Verified 82.2% at 29 calls/~1.1M tokens vs 66 calls/2.2M for comparison harnesses (78.2%)
3. **Code as action**
4. **Programmable loop engineering**
5. **Explicit object state**
6. **Model-callable harness APIs** — context blocks + event history are APIs the model can inspect/manage

**Memory subsystem (the headline for us):** not background summarization — the agent **deliberately writes/queries/corrects typed records** via model-callable tools (types, importance, tags; typed relations `supports` / `contradicts` / `derived-from` → a knowledge graph in a human-readable **SQLite** file persisting across sessions); relevant spontaneous memories surface automatically into context.

**ARC-AGI-3 results:** one generic agent + a **45-line world-modeling skill**: GPT-5.5 fleet **50.2% mean RHAE** ($17.85/game), GPT-5.6-sol fleet **85.1%** ($13.3/game, 19/25 games fully solved) — "advancing the score–cost Pareto frontier". **Ablations: world-modeling skill +8.5 pts over hypothesis-driven baseline; memory subsystem +11.8 pts over file-based notes.** CyberGym L1 86.8% (top, no network).

This is, almost line for line, our P1+P2 design (observation tools + mechanism memory with premises/support/counterexamples), now validated with published ablation numbers. Our v2 carry-note is a file-based note — NOOA's +11.8 is precisely over that baseline.

### 3.2 AVO (blog announced 2026-08-21)

NVIDIA agent system ("the surrounding agent system — often called a harness — determines how the model receives context, uses tools, maintains state, responds to feedback") lifting **Claude Opus 5 from 30.2% → 100.00 RHAE on all 183 public levels**. Coverage: Forbes 2026-08-24, The New Stack 2026-08-21 ("Claude Opus 5 scored 30%... Wrapped in [the right harness]"), eneralabs 2026-08-23 ("Agent Harness Beats the Model"). Full primary post URL was not retrievable via page_reader; the substantive claim set is consistent across four independent secondary sources. Also characterized as an autonomous coding agent that optimizes GPU kernels — i.e., a general long-horizon harness, not an ARC-specialist.

### 3.3 NVARC heritage + world-model line

- **NVARC** (Ivan Sorokin, Jean-François Puget) won Kaggle ARC Prize 2025 (ARC-AGI-2, 27.64% public / 29.72% final) — the Kaggle-NVIDIA lineage behind the current NVARC3 team (11.04 on AGI-3 LB as of our sweep).
- NVIDIA world-model blog (2026-06-15, "Pretrained to Imagine, Fine-Tuned to Act"): **action-conditioned world models (DreamDojo, Genie, JEPA-WM)** predict future states from a learned action abstraction; robotics framing. Supports our M-series JEPA plan being on-trend.
- Relevant serving intel: NVIDIA blog on **Qwen3-8-Flash-Next on GB300 NVL72 for agentic coding** — our exact model class getting first-party NVIDIA attention.

---

## 4. OpenAI + the academic core

### 4.1 OpenAI "two settings" (2026-07-29)

Official harness GPT-5.6 Sol **13.3%** → **38.3%** with **retained reasoning + compaction**; 6× fewer output tokens; other writeups cite 7.8% → 38.3% across conditions ("GPT-5.6 Sol Didn't Get Smarter. Its Memory Did.", aifounders.cz). The-decoder: OpenAI explicitly countered Anthropic's Opus-5 record — and noted the 38.3% used OpenAI API features instead of the official harness. Then The New Stack (2026-09-04): "OpenAI will sell you Astra, but not the system that scored…" — the scoring *harness* remains proprietary even as the model ships.

**Our equivalent of "retained reasoning + compaction"** (we have no provider): an externalized reasoning-state file the agent writes to every decision (already in worldmodel-v1/v2 as the carry note) + deliberate compaction of history segments instead of blind oldest-eviction. The Astra table says the *ceiling* of this technique alone is ~97% (none-effort PA) — the mechanism, not intelligence, does the lifting.

### 4.2 The four core papers

| Paper | ID | Result | Take |
|---|---|---|---|
| Executable World Models for ARC-AGI-3 in the Era of Coding Agents | arXiv:2605.05138 (AGI conf.) | agent maintains executable Python world model, verifies vs recorded observations, refactors toward simpler abstractions (MDL proxy) | the founding recipe of the line |
| Do Coding Agents Need Executable World Models, Simplification, and Verification to Solve ARC-AGI-3? (S. Rodionov) | arXiv:2607.15439 (v2 2026-08-27, 45 pp) | 4 variants (textual / flexible-executable / exec+simplification / fixed-interface+simplification+exact-replay-verification) on gpt-5.4/5.5, follow-ups gpt-5.6-sol | see findings below |
| Tycho: Active Abstraction with Programmatic World Models | arXiv:2607.28287 | formalizes games as parameterized rendered deterministic Moore machines; 4 orchestration policies, matched budgets, Opus 4.8 | **actor-requested** model building best (RHAE 88.49); with it, Opus5 & GPT-5.6 Sol hit 100.00, 183/183, Opus5 61% fewer actions than human baseline |
| PRO-LONG: Programmatic Memory Enables Long-Horizon Reasoning (Fox, Wang, Rosu, Dhingra) | arXiv:2607.20064 | append-only complete structured log; agent **searches its own history with code**; +18.0 pp avg over base coding agent; matches/exceeds specialized harnesses (76.1% pass@1) at **4.2–5.8× fewer tokens**; Fable 5 **97.4% best@2** at $1,750 | the cheapest big win in the literature; directly portable to our Python-tool sandbox |

**2607.15439 findings in detail (matters for an 8B model):**
- Gains from model capability & reasoning effort **often exceed** variant differences — but verification still ranked first *throughout*.
- **Textual beat flexible-interface executable in both gpt-5.5 conditions** — mandating an executable deliverable is not universally good (consistent with Tufa's "tools hurt" and Duck's state-schema ablation).
- Simplification prompts beat executable-only in 3/4 settings.
- Verification ranked #1 everywhere, at substantially higher resource cost — but with gpt-5.6-sol it completed every public level at ~99% human-relative efficiency using <half the human baseline's total actions.
- **At max effort even textual completed all levels with 41% fewer actions than human baseline** — imposed mechanisms are for *making weaker/less-careful operation reliable*, which is exactly our regime.

### 4.3 Tycho's repair paradox (design constraint for our skills)

Auto-repair after verification failures produced simulators that **reproduce observed transitions much more accurately, yet scored lower (83.07 vs 88.49 RHAE)**. "Transition match indicates whether a simulator reproduces observed dynamics, not whether it has identified [the game's abstraction]." → Our P3 skills must be: requested by the actor when *it* sees value, testable, and **bypassable** — never auto-polished in a loop against transition-match.

---

## 5. JEPA / small-model research line (for our M1–M4 roadmap)

- **Agentic-JEPA** (hal-05546567v2, 2026-03/05): JEPA as a **self-supervised world model for text-based agent planning** — LLMs act by next-token/CoT "without an explicit internal model of how actions transform the environment"; builds exactly that missing model in latent space. Closest published match to the user-requested "JEPA classifier" idea; feasible at our scale because JEPA encoders are small (V-JEPA-2 is 30× faster than Cosmos-class video WMs).
- **TD-JEPA** (ICLR 2026; `facebookresearch/td_jepa`): latent-predictive representations for zero-shot transfer; temporal-difference-style training of JEPA — the training recipe to copy for a grid-world latent predictor.
- **JEDI** (arXiv, 2026-05-13): Joint-Embedding **Diffusion** world model for online RL — JEPA representations + diffusion decoder for imagination; MBRL state of the art direction.
- **V-JEPA 2** (Meta): video JEPA world model, planning with 30× less compute than pixel WMs; the existence proof that small latent-predictive models beat big generative ones at prediction-speed-critical tasks (our per-decision latency budget matters).
- **Dreamer lineage** (Hafner et al., Nature 2025, 811+ citations) and **MuZero**: the classic action-conditioned latent planning stack; "LLM-Based World Models Can Make Decisions Solely, But…" (arXiv 2026-03-19) studies LLM-WM vs learned-WM decision quality.
- **Snorkel "Code World Models and AutoHarness"** (2026-05-14): two split strategies — CWM learns a full simulator and hands it to a planner; **AutoHarness keeps code synthesis inside the agentic decision loop** (the variant that matches our REPL reality).
- **Agent Harness survey** (Q. Meng 2026, 33+ citations; RUCAIBox/awesome-agent-harness): nine core harness components — good checklist for our architecture doc; plus "Natural-Language Agent Harnesses" (arXiv) cataloguing reason–act / retrieval / reflection / verification / memory / search / orchestration patterns.

**Synthesis for us:** the community converged on (a) latent/action-conditioned world models for *prediction* and (b) programmatic memory + verification for *long-horizon reliability*. Our P6 "learned router" and M1–M4 JEPA plan should target a **tiny action-conditioned latent predictor over 64×64 grids** used (i) as a cheap pre-action sanity check (ASSAY-style "no prediction → no action") and (ii) as a novelty/stagnation detector feeding the scheduler — never as an autopilot (Tycho's lesson).

---

## 6. What we adopt — v7/v8 roadmap update

Mapping evidence → our existing P0–P7 plan (docs/11 Master Plan v3) and the v6 sweep bundle:

| # | Adopt (evidence) | Into | Risk control |
|---|---|---|---|
| 1 | **Append-only structured log + code-searchable retrieval** (PRO-LONG: +18 pp, 4–5× fewer tokens) | v7: replace/augment oldest-eviction with full JSONL log in sandbox + `search_log()` helper; eviction stays as fallback | log capped per level; fail-open to current behavior |
| 2 | **Typed model-callable memory** in SQLite-ish store: records {type, importance, tags, supports/contradicts/derived-from} (NOOA +11.8) | v7: upgrade single carry-note → record store with `mem_write/mem_query` tools | toggles OFF default? No — memory was the *largest* gain; ship ON, keep env kill-switch |
| 3 | **World-modeling skill block** in system prompt (NOOA +8.5 with a 45-line skill; Astra shorthand) | v7: teach `state:→predict→compare→update` loop + algebraic shorthand examples in prompt | token budget +~300; measure |
| 4 | **sync_state verification** — after each real action, compare predicted changed-cells vs observed (2607.15439 #1; Astra sync_state.py; ASSAY) | v7: extend v2 diff block with prediction-match flag; on mismatch ≥k, inject "model wrong, re-derive" note | fail-open; don't block actions (lesson 8) |
| 5 | **Dead-signature + button-like click heuristic** (Reki) | v8: our dead-flags already fire; add shape-prior click ordering for click games | env-toggle, measure |
| 6 | **Actor-requested skill/model building, bypassable** (Tycho 88.49 vs 83.07) | v8: model may *request* a planner/solver for current game via tool; no auto-repair loops | hard cap per game; bypass always available |
| 7 | **Compaction policy = our provider-adapter** (OpenAI 13.3→38.3; Astra PA floor 96.7%) | v8: segment-summaries on level-up + stagnation instead of raw eviction | measure tokens saved |
| 8 | Small **JEPA-lite predictor** (Agentic-JEPA/TD-JEPA recipes) for pre-action sanity + novelty | M1–M4 (post-v8), CPU/GPU hybrid | never autopilot; gated |
| 9 | **Efficiency compounding**: fewer wasted actions → more games/levels within budget (Astra: higher effort cost *less*) | scheduler: raise priority of games with verified-progress trajectories | aging credit stays |

**Explicit non-adoptions (with reasons):** flexible-interface mandatory executable world model (2607.15439: textual won twice); auto-repair-to-transition-match loops (Tycho paradox); heavy hand-built perception pipelines (Tufa: hurt; forge: best run disabled machinery); Provider-Adapter-specific features (not available to us; our externalized state is the analog).

**Sequencing given GPU reality (~5 h runs, weekly quota):**
- **v7 "NOOA-lite"** = items 1–4 (memory + verification + skill prompt + log search). Buildable and testable CPU-only this week; aligns with Milestone-2 date if user opts to open-source a snapshot.
- **v8** = items 5–7 + scheduler change (item 9).
- **M1+** = JEPA-lite predictor (item 8) as a small model artifact attached to the kernel (dataset) — no serving cost.

**Milestone-2 decision (deadline Sep 30):** requires open-source submission. Options: (a) open-source a cleaned harness snapshot under a new public repo, keep campaign repo private; (b) skip. Recommend (a) only if v7 lands green before Sep 28.

## 7. Source index

Primary: arcprize.org/blog/astra · arcprize.org/blog/arc-prize-2026-milestone-1 · tufalabs.ai/research/duck-harness/ · developer.nvidia.com/blog/six-agent-harness-capabilities-for-higher-model-performance/ · developer.nvidia.com/blog/nvidia-avo-reaches-100-on-arc-agi-3/ (title confirmed; body via Forbes/New Stack/eneralabs/Threads secondaries) · openai.com "How enabling two settings tripled our scores on the ARC-AGI-3 public set" · arxiv.org/abs/2605.05138 · /abs/2607.15439 · /abs/2607.28287 · /abs/2607.20064 · github.com/NVIDIA-NeMo/labs-OO-Agents · github.com/alexisfox7/PRO-LONG · github.com/Tufalabs/duck-harness.
Secondary: thenewstack.io (2026-08-21, 2026-09-04) · forbes.com (2026-08-24) · eneralabs.com (2026-08-23) · the-decoder.com (2026-07-30) · aifounders.cz (2026-08-02) · umesh-malik.com (2026-08-04) · snorkel.ai (2026-05-14) · hal.science/hal-05546567v2 · facebookresearch/td_jepa · ai.meta.com V-JEPA 2 · RUCAIBox/awesome-agent-harness · developer.nvidia.com NVARC grandmasters (2025-12-05) · mlq.ai Opus-5 record (2026-07-26).
