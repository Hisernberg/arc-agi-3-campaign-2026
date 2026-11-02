# docs/53 — DAILY MIXTURE ARCHITECTURES (user directive: "build new architecture each day")

Directive: each day, design a new architecture as a **mixture** of the named
families — innovative-AGI + unique-gamers, tool-based reasoning + fluid-flow,
SNN + solver + world-models — plus a concrete build spec (architecture +
algorithm + model + dataset + LLM track + non-LLM track + components + harness
changes) and a one-word keyword that triggers the build. Everything stays
inside the TAAF/Duck monkeypatch discipline: additive, fail-open, receipted.

## 0. The constant substrate (all architectures ride on it)

- Harness: Duck/TAAF + harness-changes.patch (the chassis all 6 public
  notebooks share — docs/52).
- LLM track: **Qwen3.8-27B-FP8** (saltb0x) → fallback Flash-Next W4A16 →
  fallback incumbent; MTP spec decode; Pennyroyal SGLang.
- Non-LLM track: dossier-v3 (tgraphs, pars, dead lists, playbooks, cheatsheets),
  XPACK transform tools, python tool sandbox, UCB1 expert weighting.
- Governance: guard-v2 gateway patience, G1/G2 gates, receipt lines, single
  reading never promotes, redraw farm on the A-lane token.

## 1. ARCH-HYDRA — mixture of innovative-AGI reasoning + unique-gamer priors

**Idea.** Stop treating the LLM as the only brain. A **council of 5 experts**
votes on every consequential decision; the LLM is one voter with veto, not a
monarch. Gamer priors enter as explicit voters.

**Components (voters).**
1. `TGraphVoter` — dossier-v3 transition-graph prior for (game, level): ranks
   actions by historical P(progress). Non-LLM.
2. `GamerPriorVoter` — human-budget prior ×(1+0.7(p−0.5)) + dead-action ×0.65
   (already proven in v13 D3 #48). Non-LLM.
3. `PaceVoter` — pace ×0.88 @>1.25·par (#66) and endgame tilt/suppress (#67).
   Non-LLM.
4. `NoveltyVoter` — frame-delta hash: if this (screen, last-action) pair was
   seen ≥3 times with no level change, vote to switch probe recipe. Non-LLM.
5. `LLMVoter` — Qwen3.8-27B with tools; keeps VETO on non-LLM consensus.

**Algorithm.** Each voter emits (action_bucket, confidence) ∈ [0,1]. UCB1
maintains per-voter weight w_i from realized level-clears. Final score =
Σ w_i·c_i·1[bucket] with tiebreak by LLM veto flag. Weights update at every
level transition (no GPU cost).

**Model / dataset / harness.** Model = 27B-FP8 (LLM voter only). Dataset =
dossier-v3 + a new `voter_ledger.json` (UCB1 state, per game). Harness = one
additive cell: register voters at `_run_python_tool` boundary, intercept
priority only (never rewrite LLM output). Receipts: `#OURS_HYDRA voters=5
weights=[...]`, `#OURS_HYDRA veto=used/skipped`.

**Keyword: `HYDRA`.**

## 2. ARCH-RIVER — tool-based reasoning + fluid-flow scheduler

**Idea.** The 110-game tournament is a fluid. Games are particles carrying
**pressure** (D′ priority), the concurrency slots are channels, and the
scheduler is flow control. Tools are the riverbed.

**Flow laws (additive to D′, which stays the base).**
- **Backpressure**: a game finishing a level early donates its unused
  `max_runtime_s_per_game` slice to a shared pool; stuck games draw from the
  pool with D′-weighted priority.
- **Laminar freeze**: after a level transition, freeze that game's priority
  rank for K=3 trims (prevents thrash/resample churn observed in sim).
- **Turbulence breaker**: a game stuck >2× par gets ONE burst (a 12-action
  deterministic probe recipe from dossier playbook_v2 for its category), then
  returns to laminar mode.
- **Channel cap**: keep MAXREQ=10 (docs/52 #6: admission experiments do NOT
  transfer); flow control redistributes time, not slots.

**Tool-reasoning half.** python-tool sandbox gains three *flow tools*:
`replay_recipe(game_id)` (deterministic solved-level replay), `tgraph_lookup`
(best historical action path), `budget_state()` (how much pool credit remains).
The LLM calls them instead of re-deriving mechanics (tokens saved → pace ↑ →
D′ priority ↑, closing the loop).

**Model / dataset.** Same substrate; dataset gains `flow_ledger.json`
(donations, bursts, freeze events) — pure telemetry, no GPU.

**Harness.** One cell, monkeypatches `_PriorityGate._snapshot_priority` +
solver session runtime accounting; fail-open → vanilla D′. Receipts:
`#OURS_RIVER donated=... burst=... laminar=...`.

**Keyword: `RIVER`.**

## 3. ARCH-CORTEX — SNN novelty detector + solver + world model

**Idea.** A spiking layer as an **event-driven pre-attention filter**: frames
arrive as spikes (cell-state changes), refractory periods implement habituation
(biology's noop guard), and only novel spike patterns reach the LLM. Behind it,
a world model plans; a solver executes.

**Components.**
1. **SNN filter (CPU, pure python)**: per-cell delta → spike; global refractory
   2 steps; pattern = hash(grid-delta ⊕ last-action). Novel patterns → LLM
   prompt gets a 1-line "SIGNAL: new pattern P1234 (3rd similar to level-2
   wall break)". Habituated patterns → suppressed (this IS the noop guard,
   biological edition).
2. **World model**: dossier-v3 tgraph + transition counts → P(next-state|s,a)
   matrix per game; reward model = P(clear level N | action sequence) from
   replay dataset (8,170 real recorded actions already mined).
3. **Solver**: bounded best-first search over the tgraph using P(clear) as
   value; SNN novelty gates expansion (no re-expanding habituated states);
   search depth ≤ 8, budget ≤ 200 ms/call — CPU only.

**Algorithm.** `plan(s): return argmax_a Σ_path P(clear|path)` with
habituation mask; LLM receives plan as a suggestion, not an order (keeps
veto — same council shape as HYDRA, so v15 HYDRA voters plug straight in).

**Model / dataset.** LLM untouched; dataset adds `spike_patterns.jsonl` +
`wm_transitions.json` (grows during every run — telemetry for next-day retrain
of priors).

**Harness.** One cell + one patch file; fail-open → LLM sees raw frames as
today. Receipts: `#OURS_CORTEX spikes=... habituated=... wm_hits=...`.

**Keyword: `CORTEX`.**

## 4. Day ladder (keyword → build)

| Day | Keyword | Build | Mixture |
|---|---|---|---|
| Oct-27 | **GOLDRUSH** | fire apex-v13 (receipted) → build **v14 MEMORY-SEA** = solved-level memory (docs/52 #1) + retry-3600 raise + farm v1 | memory doctrine |
| Oct-28 | **HYDRA** | v15 = v14 + 5-voter council (UCB1) | AGI+gamers |
| Oct-29 | **RIVER** | v16 = v15 + flow control + 3 flow tools | tool-reasoning+fluid |
| Oct-30 | **CORTEX** | v17 = v16 + SNN filter + world-model planner | SNN+WM+solver |
| Oct-31+ | **FARM** | parallel: redraw farm max-of-N on champion + best-of mixtures | draw-max |

Each build = 1 push the evening before, receipts green before its 00:05Z fire.
Mixture rule: **new architecture layers additively on the last proven
champion; any red receipt at G2 → auto-fallback to prior champion** (fail-open
chain is sacred).

## 5. 34–38+ arithmetic (honest, per docs/45–49)

- v13 (27B swap + D2 + D3 + D′): expected 34–36.5 draw (P(≥34)≈35–50% on
  completion, per docs/49).
- v14 memory: +1.5–2.8 (M85 evidence) → 35.5–39 zone, and **raises the floor**
  of every later draw (memory compounds across levels within a run).
- Farm max-of-N on champion: board lens — best draw of N runs of a ±2σ config
  climbs ~0.5–1.0 per doubling of N; A-lane token gives 1 free draw/day.
- Sum path to gold zone: champion 36.5±2 + memory floor + farm max → 38–40
  becomes reachable by Oct-29/30 without any single risky leap.
