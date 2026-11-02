# 32 — Keyword workflow and daily/weekly routines (operating system v2, 2026-10-08)

Supersedes the cadence parts of `docs/26-workflow-os.md`; the funnel and gate rules there still hold.

## 1. Keywords (runbooks in `agents/keywords/`)

`status` · `submit` · `plan` · `agent inside` · `agent outside` · `analysis` · `research` · `search`. Each runbook says
what to read, what to run, what to write, and where. Scripts live in `scripts/kw/` and need only environment variables:

| variable | account | used by |
|---|---|---|
| `KAGGLE_API_TOKEN_A` | dasshovon | `--account A` |
| `KAGGLE_API_TOKEN_B` | kragglenote2forwork | `--account B` |
| `HF_TOKEN` | Nabidnur | HF mirroring (append-only) |

Tokens are never written to any file in this repo. Add them as environment secrets of the cloud environment (settings →
Edit → Network secrets / environment variables) so Routines pick them up; a session without them does the CPU-only parts and says so.

| script | keyword | what |
|---|---|---|
| `kw_status.py --account A/B` | status | submissions + scores, slot state, LB cutoffs, our ranks; refreshes `analysis/submission_ledger.csv` |
| `kw_submit.py --account X --kernel o/s --version N --reason "..."` | submit | guarded submission (slot free, kernel COMPLETE, registration verified) + `reports/kw/submit_log.jsonl` |
| `kw_family.py --target T` | plan / agent inside | μ/σ/n per configuration family from the ledger + `analysis/config_families.json`, P(draw ≥ T) |
| `kw_pergame.py label=benchmark.json ...` | agent inside / analysis | per-game levels/score/actions/efficiency side by side |
| `kw_sweep_kernels.py --topk 40 --days 2` | research | kernel listing, pulls new/re-run notebooks, isolates each fork's delta vs the M2S base, digest |
| `kw_sweep_discussions.py --since D` | research | incremental forum sweep via the internal API, digest of new/updated threads |

## 2. Daily cycle (Routine "ARC-AGI-3 daily cycle", 00:20 UTC = 06:20 Dhaka)

1. `status` both accounts. 2. `submit` per `analysis/next_submission.json` (date must match; else highest-μ redraw and say so).
3. `research` quick (kernels + forum). 4. If a score landed: `agent inside` → `analysis`. 5. `plan`: write tomorrow's
`next_submission.json` (variance default; experimental version only if its REGISTER gates are recorded as passed).
6. `reports/kw/daily_<date>.md` (≤ 40 lines) + `analysis/results.md` row. 7. Commit + push to the campaign branch; draft PR.

Submission workflow for any NEW version (engineering engine): CPU tests → (serving changed?) ≤ 40-min GPU smoke on 3–5 games
→ paired local comparison with P(Δ > 0) ≥ 0.90 or a single-layer thesis → placeholder commit (RUN_FULL gate, ~33 s) → submit on
ONE account while the other redraws. Never two changed layers; never a version that is not COMPLETE.

## 3. Weekly close (Routine "ARC-AGI-3 weekly close", Sunday 02:13 UTC)

`agent outside` (three outsider memos) → `research` deep (blog, arXiv, GitHub, HF) → `analysis` (refresh the layer table in
`docs/09` §3/§9) → `plan` (7-day calendar `analysis/plan_<date>.md`, REGISTER verdicts, MISTAKES) → mirror digests to HF
`Nabidnur/arc-agi-3-research/weekly/<date>/` (append-only) → commit + push + draft PR → ≤ 15-line report.

## 4. Repo map after today

```
docs/31-research-day-2026-10-08.md   the plan; docs/32 this file; docs/09 §9 corrections; docs/10 §2 new rows
agents/keywords/                      runbooks (README has the table)
scripts/kw/                           the six scripts + common.py
analysis/config_families.json         families (edit when a new config is submitted)
analysis/next_submission.json         tomorrow's instruction (rewritten daily by `plan`)
analysis/submission_ledger.csv        append-only, auto-refreshed by `status`
analysis/public25_reference_m2s.md    per-game base reference (skarin audit)
analysis/teardowns/<date>/            subagent teardowns of public notebooks
references/sweeps/<date>/             pulled notebooks' deltas (ipynb gitignored) + digest
research/discussions/                 forum topics.json + raw/<id>.json + digest_<date>.md
reports/kw/                           status/submit/daily/inside/analysis artifacts
```
