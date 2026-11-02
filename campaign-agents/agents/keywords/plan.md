# keyword: plan — learn from every submission, then decide the next ones

Inputs: `analysis/submission_ledger.csv`, `analysis/config_families.json`, `analysis/results.md`, `docs/10-bugs-setbacks-lessons.md`,
`experiments/MISTAKES.md`, latest `reports/kw/analysis_*.md`, latest `references/sweeps/digest_*.md`.

1. `python scripts/kw/kw_family.py --target <current top-20 cutoff>` — μ/σ/n per configuration family, P(draw ≥ target).
   Add every new scored submission to its family in `config_families.json` first (members = refs; external = public draws of the same code).
2. For each scored submission since the last plan: was it inside its family band (μ ± 1σ)? If below μ − 1.5σ, it is a suspect run (serving failure, early termination, infra) → `agent inside` must grep the rerun evidence before anyone changes code.
3. Mistakes pass: anything that cost a slot, a GPU hour, or a day → one row in `experiments/MISTAKES.md` with the gate that prevents recurrence.
4. Decide tomorrow per account (write `analysis/next_submission.json`):
   - **Variance engine (default)**: redraw the highest-μ family that has a COMPLETE version on that account.
   - **Engineering engine**: a new version is submitted only if it passed CPU tests + a ≤40-min GPU smoke + a paired local comparison (same games, same budgets) with P(Δ>0) ≥ 0.90 or a single-layer change with a written thesis. Never two changed layers at once.
   - One account may carry the experiment while the other keeps redrawing the best family (never both experimental on the same day).
5. Weekly (Sunday): 7-day calendar in `analysis/plan_<date>.md` — per day: account A action, account B action, engineering item, GPU budget (≤ 40 min per big run, ≤ 3–4 big runs/week), what evidence would change the plan.

> **Mode key (2026-10-11):** `analysis/next_submission.json` may carry `"mode": "manual"` (from 2026-10-13, user instruction). In manual mode the file is the *recommended* hand submission: `plan` still writes it every evening with kernel/version/predicted band/reason, `submit` is skipped by the routines and `kw_submit.py` refuses without `--manual-override`; the user submits on Kaggle and says `continue` to return to `auto` (remove the key or set `"mode": "auto"`).
