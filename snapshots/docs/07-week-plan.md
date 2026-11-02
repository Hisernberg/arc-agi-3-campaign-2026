# 07 · Week Plan (Sat Sept 19 → Fri Sept 26, 2026)

> **Verified 2026-09-19 (Sat):** Kaggle allows **1 submission per day** (API `submission-limits`).
> The 2×-variance rule is reinterpreted: variance is averaged **across consecutive days** by
> re-submitting the highest-EV variant on a later day. Sat 9/19 = Submission Day 1.

## Status board (updated 9/19 ~06:30 UTC)

- **Sat 9/19 (today):** v3 (`duck-governor-v1`) pushed 05:59 UTC, QUEUED behind
  NVARC-family GPU runs from the same account. Watcher auto-submits on completion;
  finalizer records score + PDF + push unattended.
- **Built while GPU runs:** `duck-worldmodel-v1` (10/10 tests) ready for Monday;
  25-game mechanics KB in `analysis/games/`; notes-2026-09-19.md.

## Score decision tree (applies at each day close)

| v3/day-N score vs best (3.45) | Verdict | Next-day action |
|---|---|---|
| ≥ 3.45 | new best — lineage validated | resubmit same version (variance harvest), prep next patch |
| 3.00–3.45 | in family band — neutral | resubmit same version for variance; continue planned variant Monday |
| < 3.00 | patch delta negative | next day: revert to last good config (production-12), record hypothesis |
| error / no score | crashed run | next day: resubmit last good config; audit patch locally first |

## Milestone targets

| Day | Submission | Content | Gate |
|---|---|---|---|
| Sat 9/19 | `duck-governor v1` (= Anim Base 35c14d **v3**) | A2 probe-budget governor + schema-lite prompts; verify GPU = RTX Pro 6000 | unit tests pass, v3 pushed 05:59 UTC |
| Sun 9/20 | `duck-governor v1` resubmit **or** `duck-governor v2` | If v3 ≥ 3.0: repeat for variance average; else triage test A3 (dynamic time budget) | v3 score known |
| Mon 9/21 | `duck-worldmodel v1` | B1 world-model loop v0 (persist hypothesis notes + backtest flag), conservative prompts | local replay tests |
| Tue 9/22 | best-of-lineage | re-run best variant (whichever scored highest) | — |
| Wed 9/23 | `duck-ctx v1` | A4 context window/compaction experiments | serving smoke test |
| Thu 9/24 | `duck-governor v2` | A3 per-game budget triage (dynamic time allocation) | mock-LLM sim pass |
| Fri 9/25 | best-of-week | variance harvest + M2 prep freeze | — |

**Milestone 2 (Sep 30) note:** the notebook used on ~Sep 28–29 must be a cleaned,
documented, public-open-sourceable version (prize requires open source). Prepare its
write-up during 9/26–9/29.

## Daily loop (automation, see docs/08)

1. Morning: `kaggle_status.py` → check quota, submissions, leaderboard movement.
2. Pick today's variant (per table above); update notebook cell 13 params + push new
   version via Kaggle API; interactive Save & Run.
3. On completion: submit; log score to `analysis/results.md`; 2nd submit of same version.
4. Evening: mine request logs + traces → `analysis/notes-<date>.md`; update game
   knowledge base (`analysis/games/<game>.md`); adjust next-day plan.
5. If GPU hours exhausted: resubmit best-performing existing version instead (2×).

## Success metrics for the week

- [ ] Score ≥ 6.0 (stretch 8.0) — each completed level ≈ +1.5–3 pts (docs/02)
- [ ] All 25 public games traced locally; ≥10 games have mechanics notes
- [ ] 3–4 notebooks shipped & submitted (2× each)
- [ ] Zero submission errors / notebook crashes
- [ ] Replay dataset accumulated for next week's LoRA (C2)

## Risks & mitigations

- **GPU quota burn on crashed runs** → mandatory local dry-run + serving smoke cell.
- **Variance misread as improvement** → always 2× submissions; compare on same-day.
- **Overfitting to public-25** → keep changes generic (no per-game hacks); validate
  ablations on ≥2 games before/after.
- **Kaggle API automation breakage** → automation scripts are advisory; manual fallback
  documented in docs/08.

## 2026-09-19 amendments (Submission Day 1 realities)

- **Submission cap is 1/day** (verified via API + 11-sub history pattern). The "2×
  variance rule" becomes *consecutive-day resubmission*: submit the same high-EV
  version again on a later day when a variant isn't ready.
- **Variance measured**: 11-sub history sd=0.44, same-family band 2.45–3.45 (spread
  1.0). Decision rule: a variant delta < ±0.5 is noise; only roll back if
  score < best − 1.0 (3.45 → rollback threshold 2.45).
- **Per-level efficiency model** (analysis/games/per-level-efficiency.md): median
  human baseline by level index = [30, 54, 51, 54, 96, 80, 86, 92, 163, 225] actions.
  Late levels hold most weight (L8 of 8 = 8/36 of game mass) but cost 3–8× more
  actions; completion dominates efficiency (docs/02).
- **worldmodel v1.1** replaces plain v1 as the next ship: adds `game_notes`
  (offline-probed, public-25 keyed, fail-open) + `budget` tracking vs human-baseline
  prior (transfers to hidden eval). 13/13 unit tests green vs real bundle.
- **Ship queue**: Sat 9/19 = governor-v1 (v3, queued) → next slot = worldmodel-v1.1 →
  then either tuned-knob variant (analyzer timeout, thinking budget) informed by v3
  traces, or v1.1 resubmit for variance harvest.

## Success metrics — amended

- [ ] Score ≥ 6.0 (stretch 8.0)
- [x] All 25 public games traced + mechanics KB (25/25)
- [x] Per-level efficiency model + agent cheat sheet
- [ ] 3–4 notebooks shipped (1/day cap): governor ✓(pushed), worldmodel-v1.1 ready,
      1–2 more from knob tuning / trace-informed changes
- [ ] Zero submission errors / notebook crashes
- [ ] Replay dataset accumulated for next week's LoRA (C2)
