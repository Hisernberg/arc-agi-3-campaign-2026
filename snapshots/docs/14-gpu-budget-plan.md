# 14 — GPU Budget Plan: 1 run/day, 3–4 runs/week (2026-09-26)

User directive (2026-09-26): **one run per day maximum; 3–4 runs per week; ARC-AGI-3 GPU usage ≤ 10–12h/week (target ~8h, 4×2h); plan until perfection, THEN run.**

## 1. How ARC-AGI-3 actually consumes quota (measured this week)

| Cost item | Personal quota? | Measured |
|---|---|---|
| Version-producing batch run (API push → offline public-25 run) | **YES** | v7 nooa-lite v5: push 10:32 → COMPLETE 13:10 = **2h38m** |
| Scoring rerun (after `CreateCodeSubmission`) | **NO** (Kaggle-side, proven: 9/23–24 resubmissions scored with ~0 quota left) | ~30–90 min |
| Kernel churn / status checks / pulls | NO | — |
| Non-ARC kernels (MAGFiLO yolo pair) | YES but separate competition | 2×~2h (do not count against ARC budget) |

**One ARC submission ≈ one ~2.6h batch run.** 8h/week ≈ 3 runs; 12h/week ≈ 4 runs (with ~1h margin for a short verification run if ever needed).

## 2. Quota ledger (week ending 2026-10-03 refresh)

| When | What | Δ used | Running total (ARC only) |
|---|---|---|---|
| pre 9/26 | — | 1.89h (prior week remainder) | — |
| 9/26 10:32–13:10 | v7 nooa-lite v5 offline run (produced submitted version) | 2.6h | 2.6h |
| 9/26 13:20–~16:00 | 35c14d v1 offline run (in flight; variance datapoint + kernel restore) | 2.6h | ~5.2h |
| **ARC budget left this week** | | | **~6.8h ≈ 2 more runs MAX** (plan-gated) |

## 3. Run gate: nothing launches until ALL of these are true

1. **Score verdict on the previous run is in** and mined (score + transcript evidence, not vibes).
2. **Delta thesis written**: which mechanism(s) changed, expected direction, and the trace signal that would falsify it — one paragraph, in the run doc.
3. **CPU validation green**: unit suite (51 checks) + smoke (123 steps) + preflight 31/31 on the exact notebook about to be pushed.
4. **Byte-diff vs current best artifact** reviewed (only intended cells differ).
5. **Kernel slug/title matched** (title must equal the existing kernel title, else push renames the kernel — cost us a run today).
6. **Quota check**: week-to-date ARC usage + 2.6h + 1h margin ≤ 12h.
7. **1/day submission slot free** (UTC).

## 4. Calendar plan (sept 26 → oct 3)

| Day | Action | GPU | Gate/thesis |
|---|---|---|---|
| Sat 9/26 | v7 submitted (ref 56580276); 35c14d v1 variance run in flight | 5.2h spent | score >4.5 = v7 thesis confirmed; 2.85–4.5 = band (mine traces); <2.85 rollback |
| Sun 9/27 | **No run.** Mine both v7 public-25 outputs: per-game levels, dead-flag precision, budget-flag timing, label/Predict adoption, game_notes usage. Draft v8 design doc. | 0h | v8 thesis must come from trace evidence, not intuition |
| Mon 9/28 | Decision point: if v7 score ≥ 4.5 → build v8 (click heuristics L10 + plan caps L11 + scheduler waves L15 on top of v7) with full CPU validation; ship only if all gates pass. If v7 in band → one targeted fix from trace evidence (e.g. JSONL persistence bug, Predict-in-thinking fix) | 0h build / optional 2.6h run | Milestone-2 (9/30) go/no-go also due 9/28 — user decision, needs OSS snapshot |
| Tue 9/29–Wed 9/30 | Reserve: 1 run only if v8/fix passed all gates | ≤2.6h | cumulative ≤ 8h |
| Thu 10/1–Fri 10/2 | Reserve: 1 final run of the week only if a validated delta exists; otherwise bank the hours | ≤2.6h | cumulative ≤ 10.4–12h hard cap |
| Sat 10/3 | Quota refreshes (30h). Next week's plan written from the week's trace ledger. | 0h | — |

**Hard rules encoded**
- No push without a written thesis + green preflight (plan-until-perfection).
- Never push when the title doesn't match the kernel slug exactly.
- Never run two ARC kernels concurrently; never mix ARC and non-ARC batch runs the same day (today's slot-block lesson).
- If a run's local result (offline public-25) regresses vs the prior run's local result by >1 level-mass, do NOT submit-patch further without re-planning — the local signal is free, use it before spending the daily submission.
- Milestone-2 (9/30, needs open-source) = user go/no-go by 9/28; if GO, the OSS snapshot repo is prepared CPU-side (no quota).

## 5. What "perfection" means for v8 (evidence checklist from today's traces)

- Predict adoption was 25% of turns (197/787) and 5/21 games had zero — v8 must raise it (shorter instruction, per-turn echo of last pred verdict).
- `nooa_log` JSONL never appeared in output — fix persistence (likely working-dir/teardown interaction) so pred hit-rate becomes offline-minable; that is the ablation-grade signal for every later decision.
- Level distribution: 5 games at L3, 4 games at 0 — v8 should target the 0-level games (sk48/g50t/tr87/tn36 dead-starts) with the PRIMER/pair playbook before broad deepening.
- Budget flags: verify per-game baselines actually fired (budget.used vs human_prior) in the second run's artifacts; miscalibrated flags waste actions quadratically.

---

## UPDATE 2026-09-26 16:45 UTC — v7.1 discovery (run-gate thesis for tomorrow)

**Post-run forensics found the highest-value bug of the campaign.** Pulling BOTH v7 run outputs showed:

1. `nooa_log/unknown.jsonl` contained exactly ONE record (expected: 3422, one per executed action, per game).
2. Zero real `game_notes` injections (the only "animates"/"click-only" matches were the model's own reasoning).
3. Root cause: production `state_path` = `.../artifacts/ls20-9607627b_p0_tool_runtime_state.json` — the game id lives INSIDE the `.json` filename, which v4's segment-scan key extractor skips → **every game collapsed into one shared "unknown" state in EVERY production run (v4's 3.85 included)**. Consequences: no per-game baselines, no game_notes, no memory, shared ledger chaos, and the shared state died early (`done` fires on the first game_over/run_complete from ANY game), disabling the whole world_model block for ~the entire run.

**What this means:** the 3.85 was achieved by the static prompt addendum alone; the machinery never ran. v7.1 (built + validated today) parses the run_stem directly (`(.+)_p\d+_tool_runtime_state\.json$`). 55/55 unit checks + 123-step smoke green, including the new production-path regression section (20a–20d: correct key, per-game isolation, per-game baseline, per-game notes).

**Run 2 of this week = v7.1 tomorrow (Sat 9/27)** — today already consumed its daily slot (ref 56580276, pending) plus an unplanned second offline run (kernel-rename accident). The pending score will land as the "addendum-only" baseline; v7.1's run is the first honest measurement of the full mechanism stack.

