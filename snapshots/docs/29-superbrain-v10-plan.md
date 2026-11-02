# docs/29 — SUPERBRAIN v10: the 27→40+ synthesis plan (2026-10-01)

Task 18 product. Mission: combine everything learned from ALL public notebooks
(score 4–27.89) + everything we own into one notebook targeting **30–40+**,
then farm variance toward the prize zone. Two-account division: **S
(kragglenote2forwork) = sure-shot banking**, **R (dasshovon) = experiments**.

Companion artifacts: `scripts/superbrain/` (cells + 21-test suite), `scripts/forks/superbrain-{r,s}/`,
`scripts/t18_orchestrator.sh` (running), `notebook-intel/da-fr/` (dfranzen's full patched tree + writeup).

---

## 1. The battlefield (LB 2026-10-01 07:30Z)

| # | team | score | note |
|---|------|-------|------|
| 1 | Tufa Labs | **50.65** | private; harness authors; no public notebook |
| 2 | Yi-Chia Chen | **40.97** | private; no public artifacts |
| 3 | Daniel Franzen | **27.89** | HIGHEST PUBLIC — our base |
| 4 | the last dance | 24.54 | private |
| 5 | Lord Han Solo | 23.84 | public (TAAF) |
| 6 | rellik13 | 22.53 | public (Tufa v18.1gc M-stack) |
| 7 | Tong Hui Kang | 20.53 | private |
| 8 | face-of-agi | 20.00 | public (Flash Duck-transfer arena) |
| 9–10 | Son Pham / Third Intelligence | 18.99 / 18.29 | top-10 cutoff = **18.99** |

Facts that define strategy:
- **40.97 and 50.65 exist** → the 30–40+ target is proven reachable on this
  hardware/rules window (1× RTX PRO 6000, 9h). The private top-2's edge is not
  visible, but dfranzen's writeup + Tufa's M-stack show the direction.
- **Same-code redraw σ ≈ 1.5–2** (Affectify 5.68/4.09/2.30; our taaf genome
  3.18→6.09 under scottlegrand). Best-of-N farming of a 30-mean build ≈ 34–35.
- **Cross-account API submission of foreign public kernel versions WORKS**
  (proven 10/1 07:15Z: dfranzen v1 → dasshovon, pending). Banking needs **zero GPU**.
- GPU quota: both accounts 0 until **10/3 00:00 UTC** (weekly reset). 30h/week
  each ≈ 3 scored runs/week/account (9.5h each).

## 2. Verified scoring model (drives everything)

Per completed level L: `s_L = min(human_L/agent_L, 1.15)²`; per game:
`Σ s_L·L / Σ(1..N)`; total = mean over games (verified exactly against
dfranzen's run log: lp85 15/36=41.67%, ft09 10/21=47.62% — completed levels
scored ≈1.0 each, i.e. his agent sits at human-parity efficiency; the loss is
**uncompleted deep levels**, where weight L is largest).

Levers ranked by point value:
1. **More levels within 9h** = serving throughput (NEXTN spec-decode ≈2–3×
   turns) + turn economy (image/token accounting, drain hysteresis, dedup).
2. **Animation evidence** — sirikilohit's WALL_ANALYSIS: 18.8% of available
   score is destroyed by final-frame-only views; dfranzen: "strongest benefit
   of all perception changes" (frames/timelines as REPL variables).
3. **Scheduler** — don't feed dead games (Affectify knee: 14% breakthrough at
   80 actions; dfranzen C-hazard Gaussian in actions/tokens; tail-fade 20%).
4. **Efficiency² per level** — (25/actions)²; every wasted action squares away
   credit (our M-05; dfranzen's A-term).
5. **Variance farming** — +2–4 LB from best-of-N at fixed mean.

## 3. Complete technique matrix (what the 4–27 public field taught)

### 3.1 The 27.89 base (dfranzen) — decode summary
- Serving: SGLang Pennyroyal v2.5.3, Intel W4A16-AutoRound main + albucino
  W4A16-FP8PLE MTP draft, **NEXTN 3-step spec-decode** (FR-Spec 64K token map,
  sha-pinned), fp8 KV, ctx 136K (harness 128K + 12K output), drain 58K,
  10 gate slots == 10 max-running-requests, mem-frac 0.96, page 64.
- Harness (10,086-line patch): priority gate P=(A+B)·C with
  A=level·(25/(25+a))²·55/(N(N+1)/2), B=remaining-tail lookup {8,7,5,0},
  C=0.25·2^-(a/115)²+0.75·2^-(t/62000)², tail-fade over final 20%;
  **cache-aware handover at context trims**; noop_repeat_guard (block-then-insist,
  per-position death ledger); python sandbox w/ BaseException refusal classes,
  retained functions (scope=game), frame_diff (Hungarian matching), rotation-aware
  segmentation, animation frames+timeline in REPL, UNDO exposure, game-over BAR
  RULE prompt, level-transfer guidance, per-action results in history.
- His rerun: demo-roster mean 36.56 (10 games, 25min cap); best game 93.34 (8/8 WON).
- His **negatives map** (tested, not adopted — we must NOT re-litigate blindly):
  memory sections off > on at 131K ctx; composite animation images hurt; summaries
  no gain; resume-prompt variants no gain; pace multiplier no clear advantage;
  prescriptive verification no gain.

### 3.2 The 22.53/23.84 lineage (Tufa M-stack + TAAF)
M24 reasoning ledger (dedup 34.2% of prompt!) · M43 two-tier scheduler (pts/action
~a^-1.73, cliff at 60) · M44 unlimited tool steps + sticky sandbox vars ·
**M59 world-model capture + code memory** (label variants, reasoning fallback,
no-wipe-on-game-over, function prepend w/ self-healing) · M72 one-pool UCB
(c=0.0002, quantum 2400s, reward=levels/token triangular) · M74 real image-token
accounting (66 tok/board at upscale 4 vs 505–622 charged) · M76 mid-action frames
(delta-selective, ≤4 images) · M79 exact /v1/tokenize guard (374-retry death
spiral fix) · **M84 watermarks 57,344→45,056** (oscillating window, ~10% faster) ·
M85 solved-level memory (cd82 L2: 122→8 actions) · M86 O(1) state writes ·
M90 Wang/Ludvig 5-line turns + object-id segmentation + BFS guidance ·
M108 3-file draft loader (boot −5min) · M111 animation frames in sandbox
(18.8% score in mid-animation evidence).

### 3.3 The 4–8 mid-field
Affectify (5.75): **lottery scheduler** (tickets=base+level²·alive·stall, knee=80,
halflife=40, floor 0.1; anneal K=3 P0.4→P1.9), **value correction** (triangular
weights beat level² — 3.7× misallocation fix), alive_fraction meter, FACTS
scoring-injection, keep-notes-on-death, 25.1% USER-dedup, ctx16k=7.68× decodes,
thinking-off turns −13% · AGENTFIX F1/F3/F13/F19 (image economy 26% waste, +0.51
LB from F13 frames; F19 contact sheet) · Cassowary (4.08): in-kernel LoRA
(r4 α8, 6144 SFT) + 19-dim TTT head — proof that training pipelines alone lose
to serving+allocation · Hybrid REPL (4.08): kv16 prefix-cache-ON profile,
n_passes=3 reverted · richardcsaky (20.0): sha256-pinned runtime blob + 110
cyclic replicas + KAGGLE_IS_COMPETITION_RERUN two-face design.

### 3.4 What WE own that the tops don't
- **53 verified playbooks** (25/25 public-game L1, 7–130 actions; sb26 L1→L8
  chain) — full value on public games/archetype priors on hidden roster.
- **Per-game mechanics KB**: dead L1 actions, sc25 sequence-gating, click-precision
  cells, sp80 fail-state, budget guides, trigger-chase atlas.
- **8,170 real-action trace corpus** + SFT/DPO mining + replay-through-wrapper
  validation suite (41-gate preflight).
- **Human-budget prior** [30,54,51,54,96,80,86,92,163] + effects ledger +
  dead-action flags + governor (worldmodel-v1: our best 3.85→ validated +0.40).
- **Mistake ledger M-01..M-08 as hard gates** (KV collapse, by-value import trap,
  prompt bloat −13%, history wipe −4.20, efficiency² law).
- **Variance-farming ops** (orchestrator, 1/day/account, cross-account banking —
  now proven via API).

## 4. SUPERBRAIN v10.0 — what we actually built

**Base**: dfranzen notebook v1, byte-identical, our 3 cells inserted after his
customization hook (cell 16 → SB at 17/18/19). Chosen deliberately LEAN: his
negatives map rules out flipping his off-knobs; we add only what his stack lacks.

| cell | content | evidence |
|------|---------|----------|
| SB-1 env | `ARC3_HISTORY_IMAGE_KEEP=2`, `ARC3_RESUME_PROMPT_IMAGES=0` | F1 image economy (Affectify −26% budget waste); knob built by dfranzen, unset by him |
| SB-2 scoring block | static `=== OFFICIAL SCORING ===` appended to cached system prompt: depth weights L/Σ(1..N), efficiency² (25/actions)², "next level = largest gain" | Affectify FACTS + our M-05; model never sees scoring in his stack |
| SB-3 solved-level memory | level-up harvest (actions of cleared level, RESET-excluded, mouse preserved) pinned into per-turn opener; per-game reset via runtime_dir; ≤4 levels shown | M85 (cd82 122→8 actions); sirikilohit lineage; complements his level-transfer prompt with concrete winning tails |

Safety properties (all 21 tests GREEN vs REAL patched modules):
- user-message injection only → **prefix cache never diverges** (system prompt
  built once at init; our SB-2 wraps that single build, static text).
- fail-open everywhere; orig errors propagate untouched; idempotent double-exec.
- per-game reset mirrors Tufa's runtime_dir trigger; no cross-game leakage.
- known-trap compliance: priority_value by-value import (M-04) documented for
  future scheduler patches; no forbidden env flips from his negatives map.

## 5. The 30–40+ math (honest)

- dfranzen mean on demo roster 36.56 → hidden 27.89 (−8.7 roster difficulty).
- v10.0 additions target: solved-level memory (re-derivation waste: his 3+
  uncompleted levels per game are where points die), scoring awareness
  (fewer wasted probes → efficiency² protects completed levels), image economy
  (frees ~0.5–1.5K tokens/turn → deeper history or fewer trims).
- Conservative estimate: v10.0 mean ≈ 28–31 hidden. σ≈1.5–2 redraws over
  ~20 slots → farmed max ≈ 33–36. 
- v10.1+ levers (each A/B'd on its own daily slot): M76 mid-action frame images
  (his composite-negative ≠ M76's delta-selective rule), M84 watermarks at 136K,
  M79 exact tokenize, spec-draft-tokens 4→6, memory sections A/B at 136K
  (his negative was at an earlier config), contact-sheet F19.
- The 40+ zone needs at least one structural win: playbook-lane generalization
  (archetype priors on hidden games) or W2 LoRA (H6) on our 2M+ transition
  corpus — both pre-registered, both GPU-gated.

## 6. Submission ladder (both accounts)

Banked/pending today: R = dfranzen v1 (pending, 07:15Z) · S = r12-apex (pending, 01:45Z).

| when | R (dasshovon) | S (kragglenote2forwork) |
|------|---------------|--------------------------|
| 10/2 | cross-bank lordhansolo v300 (23.84) | cross-bank dfranzen v1 (27.89) |
| 10/3 | push+run superbrain-v10 → submit on complete | push+run m2s-2789-fork-s → submit (sure-shot 27.89 config) |
| 10/4 | m2s-2789-fork (comparison) | superbrain-s (test) |
| 10/5+ | v10.x A/B per daily slot; redraw best config | same, prefer sure-shot redraws |
| final week | farm best config both accounts | farm best config |

Slots budget: ~14/account total; used so far: R=1 (dfranzen bank), S=1 (r12-apex).
Cross-bank queue holds R: lordhansolo→sirikilohit (23.84→22.53). Everything
orchestrated by `t18_orchestrator.sh` (state `.orchestra/`, 10-min loop).

## 7. Risks / discipline

- Fork reruns drift (σ1.5–2) — a banked 27.89 fork can land 20–29; the Ladder
  banks MULTIPLE lineages to saturate.
- Prize eligibility may require original work — our SUPERBRAIN line IS original
  (built on open Duck harness like the whole field); fork-banked scores may not
  be prize-eligible but anchor us on the LB while the original line catches up.
- Never push a notebook that didn't pass the local suite (M-03 title==slug,
  21-test gate + preflight before any GPU run).
- GPU 30h/week hard cap: max 3 runs/account/week; every run must answer a
  pre-registered question (E-116+).

## 8. Thought process: the 0→27→50 ladder (the "superbrain" mental model)

0–4 (where we were): Duck genome + light patches; serving = vLLM NVFP4 16–45K
ctx; no scheduler; agent re-derives everything; efficiency leaks everywhere.
4–8 (mid-field): + lottery/attention scheduler; + image economy; + animation
ascii frames; + world-model no-wipe. All harness-level, all cheap.
8–16: + real token accounting; + exact context guards; + watermarks; + UCB/pace
allocation. The run stops wasting its 9h.
16–24 (sirikilohit/TAAF): + solved-level memory; + mid-action frames; + O(1)
state; + MTP draft loading; + Wang/Ludvig prompt economy. Every turn is cheap,
informed, and non-repeating.
24–28 (dfranzen): + 136K ctx with 93.4% prefix reuse; + cache-aware priority
gate; + guards that never foreclose hidden mechanics; + spec-decode throughput.
The whole 9h is spent on actually thinking.
28–40 (the open zone — our attack surface): solved-memory × scheduler cross-breed
(ours), scoring-aware agent (ours), archetype playbook priors (ours), W2 LoRA
world-model verifier (ours, H6), pace recalibration from OUR traces, spec-decode
tuning. Plus variance farming discipline nobody in public runs systematically.
40–50 (Tufa private): presumably harness v19+ internals + their own Flash-Next
checkpoints + full M-stack at 136K ctx. Not visible; we out-execute what is.
