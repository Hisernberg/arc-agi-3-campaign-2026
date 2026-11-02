# DAILY PROTOCOL — ARC Prize 2026 (LOCKED 2026-10-19 by user directive)

> "remember from tomorrow everyday new plan and new code, notebook submission to score best possible"
> — and on 2026-10-19 the redraw violated "submit new code and notebook today". That failure is the
> reason this protocol exists. NO MORE REDRAWS.

## The three laws

1. **NEW CODE DAILY.** Every UTC day, each account (A = kragglenote2forwork, B = dasshovon) submits
   a kernel whose version has NEVER been submitted before on that account. Redraws of an
   already-scored version are FORBIDDEN unless the user explicitly orders one in that day's
   instructions.
2. **VERIFY BEFORE FIRE.** A kernel is only submitted after `kernels/status` returns COMPLETE for
   its exact pushed version. Commit runs on RTX6000 take ~1.5–2.5h. Push the next day's kernel the
   previous evening, never the same morning.
3. **ONE DELTA PER DAY, PER ACCOUNT.** Each daily variant changes exactly ONE lever vs the current
   best base (single-module discipline). Both accounts log draws of the same base first, then split
   into A/B deltas to read each lever's effect. The ledger (IDEAS_LEDGER.md) is the queue of levers.

## Daily clock (UTC)

| Time | Action |
|------|--------|
| 00:00–00:15 | `python3 scripts/submit_daily.py artifacts/daily/<today>_manifest.json` — fires both accounts |
| 00:15–01:00 | Record yesterday's pending/complete scores into reports/ + IDEAS_LEDGER evidence tags |
| daytime | Read score deltas → pick next single-module delta from IDEAS_LEDGER.md → build variant via `scripts/build_daily_variant.py` → push BOTH kernels for TOMORROW → wait for COMPLETE |
| evening | Confirm both kernels COMPLETE → write `<tomorrow>_manifest.json` → git push repo |

## Environment facts (learned 2026-10-19)

- **Mount layouts differ per account AND per run type**: dasshovon mounts competition data at
  `/kaggle/input/competitions/<slug>/` (kraggle's scored reruns historically did too), while
  kraggle commit runs mount `/kaggle/input/<slug>/`. NEVER hardcode either. All lineage kernels
  carry the `_find_comp_dir` resolver (cells 11+26) since r3/r2 — keep it in every future variant.
- Correct competition slug everywhere: `arc-prize-2026-arc-agi-3` (not `arc-prize-2026`).
- Commit runs (RUN_FULL=false) finish in ~4 min on RTX6000; only scored reruns burn hours.

## Failure playbook

- **Submission ERRORs**: never burn the day retrying the same version. If a version errors in the
  scored rerun, the NEXT day gets a NEW variant (or a diagnosed fix pushed as a NEW version).
- **Kernel not COMPLETE by 23:00 UTC**: do not submit it. Submit the fallback = previous best NEW
  variant that IS complete, or let the day go to the account whose kernel is ready (one account
  submitting is better than zero; a redraw is not an option).
- **Pending lock**: 1 pending max per account; submissions at 00:05 UTC only after yesterday's
  pending resolved (check `competitions/submissions/list` first — submit_daily.py does this).

## Current rotation (update nightly)

| Date (UTC) | Account A (kraggle) | Account B (dasshovon) | Status |
|------------|--------------------|-----------------------|--------|
| 2026-10-19 | ~~clean D-prime redraw~~ (burned, pending 57387375) | ~~eis-recovery v1 redraw~~ (burned, pending 57387404) | VIOLATION day — protocol created |
| 2026-10-20 | arc26-a-apex-dlex-v1 **v3** (D′+lexicon, NEW) | arc26-b-apex-dlex-v1 **v2** (D′+lexicon, NEW) | both COMPLETE (v3/v2 = mount-layout resolver fix) |
| 2026-10-21 | **arc26-a-leviathan-v1 v1** (combined: anim-guards + PACE=1 + TFF 0.4 + R3 ledger, lexicon OFF) — FIRED 57466626 | **arc26-b-leviathan-v1 v1** (identical config, same-config dual draw) — FIRED 57466630 | FIRED 05:5x UTC; pace/tf04 pair = fallback artifacts; scores ~9-20h |
| 2026-10-22 | candidate: SOLVED_LEVEL_MEMORY port (lalalia9 31.46, LB-proven same-family) | candidate: same base + next lever per combo read | PLANNED — radix/autotune demoted to bench-only (hidden-cost caution #189) |
| 2026-10-22 (final) | **QUOTA EXHAUSTED** — artifacts prebuilt (push_a memsolve); push+submit at quota reset | **arc26-b-memsolve-v1 v1 PRIMARY** (clean D-prime + solved-memory) / control fallback arc26-b-dprime-recal-v1 v1 — both COMPLETE 17:2x | BUILT — verdict D-2026-10-22-01; leviathan layer retired; pool 570 ideas / 400 personas |
| 2026-10-22 (fired) | QUOTA EXHAUSTED — push_a memsolve prebuilt; push+submit at quota reset (~Oct-24) | **arc26-b-memsolve-v1 v1 FIRED ref 57517413** 08:42 UTC (primary; clean D-prime + solved-memory, lexicon OFF) | FIRED — control dprime-recal-v1 untouched fallback; kill <25.5 / new-base ≥28.5; score ETA 9-20h |
| 2026-10-22 (read) | memsolve on A QUARANTINED — rebuild push_a as CONTROL before quota reset | **0.00** on memsolve-v1 ref 57517413 (structural fast-fail; forensics F-1024) — B slot burned | Oct-23 B = FIRE CONTROL dprime-recal-v1 (re-anchor + isolator); A ~Oct-24 = control too; memsolve v2 only after control read |

Base scores to beat (pooled mu): apex-dlex family mu ≈ 29.4–30.5 (n=7 clean D-prime draws,
best 33.50); EIS-recovery mu ≈ 30.2 (n=5, best 32.25). Ratchet target: any draw > 33.50.

## Evidence rules

Every scored draw gets appended to IDEAS_LEDGER.md with: date, account, variant, score, and the
lever it isolates. A lever is promoted to the shared base only with ≥2 supporting draws and no
contradicting draw worse than −1.0. Variance here is huge (same recipe spans 26.0→33.5), so
single draws never prove anything — pairs and trios do.
| 2026-10-23 | rebuild push_a as byte-identical CONTROL before quota reset (~Oct-24); NO lever on A | **arc26-b-dprime-recal-v1 v1 PRIMARY** (byte-identical 33.50 control; isolator for memsolve 0.00) — armed via scripts/fire_oct23.sh, fire at 00:0x UTC | ARMED — verdict zones D-2026-10-22-04 (0.00=platform breaker/forum; <26=recompute; 26-30=memsolve implicated; >=28.5=base strong); doctrine docs/34-ambition-doctrine.md; pool 610; deadline Nov-02 |

## Keyword calendar (docs/53, user directive 2026-10-26)

| Day | Keyword | Build |
|-----|---------|-------|
| Oct-27 | GOLDRUSH | fire apex-v13 (docs/54); then build v14 MEMORY-SEA |
| Oct-28 | HYDRA | v15 = v14 + 5-voter council (UCB1) |
| Oct-29 | RIVER | v16 = v15 + flow control + flow tools |
| Oct-30 | CORTEX | v17 = v16 + SNN filter + world-model planner |
| Oct-31+ | FARM | redraw farm max-of-N on champion |

Fire on keyword = docs/54 GOLDRUSH protocol (G1 → G2 receipts → FIRE 00:10Z → verdict T+90).
