# docs/48 — Oct-27: the 34+ shot (plan of record)

## 1. What we learned Oct-26 (inputs to this plan)
- **apex-v11 = 0.00** (ref 57659975): scoring rerun died on gateway patience (F-1031).
  3411B guard placeholder, rerun length ~60 min ≈ setup + 45-min cap.
- **F-1030 revised**: config transplant was not the killer; the rerun gateway is.
- **Platform NOT dead**: 396 teams scored Oct-25, 533 Oct-24; top-20 active through Oct-25
  (#12 40.98 Oct-25 03:08, #16 38.85 Oct-25 01:50). Our reruns die where others' live
  → per-run gateway luck + patience, not a global outage.
- **Lineage spread warning**: the 33.50 config's re-anchor (Oct-24) landed **26.47** —
  deltas on this lineage can LOSE points. Nothing above 33.50 in 17 days of draws.
- **All 3 KGAT tokens = one account/team** (identical private sub lists) → 1 slot/day, no B-lane.
- **clean-v1 (33.50) is directly re-fireable**: `kragglenote2forwork/arc26-b-dprime-clean-v1 v1`,
  same team, kernel COMPLETE. Zero build cost insurance shot (but carries the OLD 45-min guard).

## 2. apex-v12 v2 — G2 receipts read 2026-10-26 ~10:50Z (all green)
- `#OURS_V12 stall_knee=True knee=80 halflife=40 floor=0.1 flat` — D2 delta #1 exact spec
- `#OURS_ACTCHECKED {'stall': True, 'act_checked': True, 'tail': False, 'errors': 0}` —
  D2 delta #2 live; no `act_lit_count` (bootstrap literal intact); sandbox-tail False is
  cosmetic (system V12_TAIL installed)
- `#OURS_V12_TAIL installed`
- `#OURS_WASTEPACK ok` (dedup 0 / refusals 0 / errors 0)
- `#OURS_DOSSIER ok games=25 prompt_tail=installed errors=0`
- `#OURS_XPACK ok mounted games_categorized=25 tools=False` (known fail-open, v13 item)
- `#OURS_FORM ok version=d_prime` — full D′ priority formula live
- `[Y21:AUDIT]` FP8 primary + drafters + dossier licensing all clean
- `guard_decision.json` artifact works: `guard_version 2, run_full false, gateway DNS dead
  3612s (87 tries)` — interactive run correctly degraded (interactive runs are NOT scored;
  placeholder there is expected). **Guard-v2 survived a 60-min DNS outage without dying.**
- v12 currentVersionNumber = **2** (fire version 2). Datasets: dossier-v1+v2, pennyroyal,
  qwen3.5-27b-fp8, source bundle. Competition attached.

## 3. The one uncontrollable: the scoring rerun's gateway
- The rerun must resolve the `gateway` host (game service). Recent rerun outcomes:
  Oct-24 12:45Z **scored** · Oct-25 11:17Z dead · Oct-26 08:31Z dead.
- Our countermeasure is patience: guard-v2 = 120-min gateway cap + 3600s DNS escape
  (vs 45 min that died twice). If the outage inside the rerun is bounded < 2h, we complete.
- We cannot probe the rerun env from outside (gateway DNS is expected dead interactively).
- Therefore: fire the best-armed config, accept the dice, read the verdict fast (~90 min).

## 4. Fire protocol — Oct-27
1. **00:05Z**: G1 check — kernel `arc26-b-apex-v12` status complete, slot open (0 subs today).
2. **00:06Z**: G2 re-read — receipts via `kernels/output` (list in §2; all must be green).
3. **00:10Z**: `python3 scripts/fire_sdk.py dasshovon/arc26-b-apex-v12 2` → verify ref + PENDING.
4. **~01:30-02:30Z**: verdict lands (Oct-26 scoring took ~90 min). Read, then council.
5. Rationale for 00:10Z vs midday: no evidence midday reruns are healthier (Oct-25 11:17Z died);
   fastest verdict = maximal forensics + v13 build hours if 0.00.

### Branches
- **AMBER** (a receipt red at G2): emergency build `v11g` = apex-v11 source + guard-v2 cell
  only (single delta: platform fix, no scoring deltas) → 30-min build + 3 gates → fire.
- **RED** (kernel broken): backport guard-v2 into clean-v1 fork (60-min build) OR raw
  clean-v1 re-fire (`fire_sdk.py kragglenote2forwork/arc26-b-dprime-clean-v1 1`, edit DESC)
  accepting old-guard risk.
- **0.00 verdict**: forensics FIRST (rerun output artifacts if present, guard telemetry,
  support ticket with refs 57627860/57659975 + rerun timings). Never re-fire unadapted.

## 5. Verdict rules (pre-committed, unchanged from docs/45/47)
- `> 33.50` new board best → that config becomes the redraw-farm target.
- `≥ 34` Stage A cleared (user goal floor).
- `38.2+` gold cutoff zone today; solid gold = ≥39 by Nov-02 (cutoff drift).
- `< 33.50 but > 0` → council attributes the drop (stack vs engine), re-price D3.

## 6. Honest odds (stated to the user, no varnish)
- P(rerun completes) ≈ 50-60% — guard-v2 has 2.5x the patience of the config that died twice;
  healthy windows demonstrably exist.
- P(≥34 | completes) ≈ 35-50% — receipts green, component tests strong (stall-knee 2.8σ,
  act_checked flagship), but the stack's first end-to-end reading; lineage spread 26.47-33.50.
- P(≥38 tomorrow) ≈ 5-10% — needs the stack to over-deliver by +4.5 over the engine baseline.
  The 38+ path is the ladder: D3 v13 (Oct-28: transition-graph priors + KM pace + endgame
  switch) → D4 (Oct-29) → redraw farm (Oct-30 → Nov-02) on the best-μ config
  (farm eligibility: ≥2 completed draws, μ̂ ≥ target−2σ, no 0.00 in last 3).
- Downside is capped: LB takes max — 33.50 is protected no matter what tomorrow draws.

## 7. Probability of ≥34 at least once this week
With 7 slots (Oct-27..Nov-02), a mix of stack shots (μ rising via D2-D4) and redraw farm on
the best config, cumulative P(≥34 once) ≈ 80-90%; P(≥38 once) ≈ 35-50% IF D3/D4 deltas
hold their component-test sizes. Every 0.00 day burns one lottery ticket — guard-v2 is
therefore the single highest-leverage fix of the week, and it's already in.
