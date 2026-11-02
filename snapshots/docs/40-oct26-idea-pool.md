# 40 · Oct-26 IDEA POOL — the great notebook sweep (2026-10-25)

Sweep scope: **718 public notebooks** pulled from `kernels/list?competition=arc-prize-2026-arc-agi-3`
(votes + freshest sorts, 400+400 merged). **30 top notebooks pulled to source** (all OK) into
`artifacts/forks/oct26_sweep/`. **12 deep-mined** (5 parallel mining agents + direct reads).
Leaderboard CSV (4,799 teams) → top-50 personalities cross-referenced.

## 0. The map (who's who, what lineage)

| Rank | Team/Person | Score | Public code | Family |
|---|---|---|---|---|
| 1 | Yi-Chia Chen @ Fields Model | 71.48 | none | ? |
| 2 | Tufa Labs | 68.91 | duck harness base | Duck |
| 3 | Team Turducken | 56.02 | none | ? |
| 16 | Daniel Franzen | 38.85 | **M2 solution (1112 votes)** | M2 (our base) |
| ~51 | AGI Boys (romantamrazov) | 35.35 | the-agi-boys-i-am-better (113v) | M2 fork |
| top-50 | shiiin9/affectify (Osaka Met.) | ~36-37 | **D' notebook 31.54 single sub** | M2 fork (OUR priority donor) |
| 29 | Lord Han Solo (wkdrbwnd1) | 37.07 | eval30 + M2 v293 ref | M2 fork |
| — | mbmmurad | — | LB 0.86 3rd-place milestone: Forge v46 + Gemma-4-31B | Forge |
| — | heliosli | — | AGI Boys + D' merge (121v) | M2 fork |
| — | scottlegrand | — | TAAF flashnext sheetu12b (196v) | Duck fork |
| — | keithtyser/wuliao0/chiakazirim/foysalemonshanto/muhibullahansir | — | duck-qwen3-8 model-swap forks | Duck forks |
| — | poby7722 | — | v47 frontier-graph LLM-free (claims 0.54) | LLM-free |
| — | ashvinsingh | — | FORGE v20 rewrite (242v) | LLM-free |
| — | vyankteshdwivedi | — | hybrid BFS+CNN (100v, "0.39 LB" core) | LLM-free |
| — | pscamillo | — | starter: 5-tier priority + reset-reachability | LLM-free |

**Our champion** `arc26-b-dprime-fix-v1` = dfranzen M2 byte-identical + **shiiin9 D' slot priority**
(cell 23, `D_PRIME` constants, FRESH-first removed) + F-1024/F-1025 capability guard. Anchor **26.47**
(ref 57594680), LB best **33.50**, rank **106/4799**. The whole public top tree branched from the same
M2 root — we are one branch; the sweep tells us what the other branches learned.

**F-1030 root cause (confirmed by source read)**: AGI Boys' env block is an interface contract with
THEIR patch — `ARC3_PRIORITY_TAIL_FADE='1'` raises ValueError without their `configure_clock(deadline)`
wiring; `ARC3_MAX_ACTIVE_STREAMS=10` deadlocks without `_maybe_handover()` trim-point handover. Their
own `install()` validates 6 module attrs for exactly this reason. **Lesson: port mechanisms (code with
hasattr contracts + fail-open), never env blocks.**

## 1. Waste-elimination / guards (highest EV for our stack, all deterministic)

1. **Interior-vs-border `gameplay_changed`** — border-crop (4 cells) comparison separates HUD ticks
   from real progress. [dfranzen M2 #1, ALL forks] → **already in our harness** (shipped ON).
2. **Death ledger + per-position fatal-action blocking** — record (state-hash, action) pairs that
   preceded game_over; block exact replay. [M2 #4; M2-top ships ON] → **in our bundle, OFF** → we flip ON (Oct-26 pack).
3. **Fatal-prefix batch lookahead** (`ARC3_DEATH_GUARD_LOOKAHEAD`) — refuse a whole batch whose
   continuation replays a recorded fatal suffix; "nothing is spent". [M2-top ON] → we flip ON.
4. **No-op repeat guard with block-then-insist override** — refuse repeat but arm one slot; contradiction deletes entry; separate `_armed_noop`/`_armed_death` slots. [M2 #3] → in bundle, shipped OFF (animation false-noop risk); NOTE: leave OFF per author's A/B (keep for future with TAAF soft-tag policy #6).
5. **Proven no-op registry — execute-again-and-tag** (soft policy v3+) — annotate repeats instead of
   refusing; refusals misled the model ("refusals made cn04/g50t misread the harness as the game"). [TAAF F-x]
6. **Batch no-op stop** — stop executing a batch at first inert action; "a wrong movement model costs
   one action rather than the whole sequence". [M2 #5, shipped ON] → already active.
7. **Stale-state latch** — after an inert action, refuse next action in same snippet. [M2 #7, ON] → active.
8. **Guards-from-level=2** — level 1 probes hardest; watch but don't refuse. [M2 #13, ON] → active.
9. **Coordinate-normalized action signatures** — `MOUSE(4,7)` not bare `MOUSE`; "every click share[s] signature 'MOUSE'... 175 replies and one executed action". [M2 #10] → in bundle.
10. **Identical-snippet refusal within a turn** — sha1 of normalized snippet; "46 min, 35 calls, 0 actions" real stall. [TAAF F4] → **we port it (Oct-26 pack W2)**.
11. **3-idle-inspection nudge** — after 3 successful tool calls with 0 executed actions: "execute your current best candidate action now". [duck-anim observer] → future (prompt-injection point needed).
12. **Terminal latch** — after game_over/level_completed no further action() calls; "20 to 30 wasted actions" without it. [M2 #6] → in bundle.
13. **Unswallowable exceptions** (BaseException for KnownNoOp/KnownDeath/Terminal) — "1500 consecutive refusals treated as proof every cell was inert". [M2 #6] → in bundle.
14. **Circuit breakers** — BREAKER_CHECK_CALLS=6/level, 3 diverged plans sever planning, MAX_REPLAN_PER_LEVEL=8. [M2-top UND] → future.
15. **Stall throttle F10** — after 40 stalled steps, sleep the game between steps. [TAAF] → deferred: interacts with our slot-priority gate (a sleeping game holds its slot).
16. **Warmup action vs 15-min Kaggle clock** — first game fires one RESET while the server loads. [M2 #29] → already in our config (`ARC3_WARMUP_ACTION_GAMES=1`).
17. **HTTP retry grace 900s + Retry-After respect + failure circuit breaker (10)** — [M2] → already in config.
18. **Deterministic work budgets, not wall-clock** — "the same action always produces the same line". [TAAF F13b] → design principle we adopt.

## 2. Memory / context (LLM-arm levers)

19. **USER-boilerplate dedup** — 19/23 lines byte-identical across USER turns; -24.5% input tokens → deeper history; only historical copies dropped, newest keeps full contract. [shiiin9 EXP-105] → **ported (Oct-26 pack W1)**.
20. **Keep-notes-on-death** — game_over is a level RETRY, not a new level; wipe only on level_transition/run_complete. [shiiin9 #9, TAAF F3; our bundle knob `ARC3_WM_WIPE_ON_GAME_OVER=0`] → **flipped (Oct-26 pack)** (inert under MEMORY_SECTIONS=off, zero-risk insurance).
21. **Memory sections OFF is a measured result** — World model 351 writes vs Cross-level notes 0; stale sections re-injected as current; slim modes beat full. [M2 A/B] → our config already off; respect it.
22. **Tolerant section-header parsing** — parenthetical stripping took capture 89%→98%. [M2 #23] → reference only (sections off for us).
23. **Degenerate-output defense** — zlib ratio < 0.01 over ≥500 chars = repetition loop; stub it. [M2 #27] → future (LLM-arm hygiene).
24. **Malformed tool calls dropped from history AND request** — "one malformed call committed to history makes EVERY later request fail at render time". [M2 #27] → in bundle.
25. **Token-calibrated context trimming** — chars/token calibrated from server usage (measured 2.75-3.69, mean 3.12); clamp [1.0, 3.3]. [M2 #18] → in bundle.
26. **Drain hysteresis** — trim triggers at budget, drains 58k below; "evictions become rare and large"; coalesce turn-cap trims with token trims. [M2 #19] → in config.
27. **Rolling summaries on token schedule** — "one game in fourteen complied when asked per turn"; scheduled interval is the fix; summary = "the interpretation, which is precisely what eviction destroys". [M2 #20] → future lever (needs summary path; sections off for us).
28. **Trim old reasoning blocks** — reasoning was 43.7% of sent chars; Qwen3 needn't re-send old thinking; deeper history measured better (-4.20, p=0.032). [shiiin9 #15] → candidate future lever.
29. **Disable thinking entirely** — 38% engine-time reduction; quality tradeoff unproven for us. [shiiin9 #16] → contrarian knob, park.
30. **Token-denominated per-game budget** — wall-clock limits differ per backend; tokens are comparable. [shiiin9 #28, M2] → in bundle.
31. **Yield/resume in tokens (2048) + resume tones** — preserved work + continuation prompt; batch sizes 6.73/6.91 vs 5.43/3.91 after resume. [M2 #30] → in config.
32. **Flat image-token accounting + history image stripping (keep last 2)** — "median 8 obsolete boards per request, ~26% of budget"; estimator over-charged images 5-8×. [TAAF F1] → in bundle (vision path).
33. **Middle-out tool-output truncation** — head 2/3 + tail 1/3 ("tail holds the result, head the setup"). [M2 #31] → in config.
34. **Board-dump suppression** — collapse ≥6 board-like lines; "compute over the grid in python". [M2/TAAF] → available, off in shipped config.
35. **Prompt economics law** — "+1,735 chars of system prompt → +688 chars/turn generation, turn count -13%, levels 39→30". [shiiin9 EXP-099] → META RULE for all our prompt edits.
36. **Prompt rewording danger** — one rewording run "lost 43% of the previous competition score". [M2] → META RULE: additive prompt text only, A/B separately.

## 3. Perception / frame processing

37. **Rotation-canonical object hashing** — canonical orientation from COLOR-FREE hash ("the argmin depend[ed] on the colour... models were reading noise"); exposes hash/rotation/symmetry/pose_hash/shape_hash. [M2 #14] → in bundle.
38. **Object-level frame diff via Hungarian assignment** — moved/rotated/appeared/disappeared/changed_color/resized with max_group_match=40 (O(n³) guard). [M2 #15] → in bundle; D-prime scoring consumer.
39. **Animation/transient-cell capture** — cells changing ≥2× are "exactly the pixels no frame the agent can reach will ever contain"; prepend pre-action board to the chain ([Y,Y,X] vs [X,Y,Y,X]). [M2 #16] → in bundle (ANIMATION=1).
40. **Animation frames INTO the sandbox** — `last_transition.frames`/`frame_count`; "F13 is the only change that has ever moved the hidden leaderboard (3.20 → 3.71)". [TAAF F13] → in bundle via lazy `last_animation_frames`.
41. **Frames YES, narration NO** — harness-authored per-frame TEXT summary did NOT transfer (2.57 vs 3.71). [TAAF F13b] → anti-lesson: don't narrate frames to the model.
42. **Contact-sheet image** — one labelled multi-panel image, all-or-none subsampling, one legend line, area-based token charge. [TAAF F19] → vision-arm option.
43. **HUD-band learning (F5)** — learn bars/counters from diffs alone (edge line, ≤3 cells, monotone, ≥3 ticks); emit `board_changed_ex_hud`. [TAAF] → future upgrade over static border=4.
44. **Off-palette diff imagery** — unchanged cells dimmed to (16,24,48) dark navy; "no gray is safe" on the ARC palette. [M2 #17] → in bundle.
45. **Direction classifier min_frac=0.8** — at 0.6, 142 wrong directions on patterned sprites vs 11 at 0.8. [TAAF F7] → in bundle's ledger path.
46. **21-channel featurization** (16 one-hot + bg + rarity + edge + row + col) — the ChangeNet input; reusable for any learned scorer. [Ash FORGE v20] → future.
47. **Mover/target colour discrimination** — centroid drift >5px = movers; drift 0 = targets. [hybrid #25] → cheap prior for our memory dicts.

## 4. Exploration architecture (LLM-free convergence zone)

48. **Frame-hash transition graph + frontier planning + edge invalidation** — nodes = distinct frames, edges = observed transitions; plan BFS path to nearest untried frontier; planned-path mismatch deletes the edge. [hybrid #27 "from FORGE v20 / Ash's agent"; poby v47; pscamillo starter] → the LLM-free consensus architecture; our LLM harness gets it via sandbox python, but the same structure could live harness-side. **Best next-week candidate (Y25+).**
49. **Click candidates from connected components** — blob centroids ordered by button-likeness `fill/(1+size)`; FLAT pool beat 5 hard tiers ("tn36 dropped 112→30 states... tiers never reach non-button cells"). [poby v47] → evidence-backed anti-pattern warning for tiered ordering.
50. **Coarse grid backstop for clicks** — every len//6-th pixel + 8×8 grid sweep. [hybrid] → in our harness's click logic.
51. **Six-phase solver ladder** — A* → rescan-BFS → hidden-fields retry → IDDFS → permutation → beam; each phase consumes a shrinking time slice. [hybrid #22] → pattern only (hidden games are API-only; source BFS dies there).
52. **CRITICAL FACT: hidden-set games are API-only** — "Game source is not reachable, so the whole offline-BFS / CLTI / transfer stack has been deleted" (FORGE v20 rewrite rationale). [Ash] → kills source-BFS dreams on the real leaderboard; forward-model must be LEARNED from frames.
53. **State hashing with transient-field exclusion** — exclude fields that change every action; track suspect hidden counters separately. [hybrid #23] → ports to our state-hash hygiene.
54. **Warm-up unlock** — if a state scans 0 effective actions, try one unlocking click before judging dead. [hybrid #29] → ports to any agent.
55. **Cross-level prefix replay transfer** — replay previous level's solution (direct / centroid-offset / ×N repetition) on new level. [hybrid #26] → cheap win for our memory dicts (per-game).
56. **Novelty-weighted training targets** — novel change = 1.0, any change = 0.6, no change = 0.0. [Ash FORGE v20] → for any learned change-predictor we add.
57. **Global wall-clock budget shared across games + safety margin** — vs per-agent 8h. [Ash] → in our scheduler already.
58. **Hierarchical ACTION6 selection** — choose action type first, then coordinate; "/4096 division drowned clicks". [Ash v19-fix] → in our click logic.
59. **Reset-to-regain-reachability** — when graph exhausted, MAX_CONSEC_RESETS=3 escape. [pscamillo] → ports to memory-dict agents.
60. **ε=0.05 random untried + softmax sampling when exhausted** — stochastic escape from full coverage. [hybrid] → variance-band tool, use sparingly (determinism!).

## 5. Cross-game slot scheduling (the D' battleground — our champion's home turf)

61. **D' formula** = A·M·C + B·φ (A depth×efficiency^2.5, M pace, C patience with pace-relative token scale, B room-to-grow 16/14/10, φ tail fade 0.4) — the +1.5-over-v1 simulation pick; **already our champion cell 23**. [shiiin9; claimed 31.54 single sub]
62. **Fresh-first removal** — unstarted games priced by the same formula instead of jumping the queue. [shiiin9] → already ours.
63. **Prefix-band slot economics** — 2M never-trimmed / 1M warm / 0-1325 prefill bands; yield the slot exactly when the trimmer invalidates the prefix ("the one moment yielding is free"). [M2 #11] → in our scheduler.
64. **Refresh-queue on release** — re-score every waiter each release against the shared clock. [M2] → ours (`ARC3_PRIORITY_REFRESH_QUEUE=1`).
65. **(A+B)·C priority value** — level·efficiency + tail (8/7/5/0 remaining table) × hazard blend (two measured decay curves, action_scale=115, token_scale=62000); "flat tail was the WORST option tested". [M2 #10] → harness default we replaced with D'; keep as control.
66. **Kaplan-Meier pace reference** — per-level expected token cost from 1,417 historical episodes; ProgressPace EMA with shrinkage n/(n+3), clamp ×0.5-2. [M2 #18, shiiin9 #8] → ours ships mean-tokens-per-level (FormPace); the KM table is a drop-in upgrade candidate.
67. **Endgame phase switch worth 8-12% at constrained budgets** — final-phase priority = level·(0.25+efficiency). [M2 #12] → our fade 0.4 covers part; explicit endgame mode is a knob away.
68. **Tail fade** — B→0 over final 20-40% of run; ours ships 0.4 via D'. [M2/shiiin9] → active.
69. **Score normalization 55/(N(N+1)/2), N clamped 6-10** — [M2] → ours.
70. **Lottery scheduler** — proportional-lottery draw beats deterministic sort when per-game estimation is noise-soaked ("same notebook, same game: 0.00 and 28.57, SD≈6.2"); never starves (base ticket > 0). [shiiin9 duck-plus-ours EXP-100] → interesting alternative; D' priority already noise-managed via pace clamp.
71. **Stall knee at 80 actions** — P(still clearing after S actions): 61%/52%/46%/27%/14%/6% at 0/20/30/50/80/200; factor 1/(1+(S-80)/40), floor 0.1; FLAT knee beat per-level knee (4.00 vs 5.68, 2.8σ — "loosening the knee is wrong"). [shiiin9 EXP-106] → **strongest measured scheduling constant in the sweep**; candidate to fold into D' (D' has patience C but no stall-knee term).
72. **Triangular level-value correction** — level_value = ℓ/(N(N+1)/2); level² tickets misprice 3.7× across games with different N. [shiiin9 #4] → ours (norm(N) in A).
73. **Simulated annealing of ticket sharpness** — p 0.4→1.9 over run; early rankings are noise. [shiiin9 #5] → variant idea.
74. **Fresh-game pricing** — never-started games get PrioritySnapshot(1,0,0,0,N) not ∞. [shiiin9/heliosli] → ours.
75. **Drop-in scheduler contract pattern** — `install()` validates hasattr anchors and raises on drift so Save&Run catches breakage. [shiiin9/heliosli] → **our pack follows this pattern**.

## 6. Serving / models (GPU-arm intel)

76. **Qwen3.8-Flash-Next W4A16 AutoRound + INT4 MTP drafter (NEXTN, 3 steps, FR-Spec hot-token map)** — the entire M2-family serving stack; SGLang Pennyroyal v2.5.3 on RTX Pro 6000. [M2] → ours (byte-identical metadata).
77. **NVFP4 variant + 2×16k-context slot doubling** — "KV 5GiB, ctx 16384: 2× slots for 28 concurrent games in the SAME budget; unlike raising KV, uses no GPU memory". [keithtyser/TAAF] → context-window↓ tradeoff lever.
78. **MTP on/off as measured A/B arm** — ARM A mtp3 vs B mtp0 with /proc cmdline verification gate. [duck-anim] → discipline pattern.
79. **Sampling: temp 0.7 / top_p 0.95 / top_k 20** — the whole top tree ships this. [ALL] → our Y19 lever (temp 1.0) is deliberately contrarian; kernel built+verified, un-fired.
80. **Watchdog: 4 consecutive /health failures → restart, ≤2 restarts, confirm port free** — [TAAF] → hygiene for our serve cell.
81. **Gemma-4-31B vision path** — Forge v46 profile (LLM_MAX_PLAN_ACTIONS=4, reflection every 10, 4 images/prompt). [mbmmurad 0.86] → evidence that smaller non-Qwen models underperform the Flash-Next stack at equal harness.
82. **Reasoning-history key per backend** — `reasoning_content` vs `reasoning`: "69 prompt tokens vs 3670 for the same text". [M2 #28] → ours set correctly.

## 7. Sandbox / world-model (M2-top's flagship — next-week scale)

83. **DF-WM: model-written `simulate()` + `check_sim()`** — replay the model's simulator against recorded transitions, report accuracy + mismatches; "act_checked()" executes one action at a time and CANCELS the batch on divergence ("Remaining N action(s) cancelled to save budget"). [M2-top v29] → **top candidate for Y25/Y26** (372 lines, stdlib-only).
84. **Observed-edges overlay** — measured transitions outrank model predictions unconditionally. [M2-top] → principle for any planner we add.
85. **Routing cost model** — min(MemoryRoute BFS, UndoChain, ResetAndRoute 1+d); "tie breaker strictly prefers non-RESET routes". [M2-top] → with UNDO exposed (ours is).
86. **3-valued claim graph (PLUS/MINUS/UNDECIDED)** — laws need 2 direct confirmations (1 for lethal/collectible), 2 counterexamples to refute; Teacher-Forced replay judging. [M2-top UND] → concept portable; system is 11k lines (too big to port wholesale).
87. **HUD-timer detection + probe budgets** — max probes = 25% of estimated remaining steps; hard stop at ≤4. [M2-top] → ports to our death/budget handling.
88. **Knowledge card + digest with cache-stable canonical formatting** — sorted actions/colors to preserve prefix cache; zero goal leakage. [M2-top] → prompt-construction discipline.
89. **Persistent retained functions** — AST+dis validated, source-based, game scope, dependency closure; "the model stops re-writing BFS helpers every snippet". [M2 #21] → in bundle (PERSISTENT_FUNCTIONS=1, scope=game).
90. **UNDO exposure** — ACTION7=UNDO in 3-5 of 6 public games exposing it; honest "costs an action" framing. [TAAF F6/duck] → ours (EXPOSE_UNDO=on).

## 8. Submission engineering (zero-slot-cost armor)

91. **Parquet pre-materialization + finally-rewrite** — "Guarantees Kaggle runner always sees valid non-zero byte parquet". [M2-top] → our placeholder path exists via guard; finally-net is a hardening candidate.
92. **Gateway probe as commit/rerun discriminator** — the env rerun flag is DEAD platform-side since Oct-21/22 (F-1022 chain); gateway presence = rerun. [our F-1025] → ours already.
93. **Fail-open hardware probe** — ≥40GiB GPU + inconclusive probe inside rerun → run. [our F-1024] → ours already.
94. **Soft deadline = budget − min(600, budget/2)** — graceful exit preserves partial score. [romantamrazov V31] → in bundle.
95. **Daemon system census every 10 min** — "keeps reporting through a deadlock". [M2] → ours (cell 21).
96. **KAGGLE_IS_COMPETITION_RERUN gating diagnostics + private log redaction** — don't leak game ids; aggregate-only publishing. [TAAF] → hygiene note.
97. **Dummy parquet for offline runs** — Save&Run needs valid output to commit. [simplified starter] → ours.
98. **base85+gzip embedding of 11k-line patches** — 110,534 bytes fits the notebook. [M2-top] → technique for future big patches.
99. **Threaded precache (32MB chunks, 16 threads) of wheels+weights** — [M2] → ours (cell 9).
100. **Offline uv/SGLang venv + install_marker idempotence** — [M2] → ours.
101. **ONLY_RESET_LEVELS=true pinned before client build** — RESET keeps the level. [ALL] → ours.
102. **max_actions_per_game=None (never give up)** + WIN-or-timeout done condition + catch-all→RESET with reasoning tag. [hybrid #30] → ours.

## 9. Meta-discipline (the sweep's process lessons)

103. **Every knob read at call time, never at import** — "the read-at-import style is a pit we fell into 4 times". [shiiin9] → our pack sets env at install time (before module import) AND at cell runtime.
104. **Verify-then-run** — patch cells probe anchor strings + compile() + probe a function before trusting. [shiiin9] → our hasattr contracts.
105. **Observation never kills the run** — reporters are daemon threads; "never take production down for observation". [shiiin9 EXP-102] → our census cell already daemonized.
106. **AST-fingerprint-guarded observers** — refuse to run if patched method shapes drift; "do not silently promote this run". [duck-anim] → future for our own A/B instrumentation.
107. **Resolved-knob banner** — dump every effective sampler/env knob at start. [duck-anim] → our pack prints status line; extend next build.
108. **One-line-per-run arm switch** — "this is the ONLY line you change between runs". [duck-anim] → our config-flip discipline.
109. **Rehearsal clones** — 25/110 clone games with placeholder parquet; TRUE_SUBMISSION flips the audit off. [shiiin9] → our ft09 smoke is the poor-man's version; full rehearsal needs the GPU budget we don't have locally.
110. **Score variance reality** — same code: 27.62 → 31.47 (dfranzen's own page); "one submission of D' is not enough to say by how much it is better". [shiiin9 cell 0] → our ±1.9 noise-floor doctrine, independently confirmed by the 31.54-author.
111. **Per-games SD ≈ 6.2, 70% of mean 8.6** — per-game scores are noise-soaked; only cross-run aggregates mean anything. [shiiin9 EXP-099] → variance law confirmed at game granularity.
112. **Negative results are load-bearing** — memory sections OFF, noop-guard OFF, flat tail WORST, tiers REGRESSED, narration didn't transfer, prompt rewording -43%, per-level knee WRONG. The top players A/B everything and publish the graves. Respect the graves.

## 10. Top-50 personality scan (leaderboard CSV, 4,799 rows)

- Only **6 public notebooks** from top-50 members (shiiin9 ×2 mined; wkdrbwnd1 ×4 = eval/featdump internals).
- Top-50 payloads: Yi-Chia 71.48 (+2.6/wk, 41 subs), Tufa Labs 68.91 (171 subs = prod-scale A/B),
  Turducken 56.02 (209 subs!), last dance 50.69 (91), mtg 50.37 (78). The top-10 dominate via
  **submission volume + private iteration**, not public code. Nothing public explains 50+.
- `the last dance` + `Grigoriy Zatravkin` + `復活の混テキスト` — no public code at all.
- **Implication**: our public-intel edge is at the M2-fork layer (30-36 band); the 40+ tier runs
  private harnesses. To climb past ~36 we need own-build levers (DF-WM class, #83) not more forks.

## 11. Immediate actionability ranking for OUR stack

**Oct-26 fire (built, tested, ready)**: #2+#3 (death ledger + lookahead), #19 (W1 dedup), #10 (W2 snippet refusal), #20 (WM wipe off) — all fail-open, worst case = vanilla champion.
**Ready-built alternative**: #79 (Y19 temp 1.0 — 9/9 gates, kernel complete, un-fired).
**Next-week candidates (ranked)**: #71 stall-knee folded into D' (measured 2.8σ); #83 DF-WM act_checked (flagship); #48 harness-side transition graph; #28 reasoning trim; #66 KM pace table; #67 explicit endgame mode; #43 HUD-band learning.
**Respect the graves**: #4 noop-guard stays OFF; #36 no prompt rewording; #52 no source-BFS on hidden set.
