# docs/24 — THE ONE PLAN: "APEX v9 = Duck-plus-ours + Playbooks + Value Lottery"

Task 15 · 2026-09-30 · Single consolidated plan superseding the parallel-plan layout for the next two weeks. Companion: docs/23 (>5 wave analysis), docs/21 (MOAGS/MOAW), docs/20 (world model).

## 0. The one-sentence plan

**Rebuild on the now-public >5 stack (Duck on Flash-Next-NVFP4), port the proven lottery scheduler, add the two things nobody in the >5 wave has — our 53 verified playbooks and value-corrected allocation with a stall-aware efficiency governor — then farm the variance with repeated identical finals.**

Why this and not anything else: the >5 wave proved with public, replicated numbers that (a) the keithtyser-Duck serving base is the strongest foundation, (b) the Affectify scheduler is worth +1.5–1.7 LB on it, (c) σ≈1.5 between identical submissions makes best-of-N draws worth more than most code changes. Our playbook library and allocator ideas are the only clean deltas on top that don't disturb the proven stack.

## 1. Architecture (one submission, five layers)

```
┌ L5 VARIANCE FARM: identical code ×4–6 finals in the last 10 days, keep best draw
┌ L4 MOAW-LITE SHIELD (flagged, optional per-run): playbook mismatch guard +
│   stall-veto on irreversible actions (no LLM ensemble in v1 — KV is better spent on width)
┌ L3 PLAYBOOK LANE (ours, unique): 53 verified playbooks, L1 auto-replay on all 25
│   games + sb26 L1→L8 chain + ARA transfers (lf52 L1=9 actions); per-game
│   leaderboard + (action,region) untried tracking from wa30 lesson
┌ L2 LOTTERY SCHEDULER (ported Affectify, credit mandatory): tickets =
│   value-corrected triangular worth of next level × stall decay (knee by level:
│   51/72/78/132 p90, halflife 40, floor 0.05) × anneal (K=3, P0=0.4, P1=1.9)
┌ L1 SERVING BASE: Duck harness, Flash-Next-NVFP4 (primitive-ai repack —
│   checkpoint-rot fix), MTP3, ctx 16K, dedup USER boilerplate (−24.5% input),
│   thinking OFF, changed_cells tool, KV reservation 6 GiB, 28-way games
```

Layer rules inherited from the wave's hard-won lessons: never wipe history (−4.20, EXP-099 §9.2); every prompt byte must buy turns; model is TOLD the triangular scoring ("one level deeper is the largest gain"); scheduler drops only the *right to think*, never the game.

## 2. What we port vs what we add (the honest split)

**Port from public (with attribution, all verified in docs/23):**
- keithtyser serving stack + RadixArk/primitive-ai NVFP4 base (public, pinned)
- Affectify scheduler mechanics: ticket raffle, stall decay, annealing, 16K ctx + USER dedup, thinking-off, changed_cells tool, FACTS injection
- Scott Le Grand's KV6B bump (5→6 GiB reservation)

**Our additions (the deltas nobody in the >5 wave has):**
1. **Playbook lane (biggest edge).** Their stack enters every L1 cold. Our 53 playbooks clear 25/25 L1s at 7–130 actions (vs 50–190 re-explore) and sb26 to L8. On triangular scoring, guaranteed L1s + deep chains are direct points and freed time the raffle can spend elsewhere. Integration: on level entry, replay playbook if board-hash guard matches; fail-open to policy; log everything.
2. **Value-corrected tickets (OURS_VALUE done right).** Their value correction is flagged as default-off; we make it the default and add per-game N estimation from the bestiary/level-count priors. Their own example shows the bug it fixes (3.7× misallocation).
3. **Level-scaled stall knee.** Their EXP-106 numbers (p90 51/72/78/132) demand knee ∝ level; their config runs uniform 80. We implement `knee = 45 + 25·level` and floor 0.05 (their ⑦ note shows floor 0.1 still over-feeds L5 dead games at (1+25)·0.1=2.6 vs initial 2.0).
4. **(action, region)-level untried tracking** inside each game (wa30 lesson: 181 tries, 6 distinct exact actions) — feeds the stall decay with a second signal: no-unseen-region-left ≈ true dead end, decay faster.
5. **Playbook-guided annealing**: games with remaining playbook chains get a ticket multiplier at their next-chain level (we *know* they're winnable — the raffle should know too).

**Explicitly NOT in v9** (kept behind flags, next wave): world-model sidecar (F2/F3 — after the >5 base is secured), 27B deep lane (KV math now favors width at 16K ctx; revisit after first v9 score), Flash-Next-125B endgame (qwen4_exp support gate), image experiments (Attention Lottery's 4.69 says they didn't pay).

## 3. Build order (each step gated; local engine = scoring engine, proven)

| Day | Build | Gate to proceed |
|---|---|---|
| Oct 1 | L1 base: duck + primitive-ai NVFP4 + MTP + 16K ctx + dedup + thinking-off; offline smoke on 3 games | 110-game offline run completes; no vLLM restarts; input tokens ≤16K |
| Oct 2 | L2: port scheduler (raffle + stall + anneal), A/B offline vs equal-allocation | offline levels-reached ≥ +10% vs L1-only on 25-game rehearsal |
| Oct 3 | L3: playbook lane + hash guard + logging | 53/53 local replay green inside harness; zero wasted actions on L1 replays |
| Oct 4 | L2+L3 integration: playbook-aware tickets + level-scaled knee + region tracking | sb26 reaches L8+; offline mean ≥ 1.15× L1-only |
| Oct 5 | **SUBMIT v9-a** (submission #1 of the farm) | 30+ preflight greens, full offline pass |
| Oct 6–7 | L4 flag work (stall-veto, mismatch guard); watch v9-a; **SUBMIT v9-b identical code** | — |
| Oct 8–10 | variance draws v9-c/d; if v9 best ≥6.5 → start F2 world-model LoRA in parallel | — |

Submission budget: deadline 2026-11-02 → ~32 slots left. Farm plan uses 4–6 for v9 draws; the rest stay available for the F-line wave.

## 4. Score projection (honest)

| Component | Evidence-based estimate |
|---|---|
| Base (our 4.07 on same family) | 4.1–4.6 (serving fixes + 16K dedup double effective width) |
| + lottery scheduler (Affectify delta on identical base) | +1.5–1.7 → 5.6–6.3 |
| + playbook lane (25 free L1s, chains, freed time) | +0.4–1.2 → 6.0–7.5 |
| + variance farm best-of-4..6 (σ≈1.5) | +0.7–1.5 → **7–9 realistic band** |
| Stretch (value tickets + knee fixes land perfectly) | 9–11 |

This takes us past the public 5.75 and into the public-pool lead — but **not** to top-3 (cutoff 26.55). The plan is explicitly two-stage: v9 secures the >5 base and every efficiency lesson; the October second wave (F2 world-model LoRA + MOAGS routing of playbook/algo/LLM lanes + Flash-Next-125B if supported) is what attacks 26+. Stacking both is the only route to "win" that the evidence supports.

## 5. Risks & countermeasures

| Risk | Countermeasure |
|---|---|
| Ported scheduler has hidden coupling to their bundle | They designed it as a drop-in cell on Duck's hook — same hook we use; port function-by-function with our own names; keep OURS_* switch names for parity with their findings |
| Playbook replay wastes actions on mismatch | board-hash guard + fail-open (already proven in PLAYBOOK_MODE design) |
| Dedup changes prompt behavior (their −4.20 fear) | keep contract on active turn; kill-switch `OURS_DEDUP_USER=0`; A/B in rehearsal |
| Variance farming burns slots on bad draws | only farm AFTER offline rehearsal shows distribution ≥ base; 4–6 draws max; keep 20+ slots for the F-line |
| Attribution/licensing | credit Tufa Labs, keithtyser, Scott Le Grand, Affectify in the notebook header (all public; our additions documented in docs/23–24) |
| Multi-account compliance risk (standing warning) | consolidate submissions under the single authorized account before the farm phase |

## 6. Immediate actions (today)

1. Push docs/23–24 + notebook-intel extracts to repo; HF Space update (public best now 5.75 — KPI + new section + plan v5 pointer).
2. Start Oct-1 build: L1 base assembly against our existing duck-harness knowledge (docs/04) + primitive-ai repack.
3. Book GPU session for the 110-game offline rehearsal (their regime) Oct 2–4.
