# `campaign` — runbook

Run one competition's whole day (the super agent). Say `arc2 campaign` or `arc3 campaign`. Runbook of the super agent: `agents/super/ARC2.md` / `agents/super/ARC3.md`.

1. `status` both accounts; read `analysis/next_submission.json`, yesterday's `reports/kw/daily_*.md`, `experiments/REGISTER.md` open tickets.
2. `submit` per the policy file (guards; prediction recorded). One per account per UTC day.
3. `research` quick (sub-agent): new notebooks / threads since yesterday; 5-line verdict per item that scores ≥ 30 (ARC-2) / ≥ 25 (ARC-3).
4. Engineering ticket of the day (sub-agent `build`): CPU → small GPU → gate. Never a GPU run > 40 min (ARC-3) / never two ARC GPU kernels at once.
5. When scores land: `validate` → `agent inside` → `analysis`.
6. `plan`: tomorrow's `next_submission.json` (decision table in `CAMPAIGN_OS.md` §4), `writeup/<date>.md`.
7. `reports/kw/daily_<date>.md` (≤ 40 lines), commit, push, draft PR if none. Report ≤ 12 lines.
