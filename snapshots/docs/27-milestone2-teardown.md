# Milestone 2 Winner Teardown & LB Reassessment (2026-10-02)

Status: PUBLIC INTEL BOMB. This document consolidates everything published after the Milestone-2
deadline (2026-09-30) and re-derives our campaign strategy from it. All facts verified from
primary sources: winner write-ups (GitHub), winner notebooks (pulled via Kaggle API), live
leaderboard, and competition discussion threads. Artifact inventory in §9.

---

## 1. The situation has fundamentally changed

The leaderboard as of 2026-10-02 03:00 UTC:

| Rank | Team | Score | Submitted | Note |
|---|---|---|---|---|
| 1 | Tufa Labs | **52.51** | Oct 2 | Duck authors, new private work |
| 2 | Yi-Chia Chen | **48.07** | Oct 1 | likely a merge of the 3 winners + own work |
| 3 | gng | 34.77 | Oct 1 | |
| 4 | markintell | 34.21 | Oct 1 | |
| 5 | Rogers Johnson | 32.99 | Oct 1 | |
| 6 | cihan atak | **32.89** | Oct 1 | was 8.02 on Sep 30 — jumped via REAP-pruned stack |
| ... | 32 teams | ≥ 30 | Oct 1–2 | fork army |
| ... | 135 teams | ≥ 27.79 | Oct 1–2 | fork army |
| rank 10 | — | 31.60 | | top-10 line moved from 15.68 → 31.6 in 48h |
| rank 100 | — | 27.79 | | |
| us | 2 accounts | ~3.45 | Sep 19 | not in top 200 |

**What happened:** dfranzen open-sourced his 27.89 solution. Within 24h, hundreds forked it.
A single fork redraw landed at 31+ (user-reported "31 scored is public"; consistent with the
distribution below — forks span 20–34). The top-10 line is now ~31.6.

**Strategic consequence:** forking dfranzen is no longer medal-tier by itself (expected ~26,
rank ~100), but it remains our mandatory first move — it is the platform to build from, and
with redraw luck alone it can land 30+.

---

## 2. The variance law (most important number in this document)

Son Pham's analysis (discussion 745062) of hundreds of single-shot dfranzen copies:

- **Mean 25.77, σ = 3.93, Median 26.19** (distribution roughly 20–34)
- Because every fork got exactly ONE submission, this is a clean sampling distribution.
- **To be 90% sure an improvement is real you need ≥ +8 points** (single run vs single run).
- Same-code redraws: 14.5 → 22.5 (rellik13, KV-cache change confound), 5.02/5.50/6.42 triple
  (rellik13), 2.60 vs 1.45 identical builds (Makarov), 37 practice → 9.98 LB (rellik13).
- Cross-check with our own earlier evidence: #1 vs #2 same-family gap 27.89 vs 23.84 (σ≈1.5–2
  underestimated it; true σ≈4).

**Implications for us:**
1. Every submission is a lottery ticket with σ≈4 around our build's true mean.
2. Our resubmission policy: identical sureshot builds get resubmitted on consecutive days when
   we have nothing better — best-of-N redraws is free score.
3. Real signal needs multi-run verification; we must compare at matched generated tokens
   (rellik13's method), not wall time.
4. Never burn quota "testing" a change worth <8 points on a single run.

---

## 3. The three Milestone-2 winners — full teardown

All three: Tufa Duck harness (tool-agent with Python sandbox) + TAAF framework +
Qwen3.8-Flash-Next + speculative decoding (MTP). The differentiation was almost entirely
**inference engineering + context/scheduling policy + faithfulness of agent feedback**.

### 3.1 dfranzen — 27.89 (GitHub: da-fr/arc-agi-3-solution, notebook public)

Stack: SGLang Pennyroyal v2.5.3 + Intel W4A16 AutoRound main model (BF16 PLE kept) +
Albucino INT4 MTP draft (3 spec steps) + **FR-Spec 64k hot-token map** (verified in notebook
CFG: `FRSPEC=True`, `hot_tokens_64k.pt`), KV fp8_e4m3, SSM bf16, mamba radix `extra_buffer`,
ctx 139,264 server / 131,072 harness, mem-frac 0.96, chunked prefill 8192, maxreq 10,
temp 0.7 / top-p 0.95 / top-k 20, priority scheduling ON (all 110 games admitted, concurrency
gate 10, per-game cap 532 min), competition rerun budget 32,400 s (9 h).

The five pillars (from WRITEUP.md):
1. **Context economics** — calibrated text+image token estimation; trim hysteresis
   (128 Ki window → drain to ~57–59 Ki in ONE large block) so the prefix stays cache-hot;
   93.43% of prompt tokens served from cache; only 0.03% long-prompt cache misses.
2. **Compute allocation** — priority P = (A+B)·C: A ≈ immediate score gain with
   action-efficiency penalty (mirrors official scoring), B = continuation value (levels left:
   ≥3→8, 2→7, 1→5, 0→0), C = calibrated stall-falloff from 725 observed level attempts
   (Gaussian in actions a/115² and tokens t/62k²), B fades linearly in final 20% of runtime.
   Handover only at natural context-eviction points to preserve prefix cache.
3. **Perception** — image scale 4×→10× (biggest image win), frame_diff() object-level change
   descriptions, death-frame + diff-after-death, animation frames + timelines exposed as REPL
   variables (hint only when transient pixels exist). Animations = strongest perception win;
   tn36 unsolvable without them.
4. **Acting** — UNDO exposed (suspected very important on the competition set), executable
   guards: batch no-op stop, stale-state stop (from level 2), terminal-state stop;
   faithful per-action results, action echo, 3 Ki output budget with middle truncation.
5. **Memory/code** — Python function retention for the whole game (variables not retained);
   structured world model DISABLED entirely (conversation history beat it at 128 Ki context);
   summaries, resume-prompt tweaks, animation composite images, stronger verification hints,
   death ledgers, elaborate priority rules — ALL negative or neutral (see his §6).

Notable negatives (his §6, directly actionable for us): structured WM updates off; summaries
off; yielding by generated tokens (2048) not seconds; no prescriptive verification.

### 3.2 lordhansolo — 23.84 (notebook public, 17 KB launcher + private datasets)

Stack: vLLM 0.29.1rc1 nightly + own mixed NVFP4/FP8 checkpoint (built-in MTP head), ctx
147k/127k, KV fp8, 14 games live, 3,918 s cap per game, trim 126k→81,536 target, temp 0.6.
Patches: align-state retention (Mamba state reuse across turns), prompt-tail state caching,
mixed-checkpoint PLE safeguard, pinned-host embed_tokens. Harness: rewritten system prompt +
strategy-audit prompt after 25% game time used.

### 3.3 rellik13 (sirikilohit) — 22.53 (GitHub: LohitSiriki/arc-agi-3-milestone2-solution)

Stack: SGLang Pennyroyal v2.5.0 + Intel W4A16 + RadixArk FP8 PLE swap + NVFP4 MTP draft
(3 steps, draft-only shards loaded), fp8 KV with **48 GB hierarchical host-tier KV+Mamba**,
ctx 69,632, KV pool 1,004,288 tokens, 16 games live, temp 0.6.

His score ladder is the most instructive (solo, 44 submissions):
0.99 → 3.81 (Qwen3.8-Flash-Next switch) → 6.42 (SGLang over vLLM) → 7.14 (49k ctx, big-block
trims) → 9.96 (**solved-level rule memory pinned in prompt, +2.8 the ONLY text addition that
helped**) → 13.40 (Wang harness: stricter sandbox, object segmentation, code-first prompts)
→ 14.49 (fix lies: UNDO instead of ACTION7, "Level restarted." instead of "The game is over.",
removed "ignore the budget bar" line, animation frames) → **22.53 (fp8 KV → longer history,
NO prompt changes)**.

Key lessons from him:
- "At this context budget, the agent's own recent history is worth more than any instruction."
- Adding advice text DROPPED scores (6.42→4.16; 13.40→9.98) because instructions evicted
  agent's own evidence under tight context caps.
- Memory was the bottleneck, not throughput: KV pool 91–97% full all run, requests queued.
- FP8 KV was adopted late due to a confounded test (MXFP8 requant cost 25% decode speed, got
  blamed on fp8 KV). One-line settings can be worth +8.
- Failed: fresh-context restarts of stuck levels, temp 1.0, assumption ledger (never used),
  pruning 25% of experts (REAP-like — more room, worse play — but see cihanatak §5),
  higher-res images, Swift 1.5 fine-tune (35% slower).

### 3.4 cihanatak — 32.89 (the alternative stack that beats two of three winners)

Notebook teardown (pulled): vLLM 0.30.0 runtime + **REAP-k448 expert-pruned Flash-Next**
(boristown/qwen3-8-flash-next-nvfp4-reap-448e) + Swift1.5 hybrid layer + own evra/sheet
scheduler family (ctxfirst / failfast / combo variants), 48k ctx, b32 batch, per-game cap
7,920 s. REAP pruning trades expert capacity for KV/history room — and with the right
scheduler beat 23.84 and 22.53. rellik13's negative REAP result was pruning 25% (crude);
k448 targeted pruning + more history is a different regime. **Direction to watch: model
surgery + context economics beats raw model strength in this regime.**

### 3.5 Why Tufa is at 52.51

Tufa (Duck authors) did not share. Their forum post: they feared 4,000-copy lottery if they
shared; "It looks like Tufa Labs just found a big improvement ;)". 52.51 vs fork-army mean
25.77 = ~27 points of true engineering lead. What we know about their direction: nothing yet
(final solution promised after competition end). Expect Milestone-3 race at a 45+ baseline.

---

## 4. The "thought process" of the winners (reverse-engineered)

1. **Efficiency-first, not capability-first.** Nobody beat the model; they removed waste:
   cache misses, re-prefill, misleading feedback, dead actions, equal-time allocation.
2. **Memory over advice.** Every winner spent VRAM on agent's own history, not instructions.
   rellik13: instructions evict evidence; evidence beats advice.
3. **Faithful feedback loops.** Rename ACTION7→UNDO, "Level restarted." vs "The game is over.",
   death frames, per-action results, no-op guards — the harness must never lie to the model.
4. **Calibrate before you optimize.** dfranzen fitted C on 725 level attempts; rellik13 read
   server logs to find KV pool was the bottleneck; Makarov ran noise controls first.
5. **Isolate changes; assume nothing.** Every winner kept a "what didn't work" list. Single-run
   claims below noise are treated as unknown, not as failures or successes.
6. **The residual failure mode is in the model**: early goal commitment, defended against
   evidence (Makarov's state-alignment analysis: stuck runs had already tried the decisive
   action type; the loss is in which hypothesis gets committed, not in memory/coverage).
   Post-harness-tuning, the lever left is model-level (better goal judgement → final prize).

---

## 5. What this means for our campaign (updated plan)

Baseline decisions (effective immediately):
1. **Tonight (after 00:00 UTC Saturday quota reset):** auto-push already prepared:
   - kragglenote2forwork → dfranzen fork (sureshot; expected redraw ~26 ± 4)
   - dasshovon → dfranzen fork (second redraw sample; two lottery tickets on the platform)
   - Auto watcher `scripts/auto_push_submit.py` running: push → poll → submit pipeline.
2. **Both accounts' GPU quota is exhausted until Sat 00:00 UTC** — this week's earlier
   biohub/duck runs burned it. All GPU work must wait for reset. (Account note: the token we
   hold for "kraggleforwork" actually authenticates kragglenote2forwork; only two accounts are
   live: dasshovon + kragglenote2forwork.)
3. **Then: merge-and-raise ladder on dasshovon** (target ≥30, i.e. > fork mean + 1σ):
   - G1 candidate #1: dfranzen config + rellik13's solved-level rule pinning (his +2.8) and
     UNDO/level-restart fidelity already included in dfranzen patch — merge level-memory
     pinning into the harness patch.
   - G1 candidate #2: raise trim target (dfranzen drains to ~57–59k; rellik13 shows 45k
     retained works; with fp8 KV + host tier there may be room for 80k+ retained — the
     single biggest correlated score factor across all three winners is retained history).
   - G1 candidate #3: cihanatak-style REAP-k448 model swap (public model!) for more history
     per token, IF KV pool analysis shows we're memory-bound like rellik13 was.
4. **Every submission from now on targets ≥27** (per campaign directive); experimental runs
   below that bar go through demo-mode local verification first.
5. **Variance discipline:** claims <8 points = unresolved; resubmit identical builds to farm
   redraws on days without a candidate; compare runs at matched tokens.

Risks: fork submissions' prize eligibility (originality rule) — treat forks as baseline
platform, not as the prize path; the real prize path is the merge + novel layer on top.
Milestone-3 will likely reset the race at a higher bar (Tufa final release).

---

## 6. Discussion-mined plans (what the crowd will do next)

From threads 745062 (variance), 742801 (no-OSS), 743723 (harness experiments), 743952
(unpopular opinion), plus the comparison thread's comments:
- **Everyone will fork-and-merge the three winners** (Yi-Chia Chen publicly encouraged it).
  Expect top-10 line ≥35 within 2 weeks. Our merge must land FAST (next week) to matter.
- Commenters' identified gaps: fp8 vs nvfp4 KV ablation (xz), concurrency-vs-context
  tradeoff (rellik13 got it wrong until logs said otherwise), harness-vs-model blame
  (Makarov: model-side goal judgement is the residual), "wait for Qwen4" (parthenos).
- Scott Le Grand: coding agents were useless for vllm/sglang debugging — inference work needs
  direct human targeting; we should point agents at *specific* patches, not "optimize TPS".
- Son Pham: REAP-style model surgery is "an entire untapped area".
- Next-phase focus predictions: harness > serving (both converge), model swap (Qwen4) if
  released, and training for goal judgement (Tufa's likely edge).

---

## 7. Kaggle API operational notes (for future sessions)

- CLI 2.2.4 with `KAGGLE_API_TOKEN=<KGAT>` env var works (bearer); v1 basic auth does NOT.
- `kaggle kernels pull/list/status/push`, `kaggle competitions submit -k <owner/slug> -v N`
  works for code competitions (full automation possible).
- kernels/list bestScore field is 0 for code comps — use `competitions leaderboard` for scores.
- Account↔token map (see .env): KAGGLE_TOKEN→dasshovon; KAGGLE_TOKEN_B→kragglenote2forwork
  (NOT kraggleforwork); KAGGLE_TOKEN_C→kragglenote2forwork (older token, same account).
- GPU quota 30 h/week/account, resets Sat 00:00 UTC. Push fails with "Maximum weekly GPU
  quota" when exhausted (409 Conflict otherwise possible on slug/owner mismatch).
- Weekly quota is the binding constraint: one competition rerun ≈ 3 h notebook wall time but
  quota burn is per-session; plan ≤ ~8 full reruns/week/account.

## 8. Actionable config for our first merge (draft, pre-registration in REGISTER.md)

Base: dfranzen notebook (all datasets/models public). Change set for v1-merge (dasshovon):
1. Add solved-level rule pinning block to system prompt (rellik13 cells/35 pattern — his
   `cells/` dir has every cell as .py: port `35_...` trim cell + level-memory rules).
2. Keep dfranzen trim policy; test trim drain 59k → 72k (single knob, +history regime).
3. Optional: swap draft to RadixArk NVFP4 MTP (keithtyser mirror) if draft KV savings matter.
4. Demo-mode gate: run 25 public games 20 min; require ≥ median of our baseline demo runs
   before burning a submission slot.

## 9. Artifact inventory (saved locally, anti-deletion complete)

```
references/milestone2/
├── da-fr-arc-agi-3-solution/        # FULL clone: WRITEUP.md, ARC3-Inference, serving/, TAAF
├── lohitsiriki-milestone2-solution/ # FULL clone: WRITEUP.md, cells/ (every cell as .py),
│                                    #   run/ (real run outputs: logs, scheduler events, transcripts)
├── notebooks/                        # 16 kernel sources pulled via API (.ipynb + meta):
│   dfranzen (27.89), fantasy0312 + amatlas (identical forks), lordhansolo (23.84),
│   sirikilohit (22.53), richardcsaky (20.00), cihanatak (32.89 stack), scottlegrand,
│   shiiin9 ×2, amanatar, matthewblakeward, chiakazirim, wuliao0, samrishb, tantan0327
├── fork-kfw/, fork-dshv/             # ready-to-push fork packages (metadata + ipynb)
research/
├── lb_full_200.csv, kern_list_top50.json, lb_now.json
├── kaggle_745062.txt (variance), kaggle_742801.txt (no-OSS), kaggle_743723_pr.json
│   (harness experiments), disc_list_jina.txt, kaggle_738602.txt
scripts/auto_push_submit.py          # push→poll→submit watcher (running)
```

The pull script `scripts/pull_milestone2_kernels.py` re-downloads everything in one command.
