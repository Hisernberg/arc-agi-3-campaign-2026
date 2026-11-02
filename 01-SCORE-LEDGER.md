# 01 — Score Ledger (complete, 2026-10-04 → 2026-10-26)

Source: Kaggle submissions API, pulled 2026-10-26. Raw data: [`snapshots/data/all_subs.json`](snapshots/data/all_subs.json).
**Totals: 250 submissions · 180 complete · 70 errored · ~20 scored 0.00 · date range Oct-04 → Oct-26.**

## A. Every completed score, descending

| Score | Date | Ref | Config / what it was |
|---|---|---|---|
| **33.50** | Oct-09 | 56994560 | **clean D-prime v1** — lwq255 fail-open-guarded D′ + path fallbacks, one changed layer vs M2S. **Board best.** |
| 32.25 | Oct-17 | 57297300 | eis-recovery-dh redraw (uradkr-36.49 release fastpack lineage; sibling draw 29.83) |
| 32.05 | Oct-10 | 57050666 | clean D-prime **resubmit** (same config as 33.50 — pure redraw) |
| 31.62 | Oct-17 | 57298529 | EIS text H, first attributed draw (pre-registered two-draw rule) |
| 30.77 | Oct-12 | 57094303 | frozen COMPLETE source evaluation (companion-account config eval) |
| 30.35 | Oct-11 | 57056539 | v2d v2 = v1's scored-rerun policy + E-135 mount resolver |
| 30.16 | Oct-19 | 57387404 | eis-recovery-dh redraw (μ 30.2, n=3 at the time) |
| 30.05 | Oct-14 | 57168017 | (no description) |
| 29.83 | Oct-14 | 57163088 | eis-recovery-dh = uradkr-36.49 release fastpack, byte-exact sha, 28 pinned cells |
| 29.21 | Oct-07 | 56901959 | (no description, M2S-era) |
| 28.83 | Oct-18 | 57331028 | EIS text H, second draw per two-draw rule |
| 28.59 | Oct-18 | 57345341 | resubmit of the PROVEN 32.25 v1 — version-vs-account isolation experiment |
| 28.23 | Oct-12 | 57108755 | clean D-prime redraw |
| 28.16 | Oct-13 | 57150301 | dh-e001-v1 = clean D′ + E01 deadline watchdog + provenance manifest |
| 28.03 | Oct-13 | 57129298 | (no description) |
| 27.84 | Oct-19 | 57387375 | clean D-prime redraw (μ 30.5, n=4 at the time) |
| 27.67 | Oct-07 | 56900990 | super v2 re-draw #2 (M2S base stack) |
| 27.38 | Oct-04 | 56825089 | super v2 full: M2S + death-ledger + dead-reasoning stub + effort-ladder + reset exposure + act-forcer |
| 27.17 | Oct-06 | 56886854 | "Fable & Astra Play ARC-3" public notebook, v2 (foreign eval) |
| 26.73 | Oct-20 | 57424564 | apex-dlex A v3 (M2S + D-prime + lexicon) |
| 26.66 | Oct-05 | 56842664 | super v2 re-roll 3 |
| **26.47** | Oct-24 | 57594680 | dprime-fix-v3 attempt-8 — re-anchor of the 33.50 lineage after 7 platform errors; **the "hardened" variant lost 7 points** |
| 26.47 | Oct-16 | 57258538 | (no description) |
| 26.34 | Oct-05 | 56859016 | super v3 full: S1 level-replay on super v2 stack |
| 26.03 | Oct-15 | 57216531 | (no description) |
| 25.84 | Oct-04 | 56825114 | super v2 full (sibling draw of 27.38) |
| 24.50 | Oct-10 | 57026424 | v2b = v2 + E-135 mount resolver (10 streams) |
| 23.65 | Oct-08 | 56940861 | "arc-agi-3-m2-top-submission" (foreign M2S top eval) |
| 22.47 | Oct-21 | 57466630 | leviathan-v1 A (apex-dlex core + animation-aware no-op guard) |
| 22.33 | Oct-21 | 57466626 | leviathan-v1 combined build |
| 20.77 | Oct-06 | 56877835 | F+D: dfranzen M2S + fable layer + Osaka D-prime slot prior (merge experiment) |
| 19.99 | Oct-20 | 57424569 | apex-dlex B v2 (first lexicon-enabled draw, account B) |
| 0.00 | Oct-25 | 57627860 | agi35-v1 config-swap — verbatim foreign LB-35.35 config (grave **F-1030**) |
| 0.00 | Oct-26 | 57659975 | **apex-v11 v1** — full gold stack; scoring rerun gateway-patience death (grave **F-1031**) |

## B. Config families — the honest statistics

| Family | Draws | Scores | μ | Verdict |
|---|---|---|---|---|
| **clean D-prime** (D′ allocator, lwq255 guard) | 4 | 33.50 / 32.05 / 28.23 / 27.84 | ≈30.5 | **The engine.** Owns the board best. Huge draw spread. |
| **eis-recovery-dh** (uradkr fastpack lineage) | 3 | 32.25 / 30.16 / 29.83 | ≈30.2 | Solid; second-best family; carries the 36.49 lineage |
| super v2/v3 (M2S + behavior stack) | 5 | 27.67 / 27.38 / 26.66 / 26.34 / 25.84 | ≈26.8 | Pre-D′ baseline era |
| EIS text-H draws | 2 | 31.62 / 28.83 | ≈30.2 | Two-draw rule executed, no promotion |
| apex-dlex / leviathan (D′+lexicon+guards) | 4 | 26.73 / 22.47 / 22.33 / 19.99 | ≈22.9 | **End-to-end regression.** Components green, score red. |
| dprime-fix-v3 (hardened re-anchor) | 1 | 26.47 | — | Hardening deltas cost ≈7 vs the clean config |
| foreign configs (M2S top, Fable&Astra, agi35) | 3 | 23.65 / 27.17 / 0.00 | — | F-1030 grave: verbatim transplants do not survive the rerun |
| **uradkr (companion account)** | 1 | **36.49** | — | **Existence proof:** our own config family reached 36+ |

## C. Variance law

- Same-config redraw spread observed: **5.7 points** (clean D-prime: 33.50 → 27.84).
- Campaign noise floor used in planning: **±1.9** (from the Oct sweep analysis in docs/45);
  the observed n=4 spread is wider, so μ estimates stay conservative until n≥3 per family.
- Consequence: the leaderboard-max rule makes every additional draw of a ≥μ33 config a free
  lottery ticket toward 34–36. This is the mathematical basis of the D5–D7 redraw farm.
- 0.00s are **not** variance — they are binary rerun failures (gateway death, F-1031) or
  config catastrophes (F-1030). They are engineered against, not averaged over.

## D. What the ledger says about the remaining week

1. To beat 33.50 we need either a lucky tail draw of a μ≈33 config (possible, not plannable)
   or a **real μ shift of +1 to +4** from the D2/D3/D4 levers (plannable, unproven end-to-end).
2. The apex stack has **zero completed end-to-end readings**. Until Oct-27's verdict, every
   projection of it is a component-test extrapolation, not a measurement.
3. The 70 error subs (mostly Oct-24's 06:20–11:45Z platform incident and older infra fights)
   cost roughly a week of aggregate slot time — the operational discipline in docs/DAILY_PROTOCOL
   exists because of them.


---

## B. Final-week extension (Oct-27 → Nov-02, API-verified 2026-11-02)

The table above covers Oct-04 → Oct-26. The final week — the GOLDFUSION/MEGAFUSION endgame —
is documented in [`11-ENDGAME-FINAL-WEEK.md`](11-ENDGAME-FINAL-WEEK.md) and in full
machine-readable form in [`data/`](data/). Headline fires:

| Date | Lane | Fire | Score |
|---|---|---|---|
| Oct-28 | blackbox | eislab S13/S14 port v1 | **33.86** (team PB until Nov-02) |
| Oct-29 | gold | GOLDFUSION v16 | **31.09** (0.00-streak breaker) |
| Oct-30 | gold | MEGAFUSION v17 MOTION_TOK | 28.09 |
| Oct-31 | gold | GOLDFUSION v16 redraw | 28.93 |
| Nov-01 | gold | MEGAFUSION v18b cards-fd | **32.31** |
| Nov-02 | blackbox | eislab farm draw 7 | **32.94** |
| Nov-02 | gold | MEGAFUSION v25 mount-heal | **35.53 — FINAL TEAM PB** |

Raw ledgers: [`data/ledger_unified.csv`](data/ledger_unified.csv) (unified Oct-04 → Nov-02),
[`data/farm_draws.csv`](data/farm_draws.csv), [`data/constellation_final.csv`](data/constellation_final.csv),
plus the Oct-26-era snapshot in [`snapshots/data/all_subs.json`](snapshots/data/all_subs.json).
