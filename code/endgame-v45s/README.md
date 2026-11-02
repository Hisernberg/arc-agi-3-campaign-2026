# ARC26 Endgame v45s (Nov-1, 2026)

Competition: ARC Prize 2026 — ARC-AGI-2 (Kaggle code competition, lock 05:45 UTC Nov-2).

- `arc26-nvarc-v44-mixture.ipynb` — the full mixture-of-solvers build (37 cells, static PASS):
  v43 chassis + 3.8-class quant ladder entry via the proven v38 swap infra + 6h-cap budget.
  Staged for the Nov-7 00:00 UTC GPU-quota refresh (post-lock validation vehicle).
- `arc26-nvarc-v45s-solo.ipynb` — the quota-endgame derivative actually submitted Nov-1:
  the 12h NVARC starter run removed, cell-1 safety-net base (identity/flip) retained, and the
  PROVEN 27B direct leg (cells 31–33, byte-identical 33.89-port stack) improving attempt_2,
  fail-open at a 1.6h rerun kill. Commit box 40 min. Merge contract untouched (32/37 cells
  byte-identical to v44).
- `today_build.json` — the day's decision ledger entry.
- `finals_selection_receipt.json` — the Nov-2 finals-selection decision (clicks + ratification).
- `scripts/` — the v45s builder, the finals selection engine, and the live quota gate.

Key facts (Nov-1): classical DSL legs solve 0/120 eval tasks (ARC2 is model-agent territory);
locked finals refs 56842535 (32.64) + 56901303 (31.81); weekly GPU quota exhausted on both
team accounts (refresh Nov-7 > competition lock), which is what forced the v45s solo shape.
