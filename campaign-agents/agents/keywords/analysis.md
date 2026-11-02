# keyword: analysis — which layer helps, which hurts

1. Evidence sources: our ledger + families; public notebooks' deltas (`references/sweeps/<date>/*/delta_cells.txt`) joined with their authors' LB scores (`references/sweeps/listing_<date>.json` + LB CSV); the base author's ablations (`notebook-intel/da-fr/WRITEUP.md` §6); the catalog (`docs/09-techniques-catalog.md`).
2. Build/refresh the layer table (L0 serving, L1 model, L2 context/memory, L3 perception, L4 guards, L5 allocation, L6 prompting, L7 algorithmic/world-model, L8 evaluation): for each mechanism → where it is proven (🟢/🔵/🟡/🔴), effect size with n, and whether it is ON in our shipped kernels.
3. Variance discipline: a single draw never moves a verdict; a mechanism is "helps" only with paired evidence (same games, same budget, n ≥ 2 per arm) or an author-run ablation; otherwise it stays "unknown".
4. Cell-by-cell for any notebook whose author's LB score ≥ our best: isolate its delta vs the M2S base (the sweep already does this), read it, and write 5 lines: mechanism, layer, flags, evidence, verdict.
5. Output `reports/kw/analysis_<date>.md` + update `docs/09-techniques-catalog.md` §3 rows that changed. The doc must end with "top 3 layers to touch next" and "top 3 layers NOT to touch".
