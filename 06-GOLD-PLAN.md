# 06 — The gold plan: D1–D7 ladder, verdict rules, redraw farm

Full doctrine: docs/45 (strategy), docs/47 (Oct-27 runbook), docs/48 (plan of record) —
all snapshotted in [`snapshots/docs/`](snapshots/docs/). This is the distilled, current version.

## Targets

- **Stage A: ≥34** — clears the 33.50 ceiling, proves the stack, becomes the farm target.
- **Gold: ≥38.2 today, ≥39 by Nov-02** — cutoff #20 was 38.20 on the Oct-26 sweep with ~200
  subs/day still flowing; the cutoff drifts up.
- Both consume the same ladder; only the last three slots change role.

## The lever ladder (what each remaining slot is for)

| Slot | Lever | Content | Status |
|---|---|---|---|
| D1 · Oct-26 | apex-v11 (D1) | stack v1: champion D′ + wastepack + dossier + FP8 | burned — 0.00 (F-1031 gateway) |
| **D2 · Oct-27** | **apex-v12 v2** | D2 deltas: stall-knee fold + act_checked + guard-v2 | **ARMED — receipts all green** |
| D3 · Oct-28 | v13 | transition-graph priors + KM pace table + endgame switch + tool-registration fix | specified (07) |
| D4 · Oct-29 | v14 | solver diversification on dossier-flagged stall games; council-picked deltas only | queued |
| D5–D7 · Oct-30→Nov-02 | **redraw farm** | re-fire the highest-μ verified config, max-statistic harvesting | config must qualify (below) |

## Fire protocol (every day, no exceptions)

1. **G1:** kernel status COMPLETE on Kaggle · slot open (0 subs today, UTC) · quota-reject probe
   harmless if wrong.
2. **G2:** receipts grepped from kernel output — the full docs/47 list, all green.
3. **Fire** via `scripts/fire_sdk.py <owner/slug> <version> "<desc>"` (kagglesdk, Bearer).
4. **Verdict ~90 min later** (Oct-26 actual: fired 08:31Z, scored ~10:0xZ). Read against the
   pre-committed rules. Council, then next build.

## Verdict rules (pre-committed — written before the fire, never after)

- `> 33.50` → **new board best**; that config becomes the redraw-farm target immediately.
- `≥ 34` → Stage A cleared.
- `38.2+` → gold cutoff zone; ≥39 → solid gold at current drift.
- `0 < score < 33.50` → council attributes: engine fine, some Δ negative → re-price, adjust D3.
- `0.00` → **forensics first** (rerun artifacts, guard telemetry, platform state), support
  ticket with refs if platform-caused, never re-fire an unadapted config (F-1030/F-1031 law).

## Redraw farm rules (D5–D7)

A config qualifies for the farm only if **all** hold:
- ≥2 completed draws;
- μ̂ ≥ target − 2σ;
- no 0.00 in its last 3 draws;
- kernel still COMPLETE on Kaggle (no rebuild risk on the last days).

Current qualifiers: clean D-prime (μ≈30.5, n=4, best 33.50) and eis-recovery-dh (μ≈30.2, n=3).
If apex-v12 lands >33.50, it supersedes both. The farm fires daily with the best qualifier;
the leaderboard keeps the max, so each draw is a free tail sample toward 34–36.

## Cumulative odds (honest, planning-floor ±1.9)

- P(≥34 at least once, Oct-27 → Nov-02) ≈ **80–90%** — requires either one D2/D3/D4 μ-shift or
  the farm harvesting a +1 tail from a μ33 config.
- P(≥38 at least once) ≈ **35–50%** — requires D3+D4 to hold their component effect sizes
  end-to-end AND at least one healthy-window rerun per new config.
- Every 0.00 day burns one ticket → guard-v2 (already in) is the highest-leverage component
  of the entire week.

## Platform-risk playbook (active all week)

- Rerun health is a daily coin-flip we cannot probe from outside; guard-v2 is the mitigation.
- If a rerun dies despite guard-v2: forensics on `guard_decision.json` + rerun artifacts, a
  support ticket with submission refs and timings, and the fallback config fires the next day.
- Fallback ladder if any day's primary is un-fireable: (1) apex-v11-source + guard-v2 "v11g"
  build, (2) clean-v1 direct re-fire (zero build; old-guard risk accepted), (3) wastepack-v1
  pure / champion redraw v3.

---

## Oct-27 keyword protocol (docs/49, plan of record)

Weapon: **apex-v13 v1** (D2 + D3 + Qwen3.8-27B-FP8 swap). User keyword **`GOLDRUSH`** at
00:05Z Oct-27 = G1 slot check -> G2 receipts (`#OURS_V38`, `#OURS_V12`, `#OURS_ACTCHECKED`,
`#OURS_V13`, `#OURS_WASTEPACK`, `#OURS_DOSSIER`, `#OURS_FORM`) -> fire via
`fire_sdk.py dasshovon/arc26-b-apex-v13 1` -> verdict ~90 min.
Escalation: `GOLDRUSH-FORCE` (ignore G2 warnings, council-only), `ABORT`, `STATUS`.
Branches: AMBER = fire v12 v2; RED = clean-v1 re-fire. Odds: P(>=34|complete) ~35-50%,
P(top-50 tomorrow) ~35-50% conditional, P(>=34 once in 6 slots) ~80-90%.
