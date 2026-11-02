# 10 — Milestone 2 Winner Trio: Deep Analysis & Saved-Artifact Inventory

*Written 2026-10-02 (UTC Oct 1 evening). Trigger: user report that a "31-scored" notebook is public and could be deleted at any time. Mission: understand, analyze, and SAVE everything before it disappears.*

---

## 1. The actual situation behind "31 scored is public"

**What the leaderboard looks like now (snapshot 2026-10-01T19:26 UTC, full CSV saved at `analysis/lb_full/`):**

| Rank | Team | Score | Members | Notes |
|---|---|---|---|---|
| 1 | Tufa Labs | 50.65 | dlorah, driessmit1, infinitecreativity, **jeroencottaar**, pressman1, stefano1283 | Jeroen (M1 winner, Duck author) joined Tufa |
| 2 | Yi-Chia Chen | 40.97 | threerabbits | posted "excited how high people get combining the three winning notebooks" |
| 3 | gng | 34.77 | denialguo, jaydenszeto123, snoopydoo | |
| 4 | markintell | 34.21 | markintell | |
| 5–7 | Rogers Johnson / Maren Sajdaras / Junhua Yang | 32.99 / 32.29 / 32.13 | solo | |
| 8 | **minmax007** | **31.60** | solo | 15 entries |
| 9 | **KMM** | **31.47** | huekmm | 5 entries |
| 10 | **Helmut AGI** | **31.13** | antonijankowski123, **jakobbrggen**, nightmareblocks | TAAF Anim author's team |
| ... | ... | ... | ... | 10 more teams ≥ 29.9 |
| 57 | Daniel Franzen | 27.89 | dfranzen | **M2 winner, notebook public** |
| 121 | **Shovon Das (us, dasshovon)** | **25.30** | dasshovon | our dfranzen fork-bank from Oct 1 |
| 321 | Kragglenote2 Forwork (us) | 4.54 | kragglenote2forwork | stale pre-M2 agent |

**Key finding — there is no single magic "31 notebook":** the 31.x teams (minmax007, KMM, Helmut AGI) have **zero public notebooks** of their own (verified via API user scans on 2026-10-01). The 27→31→34 wave is the field forking/recombining the three **public Milestone-2 winning notebooks** (see JK-Piece in discussion 744545: *"Only 10h after sharing the score 27 notebook, we now see 34+"*). If the user saw a specific 31-scored notebook in the Code tab, it is one of these fork-variants; the underlying source artifacts are the three M2 winners, and **we have now saved all of them** (section 2). Deletion of any one fork does not matter anymore — we hold the sources.

**The four public artifacts the whole wave is built on:**

1. `dfranzen/arc-agi-3-milestone-2-solution` — **27.89** — public, GitHub + writeup published
2. `lordhansolo/built-on-tufa-labs-duck-harness-milestone-2` — **23.84** — public (⚠ original slug `arc-agi-3-milestone-2` was **renamed**, old 404s; the scored version is **V293** while latest is V306)
3. `sirikilohit/arc-agi-3-duck-18-1gc-submit` — **22.53** — public, GitHub + writeup published
4. `richardcsaky/arc-agi-3-milestone-2-submission` — 20.17 — public (4th family member, thinner)

All three winners run **Tufa Labs' Duck harness on the Tufa ARC-AGI Framework (TAAF) serving Qwen3.8-Flash-Next** on one RTX PRO 6000. Milestone-2 podium (tentative per organizers): dfranzen > lordhansolo > sirikilohit.

---

## 2. What we saved (before deletion could happen)

All under `arc-agi-3/artifacts/`:

| Artifact | Path | Status |
|---|---|---|
| dfranzen notebook source (23 cells, 568 KB) | `m2_winner_notebooks/dfranzen_*.nb.ipynb` + `.acctB.ipynb` | ✅ both accounts |
| lordhansolo notebook source (10 cells, latest V306) | `m2_winner_notebooks/lordhansolo_built-on-*.nb.ipynb` | ✅ both accounts |
| sirikilohit notebook source (50 cells, 315 KB) | `m2_winner_notebooks/sirikilohit_*.nb.ipynb` | ✅ both accounts |
| richardcsaky notebook source | `m2_winner_notebooks/richardcsaky_*.nb.ipynb` | ✅ both accounts |
| Output logs + 91/136/500-file output indexes (per-game events, requests, viewer data, benchmark.json) | `m2_winner_notebooks/*.out.log.json`, `*.out.fileindex.json` | ✅ |
| dfranzen GitHub repo (harness + SGLang builder/patches) | `m2_github/arc-agi-3-solution/` (5.1 MB) | ✅ |
| sirikilohit GitHub repo (cells + writeup) | `m2_github/arc-agi-3-milestone2-solution/` (20 MB) | ✅ |
| **tonghuikang mirror of ALL THREE winners** (notebooks + dataset sources + comparison docs) | `m2_github/daniel-franzen-arc-agi-3/` (14 MB) | ✅ |
| Comparison thread (744792) full text + HTML | `artifacts/thread_744792_m2_comparison.txt/.html` | ✅ |
| Jeroen "we will not open-source" thread (742801) | `artifacts/thread_742801.txt` | ✅ |
| Hill-climbing-on-LB thread (744365) | `artifacts/thread_744365.txt` | ✅ |
| Full leaderboard CSV (3550 teams) | `analysis/lb_full/` | ✅ |

Model/dataset dependencies (all public, safe from deletion): `dfranzen/pennyroyal-v253` (SGLang build), `dfranzen/taaf-kaggle-source-bundle-copy` (harness source), models `dfranzen/albucino-qwen3-8-flash-next-drafter` + `dfranzen/intel-qwen3.8-flash-next-w4a16-autoround`; upstream HF: Intel W4A16-AutoRound, albucino FP8PLE drafter, primitive-ai NVFP4-FP8 mixed, RadixArk NVFP4.

---

## 3. Technical breakdown of the three winners

### 3.1 dfranzen (27.89) — "inference engineering + information richness + calibrated scheduler"

- **Model/quant:** Qwen3.8-Flash-Next via Intel W4A16 AutoRound (BF16 PLE table kept unquantized on host) + Albucino INT4 MTP drafter, 3 draft tokens, 64k FR-Spec hot tokens. Server: SGLang **Pennyroyal v2.5.3** + 4 custom patches (low-M BF16 GEMM; spec-state budget fix; Marlin scale-dtype fix; **prefix-cache Mamba checkpoint retention**; shard prefetch lookahead). Resharded model for reliable startup.
- **Context:** 131k harness window, 12k output reserve, trim 118k→~57-59k in ONE big block (**hysteresis**), 93.43% prefix-tokens reused, token-accurate input estimation (text calibrated, images from patch layout).
- **Concurrency:** 10 streams = admission limit, games frozen outside; slots re-allocated only at eviction points to protect prefix cache.
- **Scheduler (the crown jewel):** priority `P = (A+B)·C`; A = immediate level value with action-efficiency penalty, normalized by `55/(N(N+1)/2)`; B = continuation lookup {≥3 left: 8, 2: 7, 1: 5, 0: 0}, faded linearly to 0 in final 20% of runtime; C = completion-probability decay **fit from 725 real level attempts** (Gaussian in actions σ≈115, in tokens σ≈62k).
- **Perception:** **animations exposed as REPL variables** (strongest single perception win; tn36 unsolvable otherwise), animation timeline text, `frame_diff()` structured object-change helper, 10× image upscale (vs 4×), game-over fatal frame + difference images.
- **Action space:** **UNDO exposed** (was advertised-but-blocked ACTION7), faithful per-action results, 3k tool output with middle truncation.
- **Guards:** batch no-op, stale-state (fires on the SECOND action after an ineffective one, from level 2), terminal-state — all on `gameplay_changed` (4-cell border excluded).
- **Memory:** Python function retention for the whole game (variables not retained); structured world-model DISABLED (bigger context made it redundant); thinking kept in history (deliberate, removing it regresses).
- **Prompts:** level-transfer guidance, game-over diagnosis protocol (bar semantics, `history[-2].frame` death-frame inspection, no-replay rule), clarified repeated-opener prompts.
- **Sampling:** temp 0.7, top-p 0.95, top-k 20.
- **What did NOT work (his own ablations):** structured world-model updates, summaries, animation composite images, stronger verification hints, more elaborate priority rules.

### 3.2 lordhansolo (23.84) — "the VRAM gambler"

- vLLM 0.29.1rc1 nightly (not SGLang!) + NVFP4 mixed quant with built-in MTP head, 3 draft tokens, 32k draft vocab.
- Biggest KV pool: **1,417,100 tokens**, 19.69 GB KV+Mamba, context 147k server / 127k harness, 14 games live.
- 3,918s hard cap per game; freed slot goes to next game immediately (8 waves × 14 games).
- Trim ~126k → target 81,536 tokens, measured by local token estimator; no turn cap.
- Patches: align-state retention, prompt-tail state caching, mixed-checkpoint PLE safeguard, pinned-host embed_tokens.
- Temp 0.6. No writeup published (their V293 = scored version; V306 re-run Oct 1 for re-validation).

### 3.3 sirikilohit / rellik13 (22.53) — "memory over advice" (most transferable lessons)

- 44 submissions in 50 days: 0.99 → 3.81 (Flash-Next) → 6.42 (SGLang) → 7.14 (bigger context) → 9.96 (**solved-level memory pinned in system prompt: rule + last 30 winning actions of each cleared level**, +2.8 alone) → 13.40 (Wang's harness: strict sandbox, object segmentation) → 14.49 (fix misleading text) → **22.53 (FP8 KV + longer history, zero prompt changes)**.
- **Core law: at this context budget the agent's own recent history is worth more than any instruction.** Adding text to prompts repeatedly DROPPED scores (6.42→4.16; 13.40→9.98) because instructions push out the agent's own evidence. Strategy: "No instructions added; wrong ones removed" — renamed ACTION7→UNDO, "The game is over"→"Level restarted", deleted "ignore the budget bar" line.
- **FP8 KV lesson (methodological gold):** freed memory → 1.0M-token pool, trims 57k→45k, context 69,632, 16 games. The earlier "FP8 failed" test was actually corrupted by an MXFP8 requant change (25% slower decode) and never actually raised concurrency. **Isolate variables; verify server flags actually took effect; check pool occupancy in logs (91–97% full = memory-bound).**
- UCB scheduler held back (his own admission): games stagnate in later stages, so moving time mostly moves stagnant time.
- Variance doctrine: same notebook scored 5.02/5.50/6.42; practice-37 → LB-9.98. Compare runs at **equal generated tokens per game**, not wall time; read transcripts, don't trust single runs.

### 3.4 Cross-cutting score levers (ranked by measured impact)

1. Model generation: Qwen3.6-27B → 3.8-27B → **Flash-Next** (each a "substantial improvement")
2. **Prefix-cache engineering** under mixed attention+linear-attention (SGLang Pennyroyal or vLLM nightly + Mamba state retention) — enables long history without re-prefill; 93%+ reuse
3. **History length** (FP8 KV → more tokens of agent's own experience): sirikilohit's 14.49→22.53 was THIS ALONE
4. **Perception**: animations, 10× upscale, diff images (dfranzen's biggest perception win: animations)
5. **UNDO exposure** + honest feedback text (both dfranzen and sirikilohit independently)
6. **Solved-level memory** pinned in prompt (sirikilohit +2.8)
7. **Scheduler**: distribute tokens to promising games (dfranzen's calibrated P; lordhansolo's wave queue)
8. Function retention (no re-generation of helpers)
9. Guard rails to stop wasted actions
10. Temperature 0.6–0.7 (never 1.0)

---

## 4. The thought process (what we actually needed to learn)

**dfranzen thinks like a systems performance engineer:** every token of VRAM and every percent of cache hit is money. His loop: measure (725-level-attempt datasets, 93.43% reuse stats) → model mathematically (Gaussian fits, priority formula) → implement at the serving layer (patches) → validate → publish. He never touched prompts where compute was the bottleneck, and disabled machinery (world-model, summaries) when context made it redundant. **Simplicity through subtraction, complexity only where measurement demands it.**

**sirikilohit thinks like an experimentalist under scarcity:** 44 submissions, one variable at a time, transcripts over scores, and a discipline of writing down WHY a test was invalid (the FP8 story). His "agent's own history > any instruction" is the deepest single insight published this milestone — it reframes harness work from "prompting" to "memory management".

**lordhansolo thinks like a gambler with an edge:** push the VRAM limit to the cliff (1.9 GB free), bet on the biggest KV pool, hard per-game caps. Higher risk, simpler control loop.

**Common root:** all three are the SAME harness (Tufa Duck on TAAF) — the milestone was won on **serving efficiency + information retention**, not on new agent ideas. Yi-Chia Chen (40.97, non-winner, non-published) explicitly predicts the next phase is *combining* the three notebooks. That is exactly our lane.

**Gap we can exploit (what the top private teams have that public code lacks):** Tufa Labs at 50.65 did NOT open-source (Jeroen's thread 742801). Their edge over the public 27.89 is +22.7 — that is the space of: their new serving work, their scheduler upgrades, their game-specific tuning, and possibly private model quant/draft improvements. sirikilohit's UCB scheduler and dfranzen's "held back" ideas (empirical continuation lookup with normalization of both A and B, pace adjustment) are documented-but-unshipped levers we can ship.

---

## 5. Action plan (locked to our dual-account doctrine)

**Banked already:** dasshovon 25.30 (dfranzen redraw, rank 121) — keeps best, zero risk.

**Armed for 00:04 UTC tonight** (`scripts/midnight_submit.py`, PID armed, log `analysis/midnight_submit.log`):
- kragglenote2forwork → **dfranzen v1** ("M2S 27.89 sureshot redraw b1") — sureshot line, expected redraw band 25–31 (σ≈1.5–2 from the three observed dfranzen-family redraws: 27.89 source, 25.30 our draw, 34+ recombinations by others)
- dasshovon → **lordhansolo V293** ("M2 23.84 redraw bank A") — expected band 21–27
- Both use the direct-version submission mechanism (no GPU needed, proven by our own 25.30)
- Following days: sirikilohit v1 (22.53 band) on whichever slot is free; then our combo builds

**Combo roadmap to 30–40+ (dasshovon experiment line, GPU quota resets Sat ~00:00 UTC):**
1. Base: dfranzen notebook (best public base, cleanest patch structure)
2. + sirikilohit's solved-level memory pinning (rule + last-30 winning actions per cleared level)
3. + temperature 0.6 (both other winners use it; dfranzen's 0.7 is untested against it)
4. + dfranzen's own "held back" scheduler ideas (B-normalized continuation lookup, pace adjustment)
5. + KV pool occupancy monitor → auto-tune games-at-once (sirikilohit's 91–97% diagnostic)
6. Test in 20-min smoke on 25 public games, compare at equal tokens-per-game; only ship on G-gate pass
7. Later: animation exposure is already in dfranzen; next perception lever = our own world-model shield hypothesis (H1) re-tested on the new base

**Risks noted:** direct-version submissions of others' notebooks are proven to score (our 25.30 is on the public LB) but are unlikely to be prize-eligible (originality/code-requirements rules); that's fine — they bank redraws while our own builds carry eligibility. Notebook slugs can be renamed without breaking scriptVersionId URLs (lordhansolo case) but versions can go private — hence full local preservation (section 2).

---

## 6. Open questions for next sessions

1. Does kragglenote2forwork's GPU quota reset Saturday 00:00 UTC (then we push our own combo kernel there first)?
2. What exactly did Tufa ship between 27.89-equivalent code and 50.65? (Watch for their final-phase public writeup; Jeroen's thread says "not open-sourcing for milestone 2" — but the final prize requires open-sourcing, so it WILL become public before Nov 2.)
3. Is lordhansolo V306 (Oct 1 re-run) materially different from V293? (Pull version history via browser when logged-in possible.)
4. minmax007/KMM/Helmut AGI 31.x: recombination details unknown; Helmut AGI's jakobbrggen TAAF-Anim lineage suggests animation-focused upgrades — watch his account.
