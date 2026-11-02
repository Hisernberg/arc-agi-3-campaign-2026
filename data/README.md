# data/ — machine-readable ledgers

| File | Contents | Source |
|---|---|---|
| `ledger_unified.csv` | 107 submissions, both lanes, Oct-04/Aug-10 → Nov-02 2026 (lane, date, ref, score, status, kernel, version, description) | Kaggle submissions API pulls 2026-11-02 + the Oct-26 snapshot merge |
| `farm_draws.csv` | The blackbox same-config eislab farm (6 draws) | API-verified |
| `constellation_final.csv` | Final top-of-board reference rows incl. our 35.53 | API-verified |
| [`../snapshots/data/all_subs.json`](../snapshots/data/all_subs.json) | 250-submission snapshot as of Oct-26 (gold lane) | private campaign repo |

Regenerate figures from `ledger_unified.csv` — the pack in [`../figures/`](../figures/) was
produced exactly this way (matplotlib; scripts described in `../code/`).
