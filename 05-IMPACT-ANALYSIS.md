# 05 — Impact analysis: what actually moved the score, and what we only believe moved it

The campaign's central epistemic problem: **component tests are green almost always; the scored
rerun is the only judge.** This document separates the two honestly.

## Tier 1 — End-to-end validated (the rerun itself confirmed it)

| Component | Evidence | Impact |
|---|---|---|
| **D′ allocator** | 27.67-era → **33.50** on Oct-09; every strong draw since runs D′ | **+5 to +6** — the engine |
| **Harness fit (M2S base, mounts, resolver)** | All completed scores 19.99–33.50 ran some version of it | Foundation, no isolated delta |
| **Redraw variance** | clean D′ n=4: 33.50/32.05/28.23/27.84 | Same config spans **5.7 points** — the LB-max rule monetizes this |
| **Hardening deltas on the clean lineage** | dprime-fix-v3: **26.47** vs clean 33.50 | **−7** — "improvements" can be net-negative |
| **Lexicon + guards (apex-dlex, leviathan)** | 26.73 / 22.47 / 22.33 / 19.99 | **−3 to −10** vs the engine — the additions did not survive the rerun |
| **Verbatim foreign config** | agi35-v1: **0.00** (F-1030) | Categorical: transplants do not adapt to our rerun path |
| **Old guard vs dead gateway** | v11 + agi35: 0.00, 3411B placeholders, ~60-min reruns (F-1031) | The 45-min patience cap was the proximate cause of both deaths |

## Tier 2 — Component-validated, end-to-end UNMEASURED (the Oct-27 verdict decides)

| Component | Component evidence | Honest prior |
|---|---|---|
| **Stall-knee fold** | 2.8σ in the sweep — strongest scheduling signal measured | Positive, moderate (+0.3 to +1.0 if it transfers) |
| **act_checked() batching** | Flagship design; errors=0 live; divergence-cancel path unit-tested (divergence-cancels-batch, factor math, idempotency — 13/13) | Positive if the model's `simulate()` is right often enough to pay for itself |
| **Dossier v1 prompt-tail (25 games)** | Mounted, 0 errors, protocol steps live in every apex run | Unproven end-to-end; apex line never completed a scored rerun |
| **Wastepack** | Green receipts every run; dedup/refusal counters live | Unproven end-to-end |
| **FP8 27B primary + 2 drafters** | Serves clean, license-audited | Unproven end-to-end vs the older serving path |
| **XPACK categories/SFT/RL prompt-tail** | Mounted, 25 games categorized | Unproven; tools fail-open (prompt knowledge only) |

**Why the caution:** every prior apex-family addition was green in components and red in the
rerun (Tier 1 rows 4–5). The base rate says: do not project component σ onto the leaderboard.

## Tier 3 — Validated as *protections* (their impact is a 0.00 that doesn't happen)

| Component | Evidence |
|---|---|
| **Guard-v2** | Survived a real 3612s DNS outage interactively; decision artifact works |
| **Fail-open wrappers everywhere** | Explains why every degraded interactive run still produced valid output |
| **Receipts + fire gates** | Zero mis-attributed fires since the system landed |
| **Byte-pinned deps** | Rerun environment reproducibility across Oct-24/25/26 incidents |

## The attribution model this buys us (used by the verdict council)

For the Oct-27 fire, the reading decomposes as:

```
score(v12) = engine_μ(≈30.5±) 
           + Δ(stall-knee)      [0 if not transferred]
           + Δ(act_checked)     [0 if not transferred]
           + Δ(stack vs clean)  [UNKNOWN — could be negative; apex-line base rate says so]
           + draw_noise(±1.9 planning floor, 5.7 observed spread)
           × P(completed rerun | guard-v2)   [≈50–60%]
```

Pre-committed verdict rules (docs/45/47/48): **>33.50** new board best · **≥34** Stage A ·
**38.2+** gold zone · **<33.50 but >0** → the stack's Δ is re-priced and D3 adjusts ·
**0.00** → forensics first, never a blind re-fire.

The single most important thing Oct-27 buys is not the score itself — it is the **first
completed measurement of Δ(stack vs clean)**, which every remaining day of the campaign
depends on.
