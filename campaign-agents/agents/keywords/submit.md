# keyword: submit — execute today's draw (00:05–00:30 UTC)

1. Read `analysis/next_submission.json` (written by yesterday's `plan`). Example:
   `{"date": "2026-10-09", "A": {"kernel": "dasshovon/arc26-m2top-v1", "version": 1, "reason": "..."}, "B": {...}}`
2. For each account with a token: `python scripts/kw/kw_submit.py --account X --kernel <k> --version <v> --reason "<reason>"`.
   The script refuses if today's slot is used, if the kernel is not COMPLETE, or if the submission did not register.
3. If the policy file is stale (date ≠ today) do NOT guess: submit the account's highest-μ family redraw per `kw_family.py` and say so.
4. Append the outcome to `analysis/results.md` (pending row) and `reports/kw/submit_log.jsonl`.

> **Mode key (2026-10-11):** `analysis/next_submission.json` may carry `"mode": "manual"` (from 2026-10-13, user instruction). In manual mode the file is the *recommended* hand submission: `plan` still writes it every evening with kernel/version/predicted band/reason, `submit` is skipped by the routines and `kw_submit.py` refuses without `--manual-override`; the user submits on Kaggle and says `continue` to return to `auto` (remove the key or set `"mode": "auto"`).
