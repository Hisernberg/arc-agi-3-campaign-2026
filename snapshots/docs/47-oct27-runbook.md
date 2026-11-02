# docs/47 — Oct-27 Gold Runbook (apex-v12 = D2)

## State at write time (2026-10-26 ~09:20Z)
- **Oct-26 slot FIRED**: apex-v11 v1 → ref **57659975** (08:31Z, PENDING; score expected 17:30–22:00Z)
- **Oct-27 weapon BUILT**: `dasshovon/arc26-b-apex-v12` v1 — pushed 09:1xZ, **GPU queued** (pinned docker
  57e612b4, RTX Pro 6000, 5 datasets, 2 models). 15/15 build gates + 13/13 real-module tests green.
- AGI-2 parallel: v37-EXP (ref 57630786) still PENDING 20h+ (kernel itself complete — scoring queue slow).
  v35 = 30.97 AGI-2 board best.

## What apex-v12 adds over the fired apex-v11 (D2, pre-committed in docs/45 §v2 spec)
1. **#71 stall-knee fold into D′** (EXP-106, 2.8σ measured, strongest scheduling constant in sweep):
   `priority *= max(0.1, 1/(1+(a−80)/40))` — flat knee 80, halflife 40, floor 0.1.
   Post-FORM wrap of `tool_agent.priority_value` (same proven seam), additive constants only,
   zero prompt rewording (#36 grave). Fail-open → exact v11 priority on any exception.
2. **#83 DF-WM `act_checked()` port** (flagship own-build lever): injected into the python-tool
   sandbox via line-scoped bootstrap patch (indent-agnostic, compile-guarded). Model batches run
   ONE action at a time; each verified against the model-written `simulate()`; divergence raises
   `PredictionMismatchError` with "[SIMULATOR DIVERGENCE] … Remaining N action(s) cancelled to save
   budget" → the model re-hypothesizes instead of burning budget on a wrong batch. Fail-open:
   no simulate() → plain batch; literal not found → no injection (telemetry `act_lit_count`).
3. One additive system-prompt tail (third wrap, distinct marker `_ours_v12`): tells the model
   simulate()+act_checked() exist, fallback plain action() still works.

## Receipts to read on the v12 GPU run (before firing Oct-27)
- `#OURS_V12 stall_knee=True knee=80 halflife=40 floor=0.1 flat`
- `#OURS_ACTCHECKED {'stall': True, 'act_checked': True, ...}` (if `act_lit_count` appears →
  bootstrap literal changed upstream → investigate before firing)
- `#OURS_V12_TAIL installed`
- plus the inherited v11 receipts: `#OURS_WASTEPACK ok`, `#OURS_DOSSIER ok games=25`,
  `#OURS_XPACK ok`, `#OURS_FORM ok version=d_prime`, Y21 AUDIT FP8 primary.

## Oct-27 fire protocol (00:00Z slot open)
1. `python3 scripts/check_state.py`-equivalent: kernel v12 status == complete AND receipts above
   present in kernel output (`reports/` helper: receipts_g2.py pattern, slug v12).
2. `python3 scripts/fire_sdk.py` (edit SLUG → `arc26-b-apex-v12`, VERSION → latest, date in desc)
   → verify PENDING + ref.
3. Score lands ~9h later. Verdict rules: **>33.50 = new board best**; ≥34 Stage A done;
   38.2+ = gold cutoff zone (cutoff drifting to ~39-40 by Nov-02; solid gold = ≥39).
4. 0.00 → forensics first (F-1030 grave discipline). Never re-fire unadapted configs.

## Attribution plan (verdict council after both draws land)
- v11 draw (Oct-26) = v1+v2 layer WITHOUT stall-knee/act_checked; XPACK logged `tools:false`
  (tool registration fail-open — dossier-v2 prompt knowledge WAS installed; tool library likely
  not importable). Treat v11 as measuring: champion+wastepack+FP8+dossier-1/2 prompt-tail.
- v12 draw (Oct-27) adds: stall-knee + act_checked + tail. If v12 > v11 → D2 deltas positive.
- Keep single-delta discipline for v13: only add what the council attributes positive.

## Fallback ladder (Oct-27, if v12 receipts bad)
1. apex-v11 v1 (complete + receipts green; already scored once — redraw variance capture)
2. wastepack-v1 pure / champion dprime redraw v3
3. clean-v1 redraw (33.50 config, guaranteed ≥34-capable shot; A-lane token)
