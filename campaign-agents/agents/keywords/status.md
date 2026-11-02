# keyword: status

1. `python scripts/kw/kw_status.py --account A` and `--account B` (skip an account whose token env var is missing; say so).
2. Read the printed block: best score, today's slot used?, pending submissions, LB cutoffs (rank 1/10/20/50/100), our ranks.
3. Compare with yesterday's `reports/kw/status_*_<yesterday>.json`: new scores → append to `analysis/results.md` (date, account, ref, config family, score, Δ vs family μ).
4. If a submission errored (status ERROR / error_description non-empty): record it in `docs/10-bugs-setbacks-lessons.md` §2 with the cause once known.
5. Output: a 6-line summary (A best/rank, B best/rank, cutoffs, what scored since yesterday, slot state, anomalies).
