# docs/23 — The >5 Wave: Deep Analysis of Recent Public Notebooks (2026-09-30)

Task 15 · Sources pulled from Kaggle into `notebook-intel/` (9 notebooks, code extracted; Affectify blobs decoded)

## 1. The family tree (who scores what and why)

```
Tufa Labs Duck harness (June-30 milestone 1.21, jeroencottaar public copy)
 └─ keithtyser fork: "Duck Qwen3.8 Flash Next NVFP4 MTP"
     serving swap → RadixArk/Qwen3.8-Flash-Next-NVFP4, ModelOpt NVFP4/BF16,
     async sched + chunked prefill + 3-token NEXTN MTP, 32K ctx, 8K batch cap,
     8 vLLM sequences, CUDA graphs, no prefix-cache, no logs; Duck keeps 28-way
     ├─ chiakazirim "Duck Qwen3.8 (Tuned)" ............ 4.50
     ├─ Duck Qwen3.8 Anim Base family ................. 4.09–4.33
     ├─ scottlegrand "taaf-flashnext-sheetu12b-0922" .. 5.19  ← TAAF bundle (closed dataset)
     │    └─ shiiin9 "TAAF KV6B" (+ Affectify cell, KV 5→6 GiB) 5.18
     ├─ shiiin9 "ARC3 Duck plus ours A" (+ scheduler v1) ....... 5.68  (same code: 5.68/4.09/2.30)
     ├─ shiiin9 "ARC3 Duck plus ours" (+ scheduler refined) .... 5.75  ★ public best
     └─ shiiin9 "ARC3 Attention Lottery" (+ img/labels exps) ... 4.69
Others: CassowaryLoRaFoRgE (Qwen3.8-27B-ARC918-LoRA + same-game TTT) 4.08 ·
Hybrid REPL Agent 4.08 · Duck Qwen3.8 (Tuned) 4.50
```

**Single decisive delta: Affectify's "lottery scheduler" cell (くじ引き) = +1.5–1.7 LB on an identical base** (4.09→5.68/5.75). Everything else in the >5 wave is that cell plus serving polish.

## 2. What the 5.75 notebook actually adds (decoded, cell 17 = 58.9K chars + 2 base64 blobs)

Their design contract: *every change is one extra cell on Duck's Customization hook; module attributes swapped, never the 15MB bundle.* All switches are `OURS_*` env vars read **inside functions at runtime** (they hit 4 init-order bugs before this).

### 2.1 The attention scheduler (the core)

**Diagnosis (verified against Duck `solver.py:246`):** Duck allocates game-time **progress-independently and equally**. `should_stop()` has only 4 stop conditions, none of which is "not making progress". A zero-point game burns its full 7920 s; a game that cleared L1 at minute 100 has only 32 min left for L2+. With **triangular scoring** (level i worth `i/(N(N+1)/2)` of the game — confirmed in their injected FACTS blob, matches our LB weighting hypothesis), deep games are starved exactly when their next level is worth the most.

**Fix:** keep all games alive (they're all `start_game`'d up front — the semaphore gates *thinking*, not *opening environments*), and raffle the "right to think next":
- **Tickets** = `base + level^pow` with `pow=2` (EXP-100: beats linear), `base=0.2`
- **Stall decay**: after **knee=80 actions** on a level, breakthrough probability **collapses 61% → 14%** (EXP-106, 298 challenge records); decay `stall_factor2` with **halflife 40**, floor 0.1; knee scales with level (slope option) because breakthrough p90 = **L1:51 / L2:72 / L3:78 / L4+:132 actions** (EXP-106, 365 records). A uniform knee of 80 is *late* for L1 and *early* for L4+.
- **Value correction (OURS_VALUE=1)**: next-level worth is ∝ level (triangular), **not** level²; N differs per game. Without it the scheduler gives **3.7× more tickets to the lower-value game** (10 tickets to L2→L3 of a 6-level game worth 14.29 pts vs 37 tickets to L5→L6 of a 10-level game worth 10.91 pts).
- **Annealing the raffle sharpness**: `p(u)=p0+(p1−p0)·u^k`, `base(u)=base0·(1−u^k)` with K=3, P0=0.4, P1=1.9 — early-run rankings are pure noise (games at ~8 turns; EXP-099 cd82@23 / wa30@21 / dc22@17 late bloomers), so start wide, sharpen late.
- Scheduler width 8; dropping a game from the pool ≠ killing it (`analyzer` and `_history_messages` stay alive; EXP-099 §9.2's −4.20 cannot happen).

### 2.2 Token economy (their second big win — mirrors our docs/15 thesis)

- **EXP-099 (25-game controlled experiment)**: +1,735 chars of system prompt → +688 chars generation/turn → **turns −13% in 25/25 games**, levels 39→30. **Everything ends in time-out; turns = distance.** Prompt bytes are the budget.
- **Thinking mode OFF** (`chat_template_kwargs={"enable_thinking": false}`).
- **Context window 32K→16K**: concurrency = KV tokens ÷ ctx len (125,898 / 32,768 = 3.84×; at 16,384 = 7.68× → **+100% concurrent decodes at zero GPU cost**, no OOM risk). Measured input 20,937 tok → needs dedup first.
- **USER-boilerplate dedup**: **25.1% of input tokens are byte-identical repeats**; ~8M tokens/run on zero-information bytes. Dropping all but the last USER turn: 20,937 → 15,813 (−24.5%) → 16K fits. (Caution learned: EXP-099 §9.2 full history wipe = −4.20, p=0.032 — they keep the contract on the active turn.)
- **Keep-reasoning trim** to last N turns; keep world-model notes on death.
- **`changed_cells(before, after)` tool** (stdlib-only, injected into Duck's python sandbox — which hides raw grids, allows 15 stdlib modules, 30 s/call): replaces the model's hand-written diff loops. Tool ablation across 25 public games: kept only changed_cells (106 calls/14 games); hud_note/hud_cells/click_candidates deleted (84% of games are click-type and click_candidates was **never called**).

### 2.3 Scoring-awareness injection (cheap and powerful)

Their FACTS blob tells the model things the harness never states:
> *"A game's levels carry TRIANGULAR weights: level i is worth i/(N(N+1)/2)... Level 3 is worth 3× level 1... **reaching one level deeper is by far the largest gain available to you**."*

### 2.4 Rehearsal & ops

25 clone environments for offline rehearsal before submission; watchdog on the owned vLLM server (restart after 4 consecutive `/v1/models` failures, max 2 restarts); report every 600 s.

### 2.5 The meta-game: variance farming

**Their own words: "the same code scored 5.68, 4.09 and 2.30."** Identical code, σ≈1.5. The raffle is stochastic → each submission is a draw. Resubmitting identical finals and keeping the best is worth more than most code changes. (This also explains "Attention Lottery" 4.69 with near-identical config + an images/labels/upscale experiment that didn't pay.)

## 3. Scott Le Grand's TAAF line (5.19) and KV6B (5.18)

- TAAF's solver ships as a **closed dataset bundle** (not readable); notebook-level deltas are serving-only on the same keithtyser base: profile `kv5-bf16-mtp3-c16-cg32-ctx16k` (5 GiB KV reservation, bf16 KV, MTP3, 16 concurrency, cudagraph 32, 16K ctx).
- **KV6B = bump KV reservation 5→6 GiB**: vLLM log showed "≈3.21× concurrent-decode at 5.0 GiB (105,202 token KV cache, 24 requests queued, 100% usage); raising reservation should raise concurrency ~proportionally". With Affectify's scheduler on top: 5.11–5.18.
- Our docs/17 KV-collapse diagnosis is independently confirmed by their numbers (KV tokens = concurrency ceiling).

## 4. The also-rans (what does NOT beat the scheduler family)

| Notebook | Score | Approach | Lesson |
|---|---|---|---|
| CassowaryLoRaFoRgE v17 | 4.08 | Qwen3.8-27B-FP8 + **ARC918 LoRA** + same-game **TTT** + RHAE baselines + synthetic causal pretraining | LoRA/TTT pipelines alone don't beat serving+allocation discipline; but ARC918-LoRA + TTT are reusable components |
| Hybrid REPL Agent | 4.08 | REPL/code-execution agent | below family |
| Duck Qwen3.8 (Tuned) | 4.50 | prompt tuning on duck | below |
| Anim Base family | 4.09–4.33 | duck variants | below |
| Attention Lottery | 4.69 | scheduler + images/labels/upscale experiments | the img experiments did not pay (or a bad draw) |

## 5. Synthesis — the five confirmed laws of this competition (now all independently verified)

1. **Turns are the budget** — everything ends in time-out; turns = levels reached (EXP-099).
2. **Prompt/generation bytes buy turns** — +1.7K prompt chars = −13% turns (25/25 games).
3. **Score is triangular in level index** — depth beats breadth; per-game N matters (confirmed in their FACTS + matches LB behavior).
4. **KV tokens = concurrency = actions/hour** — 5→6 GiB KV ≈ proportional concurrency (KV6B); ctx 32K→16K doubles decodes free (Affectify).
5. **Allocation is worth +1.5–1.7 LB** — a better raffle over the same solver is the largest public single-mechanism gain on record; and σ≈1.5 between identical runs makes best-of-N draws a real strategy.
