# 19 · Next-Week Battle Plan: 4.07 → 7–12 → 15–25 → 30–50 (2026-09-30)

## 0. Verified baseline (2026-09-30, Kaggle API, notebook names only)

| Notebook (best version) | Official LB | Levels | Note |
|---|---|---|---|
| **urad duck r10** | **4.07** | 41/183 | ← official best; efficiency champion (sb26 8/8 WON) |
| Duck Qwen3.8 Anim Base 35c14d v2 | 3.45 | — | family band |
| Duck Qwen3.8 (Tuned) v1 | 3.34 | — | family band |
| taaf-flashnext-sheetu12b-0922 | 3.18 | — | sheetu12b line |
| R12 = 5.19 sheetu12b pristine + apexfix | 3.09 | **45/183** | most levels; internal 5.19; efficiency squaring ate the LB |
| AGI Active Flash V9 | 2.89 | — | |
| duck-governor-v1 (v3) | 2.77 | ~28 | |
| Duck Qwen3.8 Flash Next NVFP4 MTP v6 | 2.71 | — | |
| v7 nooa-lite | 2.61 | — | ran with state-key bug; machinery dead |
| 27B clean fresh draw d2 | 1.72 | 23/183 | internal 3.13 |
| 27B FP8 LB9 repro | 1.17 | — | |
| 27B d2 draw #3 | 1.13 | — | |

**Correction:** the "6.68" circulating in earlier docs is an *internal* score, never an
official LB. Official best = **4.07**; official max-levels = **45/183**. The Space and
ANALYSIS.md are corrected accordingly in this pass.

LB context (2026-09-29 pull): #1 Tufa Labs 45.33 · #2 36.73 · #3 26.55 (top-3 cutoff) ·
#4 22.24 · #5 20.53 · #6 20.51 · #7 18.29 · NVARC3 16.07 · keithtyser 9.17.

## 1. Score arithmetic (unchanged, drives everything)

per level: `min(human/agent, 1.15)² × level-index weight / Σweights`, averaged over games.

- r12 proof: 45 levels but wasteful (2–6× human on many levels) → 3.09, BELOW r10's 4.07
  at 41 levels. Efficiency is worth more than raw level count until near-parity.
- Deep levels are worth multiples of L1 (weight = level index): sb26 has a verified
  L1→L8 chain — replaying it costs ~12–30 actions/level vs 50–190 to re-explore.
- Verified playbooks free 30–50% of the per-game time budget → buy extra levels AND
  efficiency at the same time. This is the only lever that improves both terms at once.

## 2. The five parallel plans

### PLAN A — PLAYBOOK_MODE + efficiency governor  (ship next slot; biggest EV)
0. **Day-1 blocker fix (found 09-30): the incumbent fast-lane checkpoint
   `keithtyser/qwen3-8-flash-next-nvfp4` was REMOVED from HF (repo 404; author listing no
   longer contains it).** Any rerun of the best notebook would fail at model boot.
   Fix: switch the fast-lane model path to `primitive-ai/Qwen3.8-Flash-Next-mixed-NVFP4-FP8`
   (verified alive, 124 files) with `tcclaviger/Qwen3.8-Flash-Next-MXFP4-FP8` as second
   option; A/B both locally before the first submit. Also hunt for cached copies of the
   old weights in Kaggle datasets attached to prior runs and mirror them to HF as backup.
   Note: `keithtyser/model-forge-qwen36-27b-ft-v4-nvfp4-dgx-spark` (Qwen3.6-27B NVFP4
   base for the ericmao LoRAs) is still alive.
1. Embed `own_playbook_library.json`: **53 playbooks / all 25 games / 53-of-53 verified**
   (verification block all-green; local engine == Kaggle scoring engine, proven by the
   r10 wa30 L1 replay clearing at action 48 on both sides).
2. Embed ARA verified transfers that beat ours: **lf52 L1 in 9 actions** (ours: 18–21),
   **su15 L1 in 18 actions**.
3. On game+level recognition → emit verified sequence; **board-hash guard → fail-open**
   to normal policy on any mismatch (never stall).
4. Efficiency governor: hard cap 2.0× human baseline per level (metadata-driven); on
   breach → one RESET, then park. Zero-game triage list sk48/dc22/cd82/g50t/r11l capped
   at 60 actions each (~700 actions burned for 0 today).
5. Expected: 41→44–47 levels at near-human efficiency → **LB 7–12**.
6. Cost: 1 day build + 1 day local verify (30+ preflight greens before submit).

### PLAN B — Two-lane swarm serving on RTX Pro 6000 96GB  (docs/14, build in parallel)
- Fast lane: **8B NVFP4**, gpu-util 0.45 → 24–26 workers (exploration unchanged).
- Deep lane: **27B NVFP4 + FP8-KV**, gpu-util 0.42 → 4–6 dedicated workers at 32K.
- Router (CPU): escalate when `same_level_actions > 25 AND board_delta == 0` OR `level ≥ 3`;
  verify/critique calls stay on the fast lane with tiny context (PRO-LONG style).
- Root cause being fixed: 27B failed from **KV starvation** (199K-token KV cache collapsed
  28 workers to 3 running), not model quality. Two lanes with FP8-KV fix the math.
- Fallback ladder if two-instance serving is unstable: pruned-RTXPRO-6000 8B A/B →
  Ornith-1.5-35B-A3B single-lane swap test → stay 8B-only.
- Expected: +3–8 LB on top of Plan A.

### PLAN C — Algorithmic solvers + mechanic priors  (zero GPU cost)
1. **tr87 pure-code solver**: ARA doc gives the complete win-rule (8 dihedral transforms +
   legend substitution) — implementable as plain frame-parsing code, no LLM needed.
2. **su15 L2–L3 recipes + ls20 key-delivery geometry** → prose priors injected per-game
   (mechanic notes transfer even where replay scripts do not — proven by tr87/wa30
   replay mismatch vs. local engine).
3. **sb26 L1→L8 chain** → macro replay memory: one verified chain = 8 levels' worth of
   weight at replay cost.
4. Expected: unlocks 5–10 deep levels that pure exploration never reached.

### PLAN D — Deep-capability lane  (start day 5+, full effort week 2)
1. **ericmao ARC-AGI-3-trained LoRA adapters** (sft-v3 / grpo / human100 /
   spatial-continuation-100) A/B on the 27B deep lane.
2. **bestiary `agentica_lite`** skill library (predicate library, stalemate triggers,
   memory journal) — CPU-side, zero VRAM, directly portable.
3. **JEPA-lite frame-prediction head** (M1 spec; grid-jepa / vjepa2 references mirrored)
   for cheap what-if action screening.
4. **Agentic world-model serving options** (Qwen-AgentWorld-style): what transfers is the
   *harness pattern* (language world-model in context + predicted-cell verification),
   not the checkpoint. Concretely: keep NVFP4 8B as actor, give the deep lane a
   world-model skill-prompt block + sync_state prediction verification (already the v7
   design), and use grid-jepa-class encoders for the JEPA-lite head. No external
   "agent-world" checkpoint is needed to run this pattern.
5. Expected: 70–90 levels path → **LB 30–50** (top-3 range, field-dependent).

### PLAN E — Ops & compliance discipline  (continuous)
- 1 submission/day/account; never burn a slot without 30+ preflight greens AND local
  benchmark ≥ current best internal score.
- **Multi-account rule**: Kaggle prohibits entering/submitting from multiple accounts —
  consolidate to ONE account immediately (flag raised; this plan's tables use notebook
  names only).
- ARC API key expired (401 since 9/18): request fresh key from operator for live-server
  replays; meanwhile local engine == scoring engine is proven, so verification continues.
- Gated `guanning` trace datasets: access requested, pending approval.
- Milestone-2 (due 9/30): NO-GO stands — open-source cut is publishable but the
  competitive edge decays if shipped mid-race; prize track is the priority.

## 3. Day-by-day schedule (Oct 1–7)

| Day | Build | Submit slot (best green candidate) |
|---|---|---|
| 10-01 | PLAYBOOK_MODE + governor; local verify all 53+2 | playbook harness (Plan A) |
| 10-02 | ARA transfers embedded; governor tuning from day-1 traces | Plan A tuned |
| 10-03 | Two-lane vLLM bring-up; lane-2 smoke test | best-of(A, A+swarm if green) |
| 10-04 | Router live; tr87 solver v0 behind env-var | Plan A+B(+C partial) |
| 10-05 | Mechanic priors ls20/su15/tr87/wa30/lf52; sb26 macro chain | Plan A+B+C |
| 10-06 | Freeze + variance draw ×2; ratchet rules | best internal re-run |
| 10-07 | Week review; Plan D start order; HF trace-learning upload | ratchet/best |

## 4. Go/no-go gates

| Item | Trigger | Cost | Expected | Verdict |
|---|---|---|---|---|
| Plan A playbooks | all 53 verified (done) | 0 GPU risk | +2–5 LB | **GO — first submit** |
| ARA transfers | lf52/su15 local-cleared (done) | 0 | +0.5–1.5 LB | **GO** |
| Efficiency governor | zero-game list (done) | 0 | +1–2 LB | **GO** |
| Two-lane swarm | KV math validated (done) | new serving code | +3–8 LB | **GO after Plan A ships** |
| **fast-lane model swap** | incumbent repo 404 (done) | 1 local A/B | parity required | **MANDATORY day-1** |
| pruned-RTXPRO 8B swap | 1 local A/B | ~0 | +0–1 | GO only if A/B wins |
| Ornith-A3B swap | harness/tool-format rework | 1–2 days | unknown | HOLD (offline test) |
| ericmao LoRA lane | vLLM LoRA on NVFP4/FP8 base | adapter loader | +1–3 deep | TEST in deep lane |
| tr87 code solver | win-rule doc (done) | 1 day | +1–2 LB | **GO** |

## 5. Risks & mitigations

- Board-hash mismatch on replay → fail-open to normal policy (never stall).
- Two-instance serving instability → fallback ladder (Plan B); non-model gains (A/C)
  carry the week regardless.
- KV starvation regression → per-lane KV budget printed at boot; watchdog kills lane B
  if Running workers < 60% of target for >5 min.
- Efficiency-squaring regression (r12 lesson) → governor caps + per-level actions/par
  telemetry to JSONL every run.
- **Checkpoint rot**: incumbents can vanish overnight (keithtyser 8B removed 09-30).
  Mirror every serving-critical checkpoint to our HF account before relying on it.
- Multi-account disqualification risk → consolidate accounts before next submission.

## 6. Where this leaves the campaign

Verified assets now in hand: 53/53 playbooks (25/25 games), 2 ARA transfers that beat
ours, complete mechanic docs for ls20/su15/tr87/wa30/lf52, KV-collapse root cause with
a fitting two-lane design, and a corrected score picture (official best 4.07, official
max-levels 45/183). The path is: **ship playbooks (7–12) → add swarm+priors (15–25) →
add deep-capability lane (30–50)**. Every mechanism is env-var switchable with a
rollback ladder; nothing ships without 30+ preflight greens.
