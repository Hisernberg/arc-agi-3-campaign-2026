# ARC-AGI-3 audit — 12 October 2026

The strongest reproducible account-B family in the recovered campaign is the full Flash-Next Franzen Milestone-2 harness with the guarded D-prime scheduler. The archived best on `kragglenote2forwork` is **33.50**; its later v2d reproduction scored **30.35**. The supplied **36.89** leaderboard row is a separate team/account result and must not be used as account B's validated baseline. No new GPU play or submission was made in this audit.

The immediate submission recommendation is a fresh-status-checked redraw of the existing COMPLETE **`kragglenote2forwork/arc26-b-dprime-v2d`, version 2**, not a large new stack. A frozen local notebook with the same code is in [candidates/arc3_v2d_reproduction.ipynb](candidates/arc3_v2d_reproduction.ipynb). Its code hash and score/version binding are in [reproduction_manifest.json](candidates/reproduction_manifest.json). It is preparation, not proof that another draw improves the score.

## Evidence recovered and checked

| Evidence | Coverage | What it establishes |
|---|---:|---|
| Local Downloads and recovered campaign notebook/script exports | 294 artifacts, 152 distinct code hashes, 5,616 cells | Source inventory, duplication, cell hashes and Python syntax; not manual semantic review of every line |
| Archived official submission ledger | 42 rows, 41 scored COMPLETE rows, 28 exact account/version groups | Account-specific history; coverage can end earlier than newer live account records |
| Old DGX Qwen3.6 play results | 7 result files, 151 game-run rows | Actual historical play, mostly zero or very low scores; not the current Flash-Next baseline |
| Public game dossiers | 25 games, 183 levels | Published replay/summary provenance and missing-mechanic labels; these are external research, not our new game runs |
| Existing checked-helper and result-collector CPU contracts rerun today | **27/27 pass, 2.940 s** | Real isolated-child retention, game isolation, failure handling and score-accounting contracts |
| Existing October CPU archive | 22 helper + 5 collector contracts; scripted 25-game lifecycle | ARM portability and one-action integration; archive explicitly reports **zero model runs** and `score_qualification=false` |

The source inventory handles actual nbformat notebooks, Kaggle `sourceNullable` exports and one plain Python script archived with an `.ipynb` suffix; [unparsed_notebooks.csv](evidence/unparsed_notebooks.csv) has no remaining failures. Notebook magics are distinguished from Python, and the prepared candidate's 15 code cells were parsed after IPython transformation and validated with nbformat. No notebook cell, downloaded pickle or model was executed during inventorying.

See [local_notebooks.csv](evidence/local_notebooks.csv), [local_cells.csv](evidence/local_cells.csv), [submission_summary.json](evidence/submission_summary.json), [exact_version_draws.csv](evidence/exact_version_draws.csv), [historical_runs.csv](evidence/historical_runs.csv), and [checked_helpers_cpu.log](evidence/checked_helpers_cpu.log).

The root agent also retrieved the selected notebook and saved outputs from Kaggle during this session. [live_verification.json](live_verification.json) records an independently recomputed matching code hash, all 15 transformed code cells and notebook schema passing, the same script-version submission recorded COMPLETE at 30.35, the expected three-game smoke, recomputed decode bins, and the downloaded `submission.parquet` read-back. Its raw-output gate passes for a frozen saved-version reproduction. Authenticated account, current slot, quota accounting and tomorrow's date lock remain runner gates. Saved smoke outputs are dated 10 October; downloading them today does not create a new GPU run.

## Submission history that matters

| Account | Exact artifact / version evidence | Archived score(s) | Reading |
|---|---|---|---|
| kragglenote2forwork | clean D-prime v1, script version 356647589, ref 56994560 | **33.50** | Best account-B draw; only one draw of this exact version in the recovered ledger |
| kragglenote2forwork | v2d v2, script version 357087759, ref 57056539 | **30.35** | Same scored policy plus mount resolver; safest recent COMPLETE artifact |
| kragglenote2forwork | D-prime v2b, script version 356821145 | **24.50** | Added robustness pack; regression is an observation, its cause is unresolved |
| kragglenote2forwork | Fable & Astra, script version 355830078 | **27.17, 29.21** | Exact-version redraw spread 2.04; cannot attribute a gain from a single draw |
| kragglenote2forwork | super-v2, script version 355067286 | **25.84, 26.66** | Multiple simultaneous flags; does not identify their separate effects |
| dasshovon | super-v3 slug, earlier script version 355067303 | **27.38, 27.67** | Compare the immutable version, not the reused slug |
| dasshovon | Fable + D-prime | **20.77** | Bundle performed poorly; interaction versus random variation unresolved |
| kragglenote2forwork | older SheetU exact version 353208764 | **3.18, 4.07, 4.54** | Large Milestone-2 transition exceeds ordinary small redraw changes, but changed model/runtime/harness together |

The recovered campaign separately snapshots `dasshovon`'s later leaderboard best **32.05**, while its central CSV ends earlier. That later snapshot is broader than the CSV; neither is live verification today. Preserve that coverage gap. The user-referenced ARC-AGI-2 ~32.64 is a different competition and is owned by the ARC2 audit.

## Engineering anatomy of the selected notebook

The selected notebook has the 498,799-character Franzen source patch, the full W4A16 Flash-Next model, its dedicated drafter, SGLang NEXTN speculative decoding and a guarded D-prime slot-priority module. Its model-visible policy uses temperature **0.7**, thinking enabled, `reasoning_content` history, a 12,288-token request output ceiling, 2,048-token fairness yields, a 128 Ki analyzer context and 58 Ki context drain. It carries eligible functions across a game, imports permitted by the retention layer, current-grid and difference images, animation information, death differences, and stale-state/batch-no-op guards starting at level 2. The explicit world-model sections are **off**. Its host permits ten active model streams even though the benchmark can enqueue 120 game workers on the scored branch.

The commit branch selects **ft09, sc25, re86** and plays for eight minutes per game; the scored rerun uses the live gateway inventory and the historical 532-minute per-game cap. This is why a 20–30-second commit artifact, a CPU pass, or a three-game smoke is not a score estimate. Public validation and hidden scoring are different execution branches. Preserve both and inspect them separately.

The archived v2d smoke completed in **1,083 s**, including **532 s** before serving became ready, then produced **241 actions, nine cleared levels, zero crashes** across those three games. The log's ten-stream policy is a configured admission ceiling; only three games were active in this smoke, so it does **not** measure full ten-stream throughput. Archived prefix reuse was **94.2%** and aggregate completion throughput **279 tokens/s** for that particular smoke. These observations support a breakage check, not expected hidden-game performance.

Fresh raw-output inspection reproduces all 513 decode lines, with one, two or three active requests and mean aggregate rates 251.3, 302.7 and 317.5 tokens/s respectively. The reported 1.062 headroom ratio is analytic, and the ≥12-stream comparison has zero samples: the optimization comparison is inconclusive despite the printed `B_THROUGHPUT_GATE PASS`. Cache arithmetic matches the reported 94.2%, but the underlying request JSONL was outside the selected download, so its token accounting is harness-reported. Nonfatal `wrapt` startup warnings and recoverable Python-tool errors appear in the saved logs; zero crashed games does not mean zero errors. The 2,648-byte parquet is a schema-verified placeholder; actual competition performance comes from the live-game rerun, not its one row.

## Which layers are supported, uncertain, or risky

**History serialization already has a concrete correctness lesson.** The older local DGX fixture reproduced a backend mismatch: a template read `reasoning_content` while the stock message used `reasoning`, dropping that field. This is a reproducible serialization defect, not a measured score gain. The selected v2d already sends `reasoning_content`, so applying the same fix again buys nothing. Verify request rendering on any new backend before comparing models.

**Function persistence is not a persistent REPL.** The current source starts a fresh isolated interpreter for each Python snippet and reconstructs eligible functions/imports. Ordinary variables and arbitrary mutable objects are discarded. Its game lifetime and checked-helper contracts are valuable existing assets. A real persistent REPL is a separate behavior change: bound memory, clean state on new game, kill/restart on timeout, record effects of partially executed actions, and revalidate level-dependent caches. Do not label today's harness a full persistent session or replace isolation without tests and equal-time play.

**Animation and death views are part of the strong baseline, but their marginal score effects are unmeasured.** A final board can equal the prior board while the intervening animation reveals an interaction. Conversely, an image composite is not an actual game state. Keep provenance labels, and do not use fixed border masking when a border might carry useful mechanics or budget information.

**D-prime is an understood, usable baseline; a causal improvement is unproved.** The account-B pair {33.50, 30.35} spans related versions, not an exact-version controlled experiment. External notebook-page maxima, model variants, and different authors' draws are not interchangeable observations from one random variable. Keep the scheduler because this account has usable artifacts and clean diagnostics, not because a mixed-family p-value establishes a gain.

**Aggressive stacking has adverse observations and attribution failure.** The Fable+D-prime bundle's 20.77 and robustness-pack draw's 24.50 justify caution. They do not establish that any single component causes a fixed -9 or -7 effect. Full-model to pruned-model transfer and higher stream counts must be tested under the same time and concurrency; successful familiar public games do not validate unseen games.

**Planning and search require a verified transition model.** MCTS/BFS/A* over an incorrect, camera-relative or hidden-state-incomplete simulator can consistently choose wrong actions. The LLM should propose rules and discriminating probes; exact code should handle parsing, symmetry, shortest paths and constraint solving once predictive checks pass. Search-budget caps and mismatch-triggered cancellation are necessary. A recorded path replay only proves the original path still executes; it cannot score the different future path an unrun prompt would induce.

**Long thoughts are a measurable resource target, with a tradeoff.** Recovered E-138 research reports 21/328 analysis steps at ≥8k generated tokens, carrying 28.9% of generated tokens; 11 of those steps occurred in levels later cleared. A lower request ceiling touches little of the total token budget because stalls include multiple requests. A hard per-step cap can lose productive reasoning. The small existing `ARC3_PREFER_TOOL_CALLS` bullet is therefore prepared as an unrun, one-change experiment in [arc3_e138_prompt_screen.ipynb](candidates/arc3_e138_prompt_screen.ipynb), not promoted as tomorrow's improved submission.

## Corrections to earlier campaign analysis

1. Do not treat maxima on public notebook pages as mean draws or compare them directly to own individual submissions. Save immutable version IDs and per-draw results.
2. Do not write "the only causal effects are negative" from single-knob, single-draw public comparisons. Their signs and sizes are associations; sampling uncertainty, version uncertainty and runtime changes remain.
3. A soft-end infrastructure pack's one +2.8 draw does not prove that soft ends cost no levels. A low score does not prove a 15-minute inactivity kill occurred. Confirm current host rules and record gateway inter-call gaps before diagnosing censoring.
4. Rejecting a family on any draw below μ−2 is not a statistical regression test when quoted run-to-run σ is around 3.9. Preserve catastrophic-crash rejection, and compare repeated controls for performance decisions.
5. CPU replay cannot measure a changed LLM prompt's level gains. Use it for deterministic action semantics, attribution, lifecycle, and trace extraction. New policy quality needs real paired play.
6. Public game guides, provider-adapter full clears, code-informed synthetic trajectories and later levels of a training game have different generalization claims. Keep these labels visible in the write-up.
7. The current instruction supersedes the old automatic dates embedded in the repo: prepare today, recommend tomorrow's authorized run, and let the root workflow resolve the one-shot schedule. The old repo's `mode=auto` is historical state, not authority to submit today.

## Public-game analysis

[game_dossiers.csv](game_dossiers.csv) covers all 25 public games; [level_dossiers.csv](level_dossiers.csv) covers all 183 levels. Each row records the public build, replay provenance, published observation, missing mechanism, source stock success profile and proposed generic intervention. Family labels are analyst inferences. No game-ID lookup or replay sequence is added to the submission agent.

The strongest common failure categories are **camera versus world coordinates**, **coupled object state**, **inventory/order and hidden variables**, **full-shape collision**, **device/program semantics**, and **timing/animation**. Representative diagnostic games are bp35/lf52/ls20 for scrolling and attributes; sk48/g50t for order and coupled timing; ft09/vc33 for efficient symbolic computation. The public provider examples clear all levels under max/low, but that is evidence about those external models and public environments, not that our resource-constrained Flash-Next agent solves them or unseen games.

The exact summary assignment rule matters: assign an action and its note to the previous record's completed-level count plus one, then apply the new completion counter. Exclude the initial RESET. A clearing action belongs to the level it solved. Positive counters associated with compaction are not a causal estimate of thinking effort.

## Sources

Primary local evidence: recovered `Hisernberg/arc-agi-3-campaign/analysis/submission_ledger.csv`; `reports/kw/status_kragglenote2forwork_2026-10-11.json`; `track-b/2026-10-10/kernel-v2d/{BUILD.md,arc26-b-dprime-v2d.ipynb}`; `track-b/2026-10-10/smoke_v2d.md`; `track-b/2026-10-11/E-138_lever_c.md`; local `/home/urad/arc3_reasoning_ab/reasoning_defect_dgx.json` and October lifecycle/CPU receipts.

Public primary source for the game/level dossiers: [sonpham-org/arc-3 at 30656a0](https://github.com/sonpham-org/arc-3/tree/30656a0), especially `docs/static/research/astra-learning-guide.json`, `astra-max-sources.json`, `astra-low-none-sources.json`, and `docs/static/data/stuck-levels.json`. The public notebook/paper/discussion coverage is maintained separately by the outside-research agent; all private winning recipes remain unknown unless a source discloses them.
