# Keyword runbooks — the campaign's operating vocabulary

Say the keyword to a session (or the daily/weekly Routine says it) and the matching runbook is executed end-to-end.
Every runbook is CPU-only unless it says otherwise, reads credentials only from environment variables
(`KAGGLE_API_TOKEN_A` = dasshovon, `KAGGLE_API_TOKEN_B` = kragglenote2forwork, `HF_TOKEN`), and ends by writing its
artifact into the repo and committing.

| keyword | cadence | what it does | artifact |
|---|---|---|---|
| `status` | every session start | live state of both accounts + LB cutoffs + ledger refresh | `reports/kw/status_<acct>_<date>.json`, `analysis/submission_ledger.csv` |
| `plan` | weekly (Sun) + after every scored draw | learn from everything we submitted: family μ/σ, mistakes, next-week calendar, next_submission policy | `analysis/plan_<date>.md`, `analysis/next_submission.json` |
| `agent inside` | daily, after scores land | analyze OUR results: per-game, per-family, rerun-log greps, what the draw tells us | `reports/kw/inside_<date>.md` |
| `agent outside` | weekly (Sun) | the three outsider reviewers (A systems sceptic, B adversarial strategist, C cognition detective) brainstorm from outside the campaign | `agents/outsider/weekly/<ISO-week>-{A,B,C}.md` |
| `analysis` | daily (evening) + weekly close | per-game / per-layer attribution of scores across all evidence (ours + public); which layer helps, which hurts | `reports/kw/analysis_<date>.md` |
| `research` | daily (quick) + weekly (deep, Sun) | sweep public notebooks (cell-by-cell delta vs M2S base), forum, arcprize blog, arXiv, HF/GitHub; decode anything that scores | `references/sweeps/digest_<date>.md`, `research/discussions/digest_<date>.md`, `research/weekly/<date>.md` |
| `search` | ad hoc | targeted lookup (a technique, a flag, a paper, a notebook) across the local corpus + web | answer in chat, cached under `research/search/` |
| `submit` | daily at 00:05–00:30 UTC | execute `analysis/next_submission.json` through the guards (slot free, kernel COMPLETE, reason written) | `reports/kw/submit_log.jsonl` |
| `campaign` | daily | run the whole day for this competition (super agent, `agents/super/ARC3.md`) | `reports/kw/daily_<date>.md` |
| `build` | per ticket | ticket → version through the funnel with gates (`docs/33-campaign-os-v3.md` §3) | kernel dir + REGISTER rows |
| `invent` | weekly | outside-the-box mechanisms with falsification tests | `agents/invent/<date>.md` |
| `solve` | weekly | per-game-class categorization, PACE / TAIL_FADE and rule priors | `analysis/categories/<date>.md` |
| `validate` | after scores | outsider verdict: prediction vs score per submission | `reports/kw/validate_<date>.md` |
| `writeup` | nightly | capture the day for the paper | `writeup/<date>.md` |
| `cross` | weekly | technique transfer with the ARC-AGI-2 campaign | `agents/cross/<date>.md` |

Order of a normal day (UTC): `status` → `submit` (00:05+) → `research` (quick) → work on the day's engineering item
(CPU → small GPU → big run) → when scores land: `agent inside` → `analysis` → `plan` (writes tomorrow's
`next_submission.json`) → commit + push.
