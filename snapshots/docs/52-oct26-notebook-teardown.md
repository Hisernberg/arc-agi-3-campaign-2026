# docs/52 — SIX-NOTEBOOK TEARDOWN (user mega-directive, Oct-26 15:0xZ)

Directive: go through the 6 named public notebooks, extract how each uses
Qwen3.8 / Qwen3.8-Flash-Next and everything else, fold into tomorrow's GOLDRUSH
build. Sources pulled byte-exact via `kernels/pull` →
`research/top_notebooks/directive_1026/` (+ `deltas/` for the 15 unique cells).

## 1. THE BIG FINDING: one chassis, six skins

All six notebooks are the **same chassis**: Daniel Franzen's Milestone-2
solution on Tufa Labs' Duck harness. Content-hash alignment over all cells:

| Shared block | Size | Present in |
|---|---|---|
| `harness-changes.patch` (%%writefile) | **498,799 ch, byte-identical ×6** | all |
| Serving launcher (`/tmp/sgl-intel` venv, Pennyroyal SGLang) | 18,718 ch identical ×6 | all |
| "About this notebook" markdown | 1,858 ch identical ×3 | heliosli, romantamrazov, (dfranzen has v3-updated 2,296) |
| Env cell (MODEL_DIR etc.) | 5,175 ch identical ×3 | heliosli, romantamrazov, dfranzen |

Differentiation lives ONLY in: (a) the customization-hook cell, (b) optional
extra fork cells inserted before the benchmark, (c) env-cell hardening deltas.

## 2. Qwen3.8 usage — identical across all six

`qwen 3.8` = **Qwen3.8-Flash-Next** (8B-class, `Qwen/Qwen3.8-Flash-Next`);
`qwen 3.8 flesh` = Flash-Next. Nobody in this six runs the 27B on Kaggle GPU.

| Piece | Value |
|---|---|
| MODEL_DIR | `dfranzen/intel-qwen3.8-flash-next-w4a16-autoround` (Intel AutoRound **W4A16**) |
| DRAFT_MODEL_DIR | `dfranzen/albucino-qwen3-8-flash-next-drafter` (Albucino **MTP drafter**) |
| Serving | Pennyroyal SGLang v253 wheelhouse, venv `/tmp/sgl-intel`, port 8001, name `flashnext` |
| CFG | CTX=136,192 · MEMFRAC=0.96 · MAXREQ=10 · page 64 · CHUNK=8192 · MAX_PREFILL=16384 · KVDTYPE=fp8_e4m3 · Mamba cache 60 · schedule-policy lpm · watchdog 1800 |
| Spec decode | SPEC=True, FRSPEC, SPEC_STEPS=3, ACCEPT_SINGLE=1.0, draft-kv fp8 |
| Hygiene | TOKENIZER_SHA/TOKEN_MAP_SHA pinned; cuda-graph bs {1,2,4,7,8,9,10}; linear backend flashinfer |

Our v13 already serves **Qwen3.8-27B-FP8** (saltb0x) with the same serving
lineage — a tier above all six public notebooks. Receipt `#OURS_V38 served=...`
verifies at G2.

## 3. Per-notebook verdicts

### (a) dfranzen/arc-agi-3-milestone-2-solution (v3, baseline)
v3 = 4 demo passes, hook: `n_passes=4→1`, TRUE_SUBMISSION → concurrency 120,
`max_runtime_s_per_game=532*60`, asserts 32400 s budget. Scores on record:
LB 27.89, best draw 31.47, unchanged resub 27.62 → **draw σ is ±2**, one
reading never promotes (matches docs/49 doctrine).

### (b) heliosli/try-merging-it… (v12) and (c) romantamrazov/the-agi-boys-i-am-better (v86)
**ZERO unique cells** vs each other (and vs dfranzen except its v3-updated
markdown/hook). These are **redraw farms of the exact M2 v3 config** —
romantamrazov pushed **86 versions**, heliosli 12. Titles are honest: "you
might get lucky", "I am better". Doctrine confirmed: on a ±2σ draw spread,
**max-of-N redraws of a proven config is a strategy, not a joke**. This
validates docs/45 §6 D5–D7 redraw ladder and adds evidence that the farm can
be run on the same kernel slug with version increments.

### (d) weitaoguo/affectify-arc-dfranzen-form-d1 (D′ slot priority) — LB 31.54 (n=1)
Replaces Franzen's scheduler priority with **D′ = A·M·C + B·φ**:

```
A = (1 + 0.5·(ℓ−1))·norm(N) × (300/(300+a))^2.5      # depth × action-efficiency
M = clip((30_000/pace)^0.4, 0.25, 4)                  # pace = mean tokens/cleared level
C = 0.1·max(0.1, 1−a/115) + 0.9·max(0.1, 1−t/T)       # stuck-decay, floor 0.1
    T = 225_000·clip(pace/30_000, 0.5, 2)^0.5          # slower game → longer patience
B = {rem≥3:16, 2:14, 1:10, 0:0}  (additive)           # room-to-grow
φ = tail fade 1→0 over last 40% of run
```
Plus: fresh games priced by the same formula (no more automatic first-pass);
env `ARC3_PRIORITY_PACE/REFRESH_QUEUE/TAIL_FADE(=0.4)`; fails loudly if
scheduler names change; receipt `#OURS_FRESH replaced=N` + `#OURS_FORM ok
version=d_prime`. Their sim said ~+1.5; one LB draw said 31.54 (+3.7 over
their own unchanged resub 27.62). **Already adopted in apex-v12/v13** (D3
tgraph priors are layered ON TOP of D′). Constants banked for tuning: eff 300/
2.5, action_scale 115, token_scale 225k, pace_ref 30k, fade 0.4.

### (e) yongjiehishi/arc3-duck-lab-t06 (the evaluation notebook) — private-set best 31.05 (8 draws: 22.06–31.05)
Ports D′ (same module, dated 2026-10-05) + adds a robust path-finder in env
cell. **Its real value is the negative results — read and obey:**
1. **Throughput is not the lever.** 2.7× actions → levels 33→35 only; generated
   tokens invariant ±12% at every concurrency.
2. **Admission control is not the lever.** concurrency 10→24 + gate raise:
   25-game local mean 2.3× better, but private set 15.67 vs 19.53/16.60 —
   local starvation is a queueing artefact, does NOT transfer.
3. **A priority function derived from the official scoring formula LOST to the
   hand-tuned heuristic** (13.37 vs 18.07 private-set mean). Right objective ≠
   right scheduler.
4. **`ARC3_NOOP_REPEAT_GUARD=1` = +16 levels on 25 public games, replicated** —
   a switch its author shipped disabled. (Our v13 carries its own
   `noop_repeat_guard.py` patch + D2 stall-knee; audit parity at G2.)

### (f) vickyfym/arc-agi-3-lalalia-final — LB 31.46 ("cache-safe solved-level memory")
Franzen config **unchanged** + one harness patch (`SOLVED_LEVEL_MEMORY_PATCH`,
adapted from rellik13/sirikilohit "M85", credited +2.8 LB):
- On level clear: record level #, actions used, winning attempt's last 30
  actions, 900 ch of the clearing turn's reasoning tail; then ask the model in
  the next 2 turns for one `Rule for level N:` line (≤600 ch), captured from
  reply or reasoning.
- Pin as ONE block at the END of system prompt (full detail only for last 3
  levels); block rewritten **only when a history drain already forces a
  re-read** → prefix cache never invalidated (measured 94.3% hit rate, zero
  throughput cost).
- Implementation: wraps `ToolAgent.analyze`, `_build_user_prompt`,
  `_note_history_evicted`, `_trim_messages_for_context`; every error is
  fail-open ("turn unchanged").
- Also hardens env: `SERVER_STARTUP_TIMEOUT=55*60`,
  `ARC3_HTTP_RETRY_INITIAL_SECONDS=3600`.
- Their caution: efficiency tweaks that looked neutral on public games cost
  **7–8 points on hidden games** — keep the champion config, add memory only.

### weitaoguo env delta (extra)
Adds an `arc3-probe` gateway reachability loop with step-retry — same lesson
as our guard-v2 (survived 3612 s DNS outage). No action needed.

## 4. Adoption table for our stack

| # | Technique | Source | Verdict |
|---|---|---|---|
| 1 | Solved-level memory (cache-safe pin, rule lines) | vickyfym M85 | **ADOPT → v14 top priority** (+2.8 LB evidence, zero-cost design) |
| 2 | D′ scheduler | weitaoguo | **ALREADY IN v13** (layered with D3) |
| 3 | NOOP-repeat guard | yongjiehishi (+16 levels) | **AUDIT parity vs our noop_repeat_guard + stall-knee at G2** |
| 4 | HTTP retry 3600 s / startup 55 min | vickyfym | **RAISE ours** if weaker (compare `_http_retry_delay_seconds` caps) |
| 5 | Redraw farm of proven config | heliosli/romantamrazov | **CONFIRMS D5–D7 ladder**; A-lane dprime redraw = free lottery tickets |
| 6 | Concurrency/admission experiments | yongjiehishi | **REJECT** (does not transfer to hidden set) |
| 7 | Throughput pushing (spec/concurrency) | yongjiehishi | **REJECT** (tokens invariant) |
| 8 | Efficiency tweaks w/o hidden-set proof | vickyfym warning | **DOCTRINE: public-neutral ≠ hidden-neutral** |

## 5. Scoreboard sanity (public claims, n as stated)

31.54 D′ (n=1) · 31.46 memory (n=1) · 31.05 eval stack (n=8 max) · 31.47
dfranzen best draw · redraw farms = same config, N draws. **Nothing public
beats our 33.50 board best**; our 27B swap + D2+D3 stack is the frontier we
defend. Gap to gold stays ~5–6 pts → memory + farm + draw-max is the road.

## 6. Receipts to add to G2 for v14 (new markers)

- `SOLVED_LEVEL_MEMORY pinned: N level(s), C chars` (from patch) → treat as
  `#OURS_SLM on levels>=1`
- `#OURS_FARM draw=k config=<slug>v<v>` (our farm runner marker)
- `#OURS_RETRY base=3600` (config receipt)
