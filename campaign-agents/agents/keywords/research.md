# keyword: research (daily quick / weekly deep)

Daily (≤ 30 min, CPU):
1. `python scripts/kw/kw_sweep_kernels.py --account B --topk 40 --days 2` → `references/sweeps/digest_<date>.md`. Read the digest; for every notebook that is new or re-run AND whose author's LB score ≥ 30, read its `delta_cells.txt` and add 5 lines to `analysis`.
2. `python scripts/kw/kw_sweep_discussions.py --account B --since <yesterday>` → `research/discussions/digest_<date>.md`. Flag host/admin posts, rule changes, infra incidents (queue, dataset mounting, image changes), and any score-mechanics claims.
3. LB deltas: from `status` — who entered the top 20, who jumped > 5 points; note their public notebooks if any.

Weekly deep (Sunday, ≤ 3 h):
4. arcprize.org blog + docs changelog; arXiv (`ARC-AGI-3`, `interactive world model`, `agent harness`); GitHub search for new ARC-AGI-3 repos by top teams; HF for new Flash-Next quantizations / drafters / pruned variants and trajectory datasets. Write `research/weekly/<date>.md` with one adopt/test/ignore verdict per item.
5. Mirror the week's digests to the HF dataset `Nabidnur/arc-agi-3-research` (append-only, `weekly/<date>/`).
