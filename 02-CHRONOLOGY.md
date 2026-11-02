# 02 — Chronology: how the campaign actually unfolded

## Phase 0 — Recon and doctrine (late September)

The campaign opened with sweeps of the Kaggle competition surface: public notebooks, the
Milestone-2 winner trio, top leaderboard configs, and the harness mechanics. This produced the
foundational teardowns (docs/04, 05, 10, 13 series) and the first doctrine: numbered docs for
every plan, a daily protocol, and the two-account structure (A = kragglenote2forwork,
B = dasshovon) that later collapsed into one team. Key recon conclusions: the M2S top
submission (~23.65 when we evaluated it) was the public ceiling to beat, the harness's slot
priority was the highest-leverage seam in the code, and interactive agent quality was bounded
by scheduling, not by model choice at that stage.

## Phase 1 — The super stack (Oct-04 → Oct-08)

First scored wave: the **super v2/v3** builds — M2S base plus a behavior stack (death-ledger
pair, dead-reasoning stub, effort ladder, reset exposure, act-forcer). Five draws, μ≈26.8,
best 27.67. Foreign baselines were also evaluated (Fable & Astra 27.17, M2S top 23.65). The
lesson forming here: the behavior stack helped a little, but the harness's scheduling formula
was still the bottleneck.

## Phase 2 — The D′ breakthrough (Oct-09)

**clean D-prime v1** replaced the harness's default slot priority with the D′ formula
(lwq255 fail-open-guarded, path fallbacks, one changed layer vs M2S) and scored **33.50** —
a +6 jump over the super-stack era, hash-verified, with inside/outside memos agreeing. This
became and remains the board best (#106). The D′ allocator is the campaign's core original
contribution: an efficiency-paced priority model over (action count, token spend, level pace)
with a guarded formula that fails open to the harness default.

## Phase 3 — Redraw science and the plateau (Oct-10 → Oct-19)

Ten days of disciplined redraws and small variants mapped the variance landscape: clean D′
drew 32.05 / 28.23 / 27.84 (μ≈30.5, n=4); the eis-recovery-dh fastpack of the uradkr lineage
drew 29.83 / 32.25 / 30.16 (μ≈30.2); EIS text-H ran its pre-registered two-draw rule
(31.62, 28.83 — no promotion). On the companion account the **uradkr family drew 36.49** —
the campaign's highest observed score and the existence proof for the 36+ zone. The plateau
was now clearly defined: every strong family sat at μ≈30, best draws 32–33.5, and the gold
cutoff (38+) was ~2σ away. Conclusion written into docs/45: **no redraw reaches gold; only a
real μ shift of +4 or more does.**

## Phase 4 — The apex line and the first graves (Oct-20 → Oct-24)

The apex program layered everything the recon said mattered: lexicon packs (apex-dlex:
26.73 / 19.99), combined guards (leviathan: 22.47 / 22.33), merge experiments (F+D: 20.77).
**Every apex-family end-to-end reading came in below the clean engine.** Component tests were
green every time — the scored rerun punished the additions anyway. On Oct-24 a re-anchor of
the 33.50 lineage with "hardening" deltas (dprime-fix-v3, attempt-8 after a 7-error platform
morning) scored **26.47** — the hardening itself cost ~7 points. That result founded the
single-delta discipline and the #36 grave (never reword the prompt).

## Phase 5 — The platform war (Oct-24 → Oct-26)

Oct-25's fire (agi35-v1, a verbatim transplant of a foreign LB-35.35 config) produced **0.00**
— grave **F-1030**: foreign configs do not survive the scoring rerun unadapted. Oct-26's fire
(apex-v11, our full gold stack: champion D′ + wastepack + dossier + FP8 27B) also produced
**0.00** — and this time the forensics (grave **F-1031**) proved the mechanism: the scoring
rerun hit a gateway/DNS patience wall, ran ~60 minutes (setup + the old 45-minute cap), and the
safety guard submitted a 3411-byte placeholder. The guard cell was byte-identical to the
Oct-24 run that scored 26.47 — same code, different platform behavior. The leaderboard showed
396 teams still scoring on Oct-25: the platform was alive; our rerun luck and patience were
the problem.

## Phase 6 — The countermeasure and the armed weapon (Oct-26, today)

In one day: forensics closed F-1031, **guard-v2** was built (120-minute gateway patience,
3600s DNS escape, smoke fast-path, guard_decision.json artifact), **apex-v12** was built on
the D2 spec (stall-knee fold + act_checked simulator-verified batching + additive tail), pushed,
run on GPU, and its receipts came back **all green** — including surviving a real 3612-second
DNS outage during the interactive run. The fire command is parametrized, the slot opens at
00:00Z Oct-27, and docs/48 holds the plan of record with pre-committed verdict rules.

## Parallel track — AGI-2

The campaign ran a parallel effort on arc-prize-2026-arc-agi-2 (board best 30.97, v37-EXP
resolved 27.36, v38 ladder receipts banked). It served as the proving ground for the LEG/model
ladder ideas and several operational tools that fed back into the AGI-3 toolchain.
