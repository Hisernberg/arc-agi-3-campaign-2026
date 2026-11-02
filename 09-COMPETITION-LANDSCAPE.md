# 09 — Competition landscape (2026-10-26 sweep, n=4,799 teams)

Source: `snapshots/reports/leaderboard_full.csv` (full sweep pulled Oct-26 ~10:36Z).

## The shape of the board

| Zone | Rank | Score | Meaning |
|---|---|---|---|
| Superhuman top | #1–2 | 71.48 / 68.91 | Yi-Chia Chen (Fields Model) · Tufa Labs — in a different league |
| Strong top-10 | #3–10 | 56.02 → 45.03 | multiple teams 45+ |
| **Gold zone** | **#11–20** | **42.77 → 38.20** | **cutoff #20 = 38.20** |
| Silver-ish | #21–60 | ~38 → ~31 | steep density |
| **We are here** | **#106** | **33.50** | 1.7σ below the cutoff by the planning floor |
| Tail | #3,000+ | <10 | long tail of partial participation |

## Cutoff dynamics

- Submission volume is *rising*, not falling: 203 subs Oct-23 → 533 Oct-24 → 396 Oct-25
  (the Oct-24/25 numbers include platform-error churn, but the trend is real).
- #16 (Daniel Franzen, 38.85) and #12 (40.98) both scored on Oct-25 — the gold zone is active.
- Campaign planning number: **cutoff ≈ 39–40 by Nov-02**. Solid gold = ≥39; the ladder's
  Stage-B target (μ≈35–36 + farm max-statistic) aims at exactly this band.

## What the top teams' patterns show

- **Tufa Labs (#2, 68.91)** burned **171 submissions** — the max-statistic farming strategy at
  industrial scale. Validation for our D5–D7 farm design, at the fraction of the budget we have.
- **Yi-Chia Chen (#1, 71.48)**: 41 subs — fewer, better; consistent with a strong μ engine plus
  disciplined draws. Our D′-engine + farm plan rhymes with this shape.
- Mid-board teams (rank 30–120) cluster at 30–35 — exactly our band; the difference between
  #106 and #20 is ~5 points of μ, not luck. That is why the plan is μ-shift-first
  (D2/D3/D4), farm-second.
- 25 games × level-based scoring: the score is a *mean over games of level progress*, so the
  cheapest points live in the games where we stall earliest — the dossier's stall-flag list is
  the priority map for D4.

## Foreign-config intelligence (what the campaign evaluated)

- M2S top submission: 23.65 in our rerun (docs/30 teardown) — the public ceiling is real but
  not gold.
- Fable & Astra handbook: 27.17.
- agi35 (rank-51 config, verbatim): 0.00 — F-1030.
- dfranzen components (pennyroyal wheels, source bundle, M2S base): load-bearing parts of our
  own stack, properly digested and pinned.
- The lesson across all of it: public configs score their authors' numbers only inside their
  authors' pipelines. Components transfer; notebooks don't.

## Strategic conclusion

Gold at ≥39 needs **+5.5 over the engine's best draw**. No realistic farm alone gets there
(max-statistic on μ33.5 ≈ 35–36). No realistic single delta gets there either. The only path
that reaches is: **stack μ-shifts (D2 → D3 → D4) to μ≈35–36, then let the farm's max-statistic
add the final +2–3** — which is precisely the ladder in docs/45/48.
