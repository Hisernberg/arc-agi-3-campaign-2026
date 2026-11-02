# Super agent — ARC-AGI-3 (`arc3 campaign`)

You run the ARC-AGI-3 campaign's day for repo `Hisernberg/arc-agi-3-campaign`, account **B = kragglenote2forwork only** (never account A for ARC-3). Competition `arc-prize-2026-arc-agi-3`. Credentials: env `KAGGLE_API_TOKEN_B`, `HF_TOKEN` only.

Read first: `docs/33-campaign-os-v3.md`, `docs/32-keyword-workflow.md`, `track-b/<latest>/plan_35-40.md`, `analysis/next_submission.json`, `experiments/REGISTER.md`, `experiments/MISTAKES.md`, yesterday's `reports/kw/daily_*.md`.

Day:
1. `python scripts/kw/kw_status.py --account B`.
2. `submit` per the policy file through `scripts/kw/kw_submit.py` (guards + prediction). Default = redraw of the highest-μ COMPLETE family (D′ v2b lineage) unless a gated experimental version is listed.
3. Sub-agents: `research` quick (`kw_sweep_kernels.py`, `kw_sweep_discussions.py`), `build` for the day's ticket (E-128c envelope probe, behavioural ticket, D′ allocation by game class), `solve` (per-class PACE / TAIL_FADE from smoke histories + `analysis/sim/`), `invent` weekly.
4. 14:30 `validate` → `agent inside` → `analysis` when the score lands (same day usually).
5. `plan`: tomorrow's `next_submission.json`, `writeup/<date>.md`, `reports/kw/daily_<date>.md`; commit; push; draft PR if none.
MODE: `manual` (user, 2026-10-11 18:25 UTC: "dont submit auto, i will say continue then only you will continue"). The routines run status/research/engineering/plan/report; `submit` only recommends; `kw_submit.py` refuses without `--manual-override` (never used by the campaign); `continue` from the user returns to `auto`.
Hard rules: ≤ 40-min GPU smokes, one ARC GPU kernel at a time, fail-closed preflight/smoke/throughput gates, one unmeasured model-visible change per version, never a non-COMPLETE version, anti-F+D rule (two draws + revert).
