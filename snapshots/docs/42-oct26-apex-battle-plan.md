# 42 · Oct-26 APEX BATTLE PLAN — wastepack + model swap + game dossier (written 2026-10-25 15:40Z)

## 0. Situation

- **Two competitions, two daily team slots** (quota model corrected Oct-24: TEAM allowance = 1/day
  per competition; pending blocks; merged team = dasshovon + kragglenote2forwork):
  - **AGI-3** (`arc-prize-2026-arc-agi-3`): Oct-25 slot burned by AGI35 config-swap → **0.00**
    (ref 57627860, F-1030). Anchor **26.47 stands** (attempt-8, ref 57594680). LB rank 106/4799,
    best 33.50.
  - **AGI-2** (`arc-prize-2026-arc-agi-2`, NVARC line): v37-EXP submitted 13:01Z (ref 57630786,
    12h rerun in flight, score Oct-26 AM); v38 "LEG model ladder" staged+validating (kernel
    running 13:06Z). NVARC v34 = 28.61 (ref 57481575).
- **Sweep**: 718 notebooks listed, 60 pulled (30+30), **520 ideas pooled** (docs/40 = 112,
  batches A/B/C = 408) + top-50 personalities dossier (`reports/oct26_sweep/top50_dossier.md`).
- **User directive**: new model + new data + CoT style + optimized, combining best-scoring work,
  submitted from **dasshovon**, ready for tomorrow.
- **GPU quota note** (v38 header: 36,812s/21,600s, refresh Oct-31) contradicted by observed GPU
  kernel runs today 10:12/10:37/11:17/13:06Z — treat as advisory; **CPU probe before GPU push**
  regardless.

## 1. The Oct-26 AGI-3 submission: `dasshovon/arc26-b-apex-v1`

**Layering** (each stage keeps the previous gates green):

| Layer | Content | Verification |
|---|---|---|
| L0 champion | byte-identical dprime-fix-v1 lineage (26.47, ref 57594680) | G02-G05 md5 parity |
| L1 W-pack | death ledger + repeat guard + fatal-prefix lookahead ON; WM notes kept on death; W1 USER-boilerplate dedup; W2 identical-snippet refusal; W3 turn counter | wastepack 10/10 gates + 8/8 unit tests (re-run today: PASS) |
| L2 model swap | Qwen3.5-27B block-FP8 (eliork) — Pennyroyal-native Qwen3_5 EntryClass, hybrid-linear flags valid, FP8 KV ~1.9GB/seq fits; drafter OFF on swap | CH1 feasibility chain + **fail-open revert to incumbent W4A16+drafter if mount absent** + **CH1 v4 post-mortem fix** (`os.path.exists(None)` TypeError, died 5.8s — now None-safe) + T4-T7 tests |
| L3 game dossier | dataset `dasshovon/arc26-game-dossier-v1`: 25 games × {probe-session mechanics, real-trace summaries, human budget/level, dead actions, click cells, sequence rules, CoT plan, L1 boards txt+png}; ONE additive system-prompt tail (no rewording) via `_build_system_prompt` wrap | dataset live (25/25) + T1-T3, T8, T9 vs REAL harness module |

**Build**: `scripts/build_apex_v1.py` → **22/22 gates GREEN** (31 cells).
**Tests**: `scripts/test_apex_v1.py` → **10/10 PASS** vs the real ARC3-Inference module + local
dataset mirror (+ wastepack 8/8 regression re-run green).
**Staging probe**: `arc26-b-apex-probe13` (CPU) verifies the exact 4-dataset + competition
attach-set + qwen3.5 config fingerprint + dossier completeness BEFORE any GPU run.

**Worst case per layer** (F-1030 discipline): L1 fail-open → vanilla champion; L2 mount absent →
incumbent serving (APEX_FP8=False printed); L3 not mounted → `#OURS_DOSSIER disabled`. The only
unfail-open residual = FP8 checkpoint present-but-crashes-at-load (accepted, bounded by probe P2d
config check + CH1 fp8-module feasibility).

## 2. Verdict rule (pre-committed, unchanged)

- Baseline = **26.47**, noise floor ±1.9, keep-above **28.37**.
- **> 28.37** → PROMOTE; **26.47–28.37** → NOISE BAND (log draw, anchor stands); **≤ 26.47** → REJECT.
- **0.00/error** → F-chain forensics BEFORE any re-fire (F-1022/F-1030 death trap).
- Attribution receipts printed by the run: `#OURS_WASTEPACK ok ...`, `APEX_FP8=True/False`,
  `#OURS_DOSSIER ok {...}` — the score readout must be read together with these.

## 3. Fire-day runbook (Oct-26, B lane = dasshovon)

1. `python3 scripts/oct25_status_probe.py` — slot + kernel state.
2. G1: `dasshovon/arc26-b-apex-v1` kernel COMPLETE (pushed + validated Oct-25 evening).
3. G2: no pending submission.
4. `python3 scripts/fire_oct26_apex.py fire` (or `loop 560` windows) → ref logged to
   `reports/oct26_draw_apex.json` + `submit_log.jsonl`.
5. `python3 scripts/fire_oct26_apex.py poll 60` → verdict → apply §2 → write `docs/43-oct26-live.md`.
6. **Fallback ladder**: (a) wastepack-v1 pure (drop L2/L3) — built+verified; (b) champion redraw
   (`arc26-b-dprime-fix-v1` v3) — variance wash.
7. **AGI-2 parallel**: when v37-EXP completes (~01:00Z) AND Oct-26 slot open → fire **v38** from
   A lane after its validation kernel reads green (LEG model ladder: Qwen3.6-27B-FP8 primary,
   qwen3-8-27b-fp8-repacked fallback — field-evidenced model strike).

## 4. Idea-pool integration (520 entries — what made it in, what's queued)

- **In this build**: #2/#3/#20 (death ledger + lookahead + WM wipe), #19 (W1 dedup), #10 (W2
  refusal), #76-79 (serving discipline), batch-B B-041 (D' constants audited), dossier = the
  "per-game data + CoT" directive materialized.
- **Next-ranked (Oct-27+)**: #71 stall-knee 80-action fold into D' (2.8σ measured); #83 DF-WM
  `act_checked()` port; #48 transition-graph; B-016 border-crop state-hash risk check on the
  death ledger; B-023 read-timeout yield-not-rollback; C-084 context watermarks; C-069 action-
  grant scheduler; #66 KM pace table; #67 endgame phase switch.
- **Respect the graves**: no prompt rewording (#36); noop-guard stays OFF (#4); no source-BFS on
  hidden set (#52); no env-block transplants (F-1030).

## 5. Danger register (unchanged from docs/41 §5)

1. No same-day re-fire after 0.00 without forensics. 2. Additive prompt text only. 3. Mechanisms,
   never env blocks. 4. Foreground polling only (sandbox kills background procs). 5. G1+G2 gates
   before every fire. 6. Single reading never promotes; anchor moves only > 28.37.

## 6. Ledger

- Idea pool: docs/40 (112) + `reports/oct26_sweep/ideas_batch_{A,B,C}.jsonl` (113+169+126 = 408)
  → **520 total**; top-50 dossier: `reports/oct26_sweep/top50_dossier.{md,json}`.
- Dossier dataset: `scripts/build_game_dossier.py` → `artifacts/datasets/arc26-game-dossier-v1/`
  → Kaggle `dasshovon/arc26-game-dossier-v1` (25 dossiers + 50 boards + playbook + index).
- Apex build: `scripts/build_apex_v1.py` (22 gates) → `artifacts/daily/2026-10-26/push_b_apex_v1/`.
- Apex tests: `scripts/test_apex_v1.py` (10/10, real-module + resolver/quant/diag/dataset).
- Probe: `scripts/build_probe13.py` → `arc26-b-apex-probe13` (CPU, staging-only).
- Fire: `scripts/fire_oct26_apex.py` (status/loop/fire/poll, foreground).
- CH1 v4 post-mortem: died 5.8s at cell 3 diag `os.path.exists(None)` (DRAFT_MODEL_DIR=None);
  fix = None-safe exists + dynamic APEX_FP8 across serving cells (apex G11/G12/G14/G15).
