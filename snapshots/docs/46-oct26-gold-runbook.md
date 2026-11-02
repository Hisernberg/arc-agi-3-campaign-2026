# 46 · OCT-26 GOLD RUNBOOK — v11 weapon + 1015 ideas + fire order (written 2026-10-25 18:0xZ)

## 0. What got built tonight (user directive: "tomorrow must gold or best possible work")

| Deliverable | Artifact | Status |
|---|---|---|
| **Dossier v2 dataset** (ALL 25 games categorized, 7 category playbooks, transform tool library, SFT gold traces, RL memory seeds, palette/symmetry hints) | Kaggle `dasshovon/arc26-game-dossier-v2` (CC0) | **LIVE** |
| **apex-v11 kernel** = apex-v1 + v2 x-pack (categories + tools + SFT + UCB1, one fail-open cell, additive prompt tail, distinct marker) | `dasshovon/arc26-b-apex-v11` v1 | **PUSHED, GPU run in flight** — 13/13 own gates + inherits 22/22 apex-v1 gates; prior apex-v1 GPU run had ALL receipts green (FP8 served, wastepack+dossier installed) |
| **Idea pool ≥ 1000** | docs/40 (112) + batches A/B/C (408) + batch D (495) = **1015** | **DONE** |
| Transform tools unit-tested | `ours_transforms` (translate/gravity/objects/effect) | PASS |
| Gold plan (two-stage, honest math) | docs/45 | pushed (8f1eb08) |

Fail-open chain (worst case = vanilla champion): v2 absent → apex-v1 · FP8 absent → incumbent
serving · dossier absent → champion. Receipts to read WITH the score: `#OURS_WASTEPACK ok`,
`APEX_FP8=True`, `#OURS_DOSSIER ok`, **`#OURS_XPACK ok`** (new: mounted/games_categorized/
sft_exemplars/tools flags).

## 1. Fire order for Oct-26 (slot opens 00:00 UTC; fire at ~00:05Z for queue-crunch buffer)

1. **G1 check both kernels** (~23:30Z): `dasshovon/arc26-b-apex-v11` AND `dasshovon/arc26-b-apex-v1`.
2. **Fire v11** if COMPLETE: `FIRE_KERNEL=dasshovon/arc26-b-apex-v11 FIRE_VERSION=1 python3 scripts/fire_oct26_apex.py fire`
   (script env-overrides are supported; description tag "apex" matches the poll filter).
3. **Fallback**: v11 not complete/errored → fire apex-v1 (verified complete + all receipts green):
   `FIRE_VERSION=1 python3 scripts/fire_oct26_apex.py fire`.
4. `python3 scripts/fire_oct26_apex.py poll 60` → verdict + receipts.
5. Verdict bands (pre-committed): >28.37 promote · 26.47–28.37 noise · ≤26.47 reject ·
   0.00 → forensics before any re-fire. **Board lens**: any draw >33.50 = new board best →
   that config becomes the redraw-farm target (docs/45 §6).
6. Evening verdict council → docs/47; build **apex-v2** (Oct-27) = v11 + stall-knee 80-action
   fold (2.8σ) + DF-WM `act_checked()` port; both fail-open, same gate pattern.

## 2. AGI-2 parallel lane

v37-EXP completes ~01:00Z → read verdict; if Oct-26 slot open + v38 validation green → fire
v38 LEG ladder from A lane. Same discipline, separate board (best 30.97).

## 3. Gold math recap (docs/45)

Board best **33.50** (rank 106) · 34 → rank 76 (Stage A) · gold cutoff 38.20 today → ~39–40 by
Nov-02 (Stage B) · ladder D1 v11 → D2 stall-knee+act_checked → D3 transition-graph+pace+endgame
→ D4 MCTS/Pathfinder → D5–D7 redraw farm (incl. guaranteed redraw of the 33.50 config,
`kragglenote2forwork/arc26-b-dprime-clean-v1`, A-lane token).

## 4. Graves + discipline (unchanged)

No verbatim foreign configs (F-1030) · no prompt rewording (#36) · noop-guard OFF (#4) · no
env-block transplants · foreground polling only · G1+G2 before every fire · single reading
never promotes · fire at 00:05Z (Oct-24 error-storm lesson).

## 5. Ledger (tonight)

- `scripts/build_dossier_v2.py` → `artifacts/datasets/arc26-game-dossier-v2/` → Kaggle dataset
  (categories.json, playbook_v2.json, sft_exemplars.jsonl, memory_seeds.json, transforms.py,
  index.json, games/ 25, boards/ 50).
- `scripts/build_apex_v1_1.py` (13 gates) → `artifacts/daily/2026-10-26/push_b_apex_v11/`
  (32 cells = apex-v1 31 + xpack cell; metadata 5 datasets + 2 models, code_file fixed).
- `scripts/build_ideas_batch_D.py` + `build_ideas_batch_D2.py` →
  `reports/oct26_sweep/ideas_batch_D.jsonl` (495).
- Recovery note: sandbox reset mid-session; restored everything from origin/main (8f1eb08) —
  .env tokens restored from user-provided values.
