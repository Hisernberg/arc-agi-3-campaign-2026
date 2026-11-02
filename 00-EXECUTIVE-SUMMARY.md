# 00 — Executive Summary

## FINAL OUTCOME (2026-11-02, deadline day) — read this first

> This chapter's tables below were written on Oct-26 with 7 slots left. The campaign is now
> **closed**. Final numbers:

| Metric | Final value |
|---|---|
| **Final team best** | **35.53** — `arc26-megafusion-v25-mount-heal`, fired Nov-02 03:09Z on an ALL-GREEN gate, COMPLETE after ~9.9h |
| Gold-lane best | **35.53** (was 33.50 at the time of writing below) |
| Blackbox-lane best | **33.86** — eislab S13/S14 port (Oct-28) + a 6-draw max-of-N farm, final-day draw 32.94 |
| Constellation slot | between franzen 36.18 and eislab 34.98 (cluster top uradkr 36.89); gold zone 38.98 not reached (gap 3.45) |
| What carried it | proven D′ engine + eislab S14 carrier armor + pre-fire gate matrix V0–V7 + mount self-heal + max-of-N farm discipline |

The Oct-26 plan's prediction — "P(≥34 at least once) ≈ 80–90%" — landed on the last possible
day, one point above the plan's stretch band. Full final-week narrative:
[`11-ENDGAME-FINAL-WEEK.md`](11-ENDGAME-FINAL-WEEK.md).

---

## Where we were on 2026-10-26 (pre-final-week snapshot, kept for the record)


| Metric | Value |
|---|---|
| Board best | **33.50** — `arc26-b-dprime-clean-v1`, Oct-09 |
| Rank | **#106 / 4,799** |
| Gold cutoff (#20) | **38.20** today, drifting ~39–40 by Nov-02 |
| Gap to gold | **+4.7 minimum, +5.5–6.5 realistic** |
| Scored slots left | **7** (Oct-27 → Nov-02, one per day) |
| Oct-27 weapon | **apex-v12 v2 — built, receipts green, guard-hardened, fire command armed** |

## The campaign in one paragraph

We entered October with an M2S-derived harness scoring ~23–27. On Oct-09 a clean re-derivation of
the D′ slot-priority allocator broke the plateau with a **33.50** — still our board best and
#106 on the board. Ten days of redraws and variants mapped the noise floor (same config spans
27.8–33.5 across draws; cross-account the uradkr family once drew **36.49**). From Oct-20 the
apex line layered scheduling, knowledge, and model upgrades onto the proven engine; its three
fires were never properly scored — two died as **0.00 placeholders inside Kaggle's scoring
rerun** (a gateway/DNS patience problem, not an agent problem, proven byte-for-byte by F-1031
forensics) and one lineage variant scored 26.47. The current weapon, **apex-v12 v2**, keeps the
full stack, adds the two strongest untested scheduling deltas (stall-knee fold, act_checked
simulator-verified batching), and ships **guard-v2**, which on Oct-26 survived a real 61-minute
gateway outage that killed its predecessor.

## What actually moves the score (evidence-based)

1. **The D′ priority allocator is the engine.** Replacing the harness default slot priority with
   the D′ formula took the account from ~27 to 33.50. Every strong draw since runs some version
   of it. This is our single most validated component.
2. **Draw variance is the second-largest force.** The same clean D′ config drew
   33.50 / 32.05 / 28.23 / 27.84 (n=4, μ≈30.5, spread 5.7). Since the leaderboard keeps the max,
   disciplined redraws of the best-μ config are a legitimate scoring strategy, not a cop-out.
3. **Additive prompt/scheduling layers so far lost points end-to-end.** apex-dlex (26.73/19.99),
   leviathan (22.47/22.33), the re-anchor variant (26.47) all underperformed the clean engine.
   Component tests were green every time; the scored rerun punished them anyway. This is why the
   plan enforces single-delta discipline and pre-committed verdict rules.
4. **The scoring rerun is a separate environment that must be engineered for.** Interactive runs
   (which are not scored) were flawless; the rerun killed us twice. Guard-v2 exists because of
   this and is the highest-leverage fix of the final week.

## The plan to gold (detail in 06/07)

- **Oct-27 — D2:** fire apex-v12 v2 (stack + stall-knee + act_checked + guard-v2). Verdict ~90
  minutes after fire. ≥34 clears Stage A; >33.50 is a new board best; 0.00 triggers forensics,
  never a blind re-fire.
- **Oct-28 — D3:** v13 adds transition-graph priors, a KM-style pace table, and an endgame phase
  switch, plus the dossier tool-registration fix.
- **Oct-29 — D4:** solver diversification on the games the dossier shows stalling.
- **Oct-30 → Nov-02 — D5–D7:** redraw farm on the highest-μ verified config (farm eligibility:
  ≥2 completed draws, μ̂ ≥ target−2σ, no 0.00 in last 3).
- **Cumulative odds:** P(≥34 at least once) ≈ 80–90%; P(≥38 at least once) ≈ 35–50% if D3/D4
  hold their tested effect sizes. The leaderboard keeps the max, so no draw can hurt us.

## The three rules that keep us alive

1. **Ratchet:** the board best only moves up (LB takes max) — but *knowledge* ratchets too: a
   verdict is never closed without an attribution.
2. **Verdict council:** every score is read against pre-committed rules written *before* the
   fire. No post-hoc rationalization, no moving goalposts.
3. **Death traps:** never fire an unadapted foreign config (F-1030), never reword the prompt
   (#36), never trust an unvalidated rerun path (F-1031), never leave a slot empty while a
   verified weapon sits armed.

---

## Evening update — Oct-26 15:45Z (six-notebook teardown + v2)

User-directed teardown of the six public notebooks (docs/52, byte-exact via
kernels/pull): all six are the same Franzen M2 chassis; heliosli and
romantamrazov are pure redraw farms of it (86 versions on one slug); D′
scheduler (weitaoguo, 31.54) already ships in our v13; vickyfym's cache-safe
solved-level memory (31.46, +2.8) becomes v14 MEMORY-SEA's core; yongjiehishi's
negative results (throughput/admission do not transfer, +16 levels from
NOOP guard) are codified as doctrine. Public frontier: nothing above 31.54 —
our 33.50 board best still leads every public number.

Rehearsal caught two pre-fire blockers in v13 v1 (saltb0x 27B dataset never
attached → silent qwen3.5 fallback; xpack tools=False ordering) → **apex-v13 v2**
pushed 15:35Z with both fixed (10/10 gates + CPU test on fake mounts).
GOLDRUSH fire at 00:05Z now targets v2 with upgraded receipts
(served=qwen38-27b-fp8 dir=saltb0x, tools=True, heal=import-ok).
Idea pool 1,515 → **1,575** (batch F, docs/52+53-derived).
New docs: 52 (teardown), 53 (HYDRA/RIVER/CORTEX daily mixture architectures
+ keyword calendar), 54 (GOLDRUSH final v2 = plan of record).
