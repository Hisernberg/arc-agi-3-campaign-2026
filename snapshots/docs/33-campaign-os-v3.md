# Campaign OS v3 — two competitions, one operating system (2026-10-10)

Scope: **ARC-AGI-2** (`arc-prize-2026-arc-agi-2`, closes 2026-11-02 23:59 UTC) and **ARC-AGI-3** (`arc-prize-2026-arc-agi-3`), both on Kaggle,
both driven on **account B = kragglenote2forwork only** (user instruction 2026-10-10: account A = dasshovon is never touched by this campaign, in either competition), one submission per UTC day, public LB = max() over the account's submissions. Repos: `Hisernberg/arc-agi-2-kaggle` (ARC-2) and `Hisernberg/arc-agi-3-campaign` (ARC-3). This file is identical in both.

The purpose of the OS is simple: **every UTC day, each competition gets one gated submission on account B, and every submission is a
pre-registered, measured experiment** that feeds the next version and the final write-up. The two competitions think separately (different
agents, ledgers, plans) and share techniques through one cross agent.

## 1. Agent roster

Two **super agents** (one per competition) run the day. Each spawns the sub-agents below as needed (they are prompts/runbooks under
`agents/`, executed as subagents by the session or Routine that runs the day).

| Agent | Keyword | Role | Reads | Writes |
|---|---|---|---|---|
| **Super agent ARC-2 / ARC-3** | `campaign` | runs the daily loop end to end, decides the day's submission, delegates, reports | everything below | `reports/kw/daily_<date>.md`, `analysis/next_submission.json` |
| Research | `research` | new public notebooks (cell-level delta vs our base), forum, arcprize blog, arXiv, HF/GitHub; verdict adopt/test/ignore per item | sweeps, digests | `research/sweeps/<date>/`, `research/discussions/`, `research/weekly/` |
| Analysis (inside) | `analysis`, `agent inside` | our results: per-task (ARC-2) / per-game (ARC-3), per-family μ/σ, what each layer did | ledgers, rerun logs | `reports/kw/inside_<date>.md`, `reports/kw/analysis_<date>.md`, `analysis/config_families.json` |
| Build (coding) | `build` | turns one ticket into a notebook version through the funnel (§3) with gates and receipts | plan, REGISTER, kernel text | `kernel-v<N>/`, `experiments/REGISTER.md` rows, gate receipts |
| Invent (outside the box) | `invent` | new mechanisms, architectures, selection/anchoring ideas; each with mechanism, cost, falsification test | plan, outsider memos, cross notes | `agents/invent/<date>.md` |
| Solve (categorize + anchor) | `solve` | task/game categorization, per-category budget and selection rules, exact-verified families / rule priors | data, pools, histories | `analysis/categories/`, family/prior code |
| Validate (outsider) | `validate` | after scores land: prediction vs result verdict per submission; did the code change move the score or was it a redraw? | submit log, ledger | `reports/kw/validate_<date>.md`, REGISTER verdict rows |
| Outsider board (A/B/C) | `agent outside` | weekly outside-view memos (systems sceptic, adversarial strategist, cognition detective) | context pack | `agents/outsider/weekly/<ISO-week>-{A,B,C}.md` |
| Steward | `submit`, `status` | guarded submission (slot free, version COMPLETE, gate PASS, prediction recorded) and live state | policy file | `reports/kw/submit_log.jsonl`, `analysis/submission_ledger.csv` |
| Write-up | `writeup` | captures engineering/research value daily (method, measurement, negative result, figure to make) | all of the above | `writeup/<date>.md`, `writeup/INDEX.md` |
| Cross | `cross` | transfers techniques between the two competitions (§5) | both repos | `agents/cross/<date>.md` |

## 2. Daily loop (UTC)

| Time | ARC-3 (B only) | ARC-2 (B only) |
|---|---|---|
| 00:05–00:30 | `status` → `submit` per `analysis/next_submission.json` (fallback rule inside the file) | `status` → `submit` per `analysis/next_submission.json` (B at 00:35) |
| 00:40–12:00 | `research` quick → day's engineering ticket: CPU → ≤ 40-min GPU smoke → gate | `research` quick → day's ticket: CPU (pools, families, offline A/B) → on commit days (Sat after the quota refresh, or when ⅓ pool is free) a 1-h commit → gate |
| 14:30 | `validate` (scores landed? verdicts into REGISTER) → `agent inside` → `analysis` | same |
| 20:00 | `plan` writes tomorrow's `next_submission.json` + `writeup/<date>.md` | same |
| Sun 02:13 (ARC-3) / Sat 01:00 (ARC-2) | weekly close: `agent outside` → `research` deep → `analysis` → `plan` (7-day calendar) | weekly commit day: build → commit → gate → submit |

Rules: one submission per account per UTC day, never skipped (LB = max(), a "Kaggle Error" is free); submit early (queues run 24–36 h);
never two ARC GPU kernels at once on one account; never a GPU run > 40 min on ARC-3 outside the weekly big run; ARC-2 commits cost ≈ ⅓ of
the weekly L4×4 pool each.

## 3. Submission funnel (how a new version becomes eligible)

| Stage | ARC-3 | ARC-2 | Gate to pass |
|---|---|---|---|
| 0 desk | ticket in `experiments/REGISTER.md`: hypothesis, mechanism, predicted band, kill criterion | same | reviewer (super agent) accepts; at most ONE unmeasured model-visible change per version |
| 1 CPU | nbformat + AST + use-before-import + cross-cell names + mount audit; D′ simulator / per-game sim where applicable | same static checks + offline paired eval on saved candidate pools (295 labelled candidates, v6full pools) or train-1000 for families | all static checks green; offline paired result P(Δ > 0) ≥ 0.90 or a single-layer thesis with precision ≥ 0.95 |
| 2 small GPU | ≤ 40-min smoke on 3–5 public games on the RTX (B), serving preflight + smoke gate + throughput probe | 1-h commit (50-min validation) on L4×4; `scripts/gate_v30_output.py` (120 tasks, not the fallback, 4 workers, no traceback, reload line, atlas selftest) | fail-closed gates PASS |
| 3 big run | placeholder commit (RUN_FULL gate) → the scored rerun is the big run | the commit output IS the big run's text; scored rerun = 12 h | version COMPLETE and listed as eligible in `next_submission.json` (never a non-COMPLETE or `ineligible` version) |
| 4 submit / draw | one account draws the new version, the other redraws the best family | same | prediction recorded in `submit_log.jsonl` before submitting |

## 4. Resubmission criteria (decision table, applied by `plan` every evening)

| Situation | Action |
|---|---|
| No new gated version | redraw the family with the highest μ that has a COMPLETE version (variance engine); both accounts |
| New version passed stages 0–3 | submit it on ONE account; the other account redraws the best family; at most one experimental submission per day per competition |
| Score landed for an experimental version | `validate`: if score within predicted band and ≥ family μ − 1σ → version joins its family (n += 1); if < μ − 1σ twice (two draws) → revert to the previous family and log the negative result |
| Version ERRORED / non-COMPLETE / failed gate | never submit; fallback = last gated version; log in MISTAKES |
| Slot refused (pending limit, queue) | retry hourly until 23:50 UTC; never skip the day |
| Scores delayed > 36 h | keep redrawing; do not change versions on hope |
| Quota exhausted | CPU-only day; redraw; no commits |
| Base-model / serving-stack change | only via a probe (stage 2) with a kill criterion; never shipped on an author's LB claim |

## 5. Shared techniques (the cross agent's catalogue)

| Technique | ARC-2 form | ARC-3 form | Status |
|---|---|---|---|
| Categorize the units | R6 semantic families of the 120 eval tasks; hidden pool train-sized | 55 public games in classes (ft/sc/re/sk/lf/sp/ka/cn/ls/su/dc/tn/vc/tu…), level-index weighting | ARC-2 taxonomy exists (HF `solution-methods`); ARC-3 class table in docs |
| Anchored / greedy selection | exact-verified family output = anchor; greedy pick among candidates consistent with anchors; attempt-2 = most-different | D′ slot priority (A·M·C + B·φ) is a greedy allocation; anchor = verified level-advancing action rules | ARC-2: design stage (S6); ARC-3: live (D′) |
| Redraw under max() | per-rerun random aug salt; deterministic only in commit | nondeterministic serving; daily redraw of the best family | live in both |
| Budget by category | per-category caps (train-sized pool), retry pass in the ~1.5 h slack | PACE / TAIL_FADE per game class; soft end 9 h − 9 min | ARC-3 live; ARC-2 v31 |
| Exact programs ↔ rule priors | 17 atlas families (precision 1.0) | action-rule priors from offline engine traces | ARC-2 live; ARC-3 ticket |
| Fail-closed gates | gate_v30_output.py | preflight + smoke gate + throughput gate | live in both |
| Inside / outside agents | same board | same board | live |

## 6. Keywords (say the word; the runbook in `agents/keywords/<keyword>.md` runs)

`status` · `submit` · `plan` · `research` · `analysis` · `agent inside` · `agent outside` · `search` (existing) ·
**`campaign`** (run the whole day for one competition) · **`build`** (ticket → version through the funnel) · **`invent`** (outside-the-box
ideas with falsification tests) · **`solve`** (categorize + anchor/greedy selection work) · **`validate`** (prediction vs score verdicts) ·
**`writeup`** (capture the day for the paper) · **`cross`** (technique transfer between the competitions).
Prefix with the competition when ambiguous: `arc2 campaign`, `arc3 build E-140`.

## 7. Write-up capture

Every day `writeup/<date>.md` records, per competition: what was submitted and why (with the prediction), what was measured (numbers with
their source), negative results (what did not move the score and the evidence), one figure or table worth making, and the mistake of the day.
`writeup/INDEX.md` lists the themes for the final write-up: variance under max() and the redraw policy; exact-verified program families with
precision 1.0; budget saturation and anytime scheduling; serving-envelope measurements (KV pool, streams, spec steps); fail-closed gates;
cross-competition transfer.

## 8. Routines (where the day runs)

Until the environment carries the secrets, the day runs from the orchestrator session (it holds the credentials in its own scratch space):
ARC-3 daily 00:20 UTC, ARC-2 daily 00:35 UTC, joint `validate` 14:30 UTC, weekly engineering Sat 01:00 UTC, ARC-3 weekly close Sun 02:13 UTC.
Once the user adds `KAGGLE_API_TOKEN_A`, `KAGGLE_API_TOKEN_B`, `HF_TOKEN` as environment secrets and attaches both repositories to the
environment, the same prompts run as fresh-session Routines (independent super agents) and the session-bound ones are disabled.

## 9. Credentials and safety

Credentials only from environment variables or the orchestrator's scratch file; never in files, commits, notebooks, prompts or logs. Never
delete anything on Kaggle, GitHub or Hugging Face. Never push to main. Never touch account A (dasshovon) in either competition. Never submit a version that is not
COMPLETE or failed a gate. One unmeasured model-visible change per version. Report outcomes as they are.

## 10. Modes (added 2026-10-11, user instruction)

| mode | submissions | everything else | how it is set |
|---|---|---|---|
| `auto` (10-10 → 10-12) | the daily routine submits per `analysis/next_submission.json` (one per UTC day, account B only) | runs | default |
| `manual` (from **2026-10-13**) | **none by the campaign**: the policy file becomes the *recommended* hand submission (`"mode": "manual"`), `kw_submit.py` refuses without `--manual-override`, the user submits on Kaggle and says `continue` to return to `auto` | status, research, analysis, engineering (kernel commits + ≤ 40-min gated smokes on B stay allowed), plan, write-up, daily chat report all continue | `plan` writes `"mode": "manual"` into the policy file; the routines carry the same rule |

**Status 2026-10-11 18:25 UTC: the user said "dont submit auto, i will say continue then only you will continue" → `manual` mode from now (policy files carry `"mode": "manual"`, both daily routines skip `submit` and recommend instead, `kw_submit.py` refuses). `continue` from the user returns to `auto`. Hand submissions by the user are picked up by `validate` (they appear in the ledger) and judged like any other draw.**
