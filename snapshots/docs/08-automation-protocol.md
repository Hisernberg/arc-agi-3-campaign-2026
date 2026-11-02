# 08 · Daily Automation Protocol

All automation uses the Kaggle REST API with the team token (stored in `.env`, gitignored).
Secrets hygiene: tokens NEVER committed; rotate if leaked.

## Verified API capabilities (tested 2026-09-19)

| Endpoint | Status | Use |
|---|---|---|
| `GET /api/v1/competitions/{c}/leaderboard/view` (+nextPageToken) | ✅ 200 | leaderboard tracking |
| `GET /api/v1/competitions/submissions/list/{c}` | ✅ 200 | submission history & scores |
| `GET /api/v1/datasets/view/{owner}/{slug}` | ✅ 200 | verify attached datasets |
| `GET /api/v1/datasets/download/...` | ✅ 200 | pull solver bundles |
| `GET /api/v1/kernels/list?user=...` | ✅ 200 (fields sparse) | notebook inventory |
| `kaggle competitions submit -k <kernel> -v <N> -m <msg>` | ✅ verified (CLI 2.x) | **code-comp submission from CLI** — no UI needed |
| `kaggle competitions submission-limits <c>` | ✅ verified | hard daily cap (1/day confirmed 9/19) |
| `kaggle kernels output <kernel>` | ✅ runs, but **empty for our kernels** | run artifacts are NOT retained → trace mining must be local |
| `kaggle kernels status <kernel>` | ✅ verified | watcher poll target (KernelWorkerStatus.*) |
| `POST kernels push / competitions submit` | ⚠️ code-comp submissions need the notebook UI or internal endpoint | daily flow assumes UI submit; API used for version push + monitoring |

## Daily flow (Sat 9/20 onward) — FULLY AUTOMATED as of 9/19

```
nohup bash scripts/watch_and_submit.sh <kernel> <version> > /tmp/watcher-<date>.log 2>&1 &
nohup python3 scripts/finalize_day.py            > /tmp/finalizer-<date>.log 2>&1 &
```

1. `watch_and_submit.sh` — polls `kernels status` every 5 min; on COMPLETE runs
   `kaggle competitions submit -k <kernel> -v <version>` (1 retry); on ERROR exits
   without submitting; then polls the score for up to 24 h.
2. `finalize_day.py` — waits for today's submission row, then (idempotent):
   appends the score row to `analysis/results.md`, applies the decision tree to
   `reports/data-<today>.json` (new-best / in-band / rollback verdict),
   regenerates `reports/<today>-daily-report.pdf`, commits + pushes to GitHub.
3. Morning audit (next session): read watcher/finalizer logs, verify push, pick
   today's variant per docs/07, build + test notebook, push new kernel version.

## Automation scripts in this repo

| Script | Purpose |
|---|---|
| `scripts/kaggle_status.py` | leaderboard + submissions + quota probes |
| `scripts/kaggle_full_subs.py` | full submission history, best score |
| `scripts/kaggle_datasets.py` | dataset availability + own notebook inventory |
| `scripts/analyze_games.py` | 25-game metadata table |
| `scripts/local_play.py` | offline CPU play of any public game |
| `scripts/probe_game_mechanics.py` | systematic per-action probing of all 25 games → mechanics KB |
| `scripts/test_apis.py` | token health checks |
| `scripts/watch_and_submit.sh` | kernel-status watcher → auto-submit → score polling |
| `scripts/finalize_day.py` | post-score close-out: results.md + data JSON + PDF + git push |
| `scripts/build_governor_notebook.py` | builds duck-governor-v1 from production-12 |
| `scripts/build_worldmodel_notebook.py` | builds duck-worldmodel-v1 from production-12 |
| `scripts/test_governor_patch.py` | unit tests vs real bundle modules (governor) |
| `scripts/test_worldmodel_patch.py` | unit tests vs real bundle modules (worldmodel, 10 checks) |
| `scripts/daily_loop.sh` | legacy orchestrator (superseded by watcher+finalizer) |

## Offline engine gotchas (learned 9/19, cost real debugging time)

1. `GameAction` lookup only works by NAME item access: `GameAction["ACTION1"]` ✅,
   `GameAction(1)` ❌ (raises despite `.value == 1`). Build `{m.value: m for m in GameAction}`.
2. Frame grids live in `fd.frame` — a LIST of numpy arrays (one per animation
   frame). `fd.grid` does not exist. Use `fd.frame[-1]` as the post-action board.
3. `fd.available_actions` items are plain INTs (enum values), not members.
4. **Coordinate-dependent engine crashes**: clicking certain cells (e.g. m0r0,
   tn36) raises inside the game's `step()`; `env.step()` returns `None`. Always
   null-check the frame after a step; treat as a failed probe + reset.
5. `LocalEnvironmentWrapper` needs a `scorecard_id`; OFFLINE mode + local
   environments_dir is the GPU-free dev loop.

## Rules encoded

1. **One new variant per day**; submission cap is **1/day** (verified via submission-limits). Variance averaging = re-submit the same version on a later day (see docs/07).
2. **GPU exhausted → resubmit best existing version** (identify via `kaggle_full_subs.py` best; resubmitting a version consumes the daily slot).
3. **No submission before local dry-run passes** (offline engine + unit tests).
4. **Every score lands in `analysis/results.md`** with config fingerprint (git SHA of
   harness patch + env profile name) — no untracked experiments.
5. **Rollback**: if a variant scores < best − 1.0 on both submissions, revert to best
   config next day and record hypothesis in notes.

## Kaggle CLI bootstrap (for version push)

```bash
pip install kaggle --quiet
cat > ~/.kaggle/kaggle.json <<EOF
{"username":"kragglenote2forwork","key":"$KAGGLE_TOKEN"}
EOF
chmod 600 ~/.kaggle/kaggle.json
kaggle kernels push -p notebooks/duck-governor-v1/   # kernel-metadata.json required
```

`kernel-metadata.json` template (competition attachment required):

```json
{
  "id": "kragglenote2forwork/<slug>",
  "title": "<title>",
  "code_file": "<notebook>.ipynb",
  "language": "python",
  "kernel_type": "notebook",
  "is_private": "true",
  "enable_gpu": "true",
  "enable_internet": "false",
  "dataset_sources": ["keithtyser/duck-qwen38-nvfp4-mtp-vllm-smoke-v1",
                      "keithtyser/qwen38-flash-next-vllm-nvfp4-runtime-v1"],
  "competition_sources": ["arc-prize-2026-arc-agi-3"],
  "kernel_sources": []
}
```

⚠️ GPU accelerator type (RTX 6000) must be set once in the notebook UI; verify after each
push (community reports of P100 fallback: discussion 738602).
