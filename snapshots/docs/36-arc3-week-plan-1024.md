# 36 — ARC-3 ENDGAME WEEK PLAN (Oct-24 → Nov-02): teardown integrated, quota rebuilt, F-1024 fixed

*Task 36, 2026-10-23 (evening UTC). User supplied the external "Competitor Teardown,
Architectures & 100+ Ideas" report (v1 + v2, snapshot Oct-23 16:05/16:35 UTC) and directed:
"use ideas of arc-3 and plan for this week properly with new ideas such and similar."
This doc: (1) reports the F-1024 root-cause kill (proven from rerun logs this session),
(2) reconciles the teardown against our ground truth, (3) lays the day-by-day endgame
plan under the REBUILT quota model, (4) registers the new idea wave Y1–Y30.*

---

## 1. Situation report — the breaker is dead, long live the base

**F-1024 SOLVED (root cause proven, not hypothesized).** The Oct-22 memsolve 0.00 and the
Oct-23 byte-identical control 0.00 (ref 57553794) shared one signature: both scoring reruns
printed `[guard] rerun=False -> RUN_FULL=False`, wrote the placeholder parquet (3411 B) and
exited in ~23 s. The guard — inherited from the `lwq255/arc3-dprime-guarded` fork — gated
the full run on `KAGGLE_IS_COMPETITION_RERUN=1`. **Kaggle stopped setting that env var in
scoring reruns between Oct-21 05:03 UTC (leviathan 22.33/22.47 real) and Oct-22 08:42 UTC
(memsolve 0.00).** Platform-side, silent, and it zeroed every submission we made for two
days. Evidence chain: `reports/rerun_log_control_1023.txt`, `reports/rerun_log_memsolve_1022.txt`
(the rerun logs ARE retrievable via `kernels/output` — that false belief cost us two days).

Consequences, ranked:

1. **memsolve is EXONERATED.** The control carried no solved-memory module and failed
   identically. The 0.00 was the guard, not the module. memsolve returns to the lever queue
   (still behind re-anchor; still n=1 provenance halo risk on its +1.4 claim).
2. **F-1024 guard-fix built, verified, and FIRED.** `arc26-b-dprime-fix-v1` pushed 18:2x UTC
   Oct-23; commit runs overnight with the fail-open guard (`RUN_FULL=True` on any ≥40 GiB
   GPU); watcher `scripts/watch_fire_oct24.py` (PID armed) submits at the Oct-24 window after
   verifying `RUN_FULL=True` in the commit log (loud-fail if the platform changed again).
   `arc26-a-dprime-fix-v1` is built + verified + **quota-locked** (below).
3. **[diag:F-1024] canary embedded in every future build.** One log line per run: env key
   NAMES (never values), python version, `/kaggle/input` + competition-bundle listings.
   Readable for scored runs at zero slot cost. We will never be blind to rerun plumbing again.
4. **Quota model REBUILT — this changes the endgame math.** A's push failed with
   **"Maximum weekly GPU quota of 30.00 hours reached"** — the hard cap, per account, weekly.
   The guard-fix cycle costs commit (6–9 h, full public-set play) + rerun (6–9 h, hidden set)
   ≈ 12–18 h. Therefore **~2–3 verdict-bearing cycles per account per week → ~10–14 team
   cycles to Nov-02, not the ~20 slots we budgeted on Oct-22.** Every remaining slot must
   carry a verdict. A's reset: probe daily with a smoke push (~23 s GPU on success, free
   error while capped) — the push error IS the quota gauge.
5. Slot ledger discipline: two consecutive 0.00s cost us 2 of ~12 remaining cycles. The
   pre-committed control-isolator decision (D-2026-10-22-04) is exactly what bought the
   diagnosis — it converted a second wasted slot into the proof.

## 2. Teardown reconciliation — adopt / already-have / reject

The teardown's ARC-3 core claims, checked against our stack (we fork dfranzen's M2 solution
+ Duck harness + Pennyroyal SGLang + Flash-Next W4A16 + MTP×3 + FP8 E4M3 KV + 10 streams @
~136 Ki ctx — i.e. **we already run the "public best" stack** the teardown says to reproduce):

| Teardown claim | Verdict for us | Action |
|---|---|---|
| "Reproduce Franzen's stack (B1–B41 P0s), gate board ≥ 35" | **ALREADY OUR BASE** — our fork IS his public code; our 33.50 (Oct-09) sits at the gold line (38.20 = rank 19) and ABOVE his M2 27.89 | No action; our lever search continues from here |
| "5 submissions/day" | **FALSE** (our metadata: maxDailySubmissions=1; docs/35 §1) and now MOOT — quota caps us at ~2–3 cycles/week/account anyway | Slots are quota-bound, not limit-bound |
| "A/B two accounts risk DQ; merge by Oct-26" | Already merged: team `arc-needs-to-be-agi`, both accounts (fact-checked #214d); the one-person-two-accounts rule question stays a user-level compliance call, not an ops blocker | Note in risk table; user decision |
| "KV cache is THE binding constraint (+8.0); size the pool first" | **NOT BINDING FOR OUR STACK** (docs/35 §1: incumbent = GatedDeltaNet×36 constant state + QSA×12 @ 2 KV heads → ~350 MB @ 57 k FP8) | B13/B11 KV-sizing PARKED unless our own pool telemetry says >90% (Y2 instrument added) |
| "Vision helps; ARC-2 vision NO-GO doesn't transfer" | Weakened for us (AVO 95–100% on 64×64 text grids; our incumbent is a VLM fed text) | Vision input stays a separate later lever (Y12), never part of a model swap |
| "Memory on state, not advice text; every advice line −2 to −3.4 (rellik13); Franzen's notes/summaries/death-ledgers neutral-to-harmful" | **ADOPTED AS DOCTRINE** — this DEMOTES our own queue: W23 R3 death-ledger re-port → PARK; W19 K-rules → CONDITIONAL (only solved-level-pinned rules, rellik13's +2.8 form; never generic advice) | ev_tracker updated |
| "Top-10 differ by: verify-instead-of-score, state-not-advice, marginal-score scheduling, paired-evidence promotion" | Matches our W-series doctrine (W5 paired reads, pre-committed zones); the two gaps are **B53 explorer-state** and **B46 expect=** — both promoted to top new levers | Y-series + calendar below |
| "Model swaps are the biggest single step; keep one challenger in the B lane" | Already scheduled (docs/35): Sage-A1.5 = CH1 (vllm 0.19 native), Gemma-4-26B-A4B = CH2; Glimmer/Bolt parked | Calendar §3; verdict rule = same-day paired read > incumbent + 1.9 |
| "Scoring = min(115, (human_actions/agent_actions)²×100) per level — wasted actions punished quadratically" | Confirmed direction (#203/204 throughput doctrine); this formula is why UNDO-guards, no-op suppression, explorer state and expect= checks are action-efficiency levers | Y-series efficiency block |
| "Python 3.13 image / cp312 wheelhouse break (B16)" | Did NOT hit us (pinned docker digest, rerun shows python3.12) — but our guard bug was the same *class*: silent platform coupling | Y1/Y2 resilience instruments institutionalize this class |
| "110 hidden games (55+55)" | Confirms our byte-forensics estimate (3767 B ≈ 110 games, W13) | Instrument stands |
| "Reruns vary hugely (5.02/5.50/6.42); public board ≈ half the data" | Validates our noise floor ±1.9 + drift-adjusted mu + paired-read discipline | No change |

**Net strategic read:** the field's ceiling with our exact harness family is Tufa's 68.91 —
~35 points above our best draw. The gap is config/tuning + verification machinery, not a
different model. With ~10–14 cycles left, we buy information in this order: base re-anchor →
one challenger → two verification levers → frozen stack finals.

## 3. The week, day by day (all times UTC; slots are quota-gated)

**Standing rules:** one submission/account/day (platform) + one GPU cycle per read (quota);
every fire pre-registered (manifest question + kill criteria + expected read); verdict ≤1 h
after score lands (W38); ≥3 free experiments per slot (W40); no new levers after Oct-31;
finals picked Nov-01/02 as (best paired-eval stack, most robust stack) — never "second-best
public score".

| Day | B (dasshovon) | A (kragglenote) | Gate / verdict zones |
|---|---|---|---|
| **Oct-24** | **F-1024 guard-fix control** (arc26-b-dprime-fix-v1, watcher fires at window). Free: read [diag:F-1024] from commit log; rebuild bands from the read | **quota-locked.** Daily probe: smoke push (`ARC3_FORCE_SMOKE=1`, ~23 s) — success ⇒ push `arc26-a-dprime-fix-v1` for an Oct-25 paired read | Read ≥24 ⇒ **base re-anchored** → challengers open. 0.00 ⇒ read diag dump FIRST, hold all fires. <24 ⇒ drift deeper, recompute bands before any lever |
| **Oct-25** | **CH1 Sage-A1.5 swap** (guard-fixed build, single lever: model+processor+template+sampling; gates docs/35 §4) — only if Oct-24 in band | If quota returned: **fix-kernel paired control** (n=2). Else: probe again | Challenger verdict: same-day incumbent baseline read ±1.9 → promote/reject (W43). No baseline ⇒ no verdict ⇒ no challenger fire |
| **Oct-26** | **CH2 Gemma-4-26B-A4B swap** or Sage n=2 (whichever needs the read) | paired baseline / probe | **kernelsPublishingDisabled 23:59** — fork ALL candidate parser notebooks (Glimmer/vLLM-0.28 parsers, drafter examples) BEFORE this deadline (W45) |
| **Oct-27** | **L1 = B53 explorer-state** (CPU state graph: masked-frame hashes, untested-action frontier, BFS-back — exposed as `graph`/`clicks` REPL variables, zero advice text) | paired baseline n≥3 for the surviving config | Keep if: fewer actions per solved level on public games AND tokens flat (teardown gate). Kill: any −1.9 read |
| **Oct-28** | **L2 = B46 expect= light** (model writes an expected-frame hash per grid-move action; harness diffs and surfaces mismatches as variables — not prose) | paired baseline | Keep if: mismatches predict failed levels on the 25 public games (offline chamber first — Y7 gate). Kill: no predictive power or token cost > Y13 cap |
| **Oct-29** | Best-of: winner model + passed levers (single combined stack, still one delta vs base at a time already individually verified) | paired read | This is the Phase-3 stacking rehearsal (doctrine A3: stacking starts Oct-30 — pulled one day early by the quota math) |
| **Oct-30** | **Phase-3 stack** full read | paired read | mu of stack ≥ base mu + max(passed lever deltas) − 1.9, else un-stack and re-bench |
| **Oct-31** | **FREEZE.** Last experimental read if a cycle is free; else base redraw for mu n≥3 | probe / baseline | No new levers after today (hard). Both accounts hold known-good COMPLETE kernels for Nov-01/02 |
| **Nov-01** | Finals pick 1: **best paired-eval stack** | Finals pick 2: **most robust stack** (lowest seed variance / no timeouts), scored today | numScoredSubmissions=2 — the final leaderboard takes the best 2; submit BOTH finalists today |
| **Nov-02** | 23:59 CLOSE. Final reads only if a finalist failed to score | same | Papers due Nov-08 (draft was due Oct-28 per W39 — paper outline exists; write during rerun windows) |

**Quota ledger for the plan (worst case 12–18 h/cycle):** B: Oct-24 fix (≈12–18 h) → ~12 h
left this window ⇒ either Sage (Oct-25) **or** Gemma (Oct-26), not both, unless A's window
shares the load. A: returns ~Oct-24/25 (probe tells us) ⇒ carries the paired baselines and
the second challenger. If BOTH accounts run dry by Oct-29, the stack freeze falls back to
"best verified subset" — the paired-read record decides, not hope.

## 4. New ideas wave Y1–Y30 ("such and similar", ARC-3-focused)

Convention: [P0] this week, [P1] if a cycle frees up, [P2] park. Every idea names its
receipt, its cost class, and its kill rule. Items already covered by W/B-series are not
repeated; Y1–Y4 are the platform-resilience block this week *earned*.

**Resilience & instrumentation (the F-1024 class — never again)**
- **Y1 [P0, LIVE]** Fail-open capability guard + `ARC3_FORCE_SMOKE=1` smoke switch in every
  build. *Receipt: F-1024 zeroed 2 slots.* Kill: none — permanent.
- **Y2 [P0, LIVE]** `[diag:F-1024]` rerun-environment signature to log every run (env key
  names, python, input listings). *Receipt: the two blind days.* Kill: none — permanent.
- **Y3 [P1]** Content-based rerun detection: count game IDs in the competition bundle
  (public = 25; rerun = 110 hidden) → restores cheap placeholder commits + full reruns if
  the mount layout allows. *Needs the Y2 listing from the Oct-24 read.* Kill: if public and
  hidden sets are indistinguishable in mounts, park.
- **Y4 [P0]** Daily A-quota probe: smoke push; push-error text = free quota gauge. *Receipt:
  A's 30.00 h cap error.* Kill: none.
- **Y5 [P1]** Parquet byte-census auto-appender: every draw's totalBytes → DRAWS note (W13
  formalized); alert if < 2700 B (placeholder leak) — now cross-checked with the guard gate.
- **Y6 [P1]** Log-diff harness: fetch kernels/output log after every scored run, grep the
  `[guard]`/`[diag]`/`OURS_*` lines into the ledger row. *Cost: 20 lines of code, zero GPU.*

**Action-efficiency block (the quadratic formula's levers: min(115,(human/agent)²×100))**
- **Y7 [P0]** Offline expect=-predictiveness chamber: before spending a cycle on B46, replay
  our 16 recorded real-run traces (21 GIFs + JSONL already on disk) and measure whether
  model-written expect= mismatches separate solved from failed levels. *Kill: AUC < 0.6 ⇒
  B46 never ships.* Cost: CPU-only, free.
- **Y8 [P1]** Action-budget governor: estimate each level's human baseline actions (we have
  per-level baselines for all 25 public games) from metadata; if agent actions > 1.4×
  estimate, flip the model's operating mode via a variable (not advice) — e.g. expose
  `budget_state = "over"` and let the policy react. *Kill: token cost > 1% of run.*
- **Y9 [P1]** UNDO cost-model: ACTION7 (UNDO) only when the expected revert saving exceeds
  2 actions (quadratic math: one wasted action at 100-human baseline costs ~2 score points
  per level at the margin). Fold into the existing no-op guard. *Kill: rerun shows UNDO
  rate up but score flat/down.*
- **Y10 [P2]** Dead-signature suppression v2: hash (frame, action) → outcome ledger as a
  sandbox variable `dead_ends` the policy can consult; suppress repeats at harness level
  (Reki's heuristic + our W22 affordance table). *Receipt: Reki M1; keep OFF if lexicon
  lesson repeats (the model ignored unused views).*
- **Y11 [P1]** Win-path replay cache: after a game-over, replay the recorded win-path
  actions to re-solve without exploration (saves tokens; actions already spent). samrishtt's
  B54, adapted: only if the harness can reset levels cheaply.

**Verification block (verify-instead-of-score, the teardown's #1 lesson)**
- **Y12 [P2]** Vision as a separate lever (not in swaps): feed segmentation-derived object
  crops only on frames where ASCII delta is ambiguous. *Receipt: Tufa attribution; AVO
  counter-receipt. One cycle, late, only if a cycle is free after Oct-29.*
- **Y13 [P1]** Token-cost hard-gate for every new variable/metric: candidate modules must
  attach a measured tokens/level delta (W31 extended from prompts to sandbox variables).
  *Kill rule for all Y-variables: >1% tokens/level ⇒ cut.*
- **Y14 [P1]** Practice-level holdout inside a game: treat solved level k as the verifier
  for level k+1 rules (ARC-NEST's hold-one-demo-out, ported to games); use it to early-stop
  hopeless games in the scheduler. *Kill: fewer games completed.*

**Scheduling & memory (marginal-score doctrine)**
- **Y15 [P1]** Completion-falloff recalibration on OUR attempt logs (B18 with our own 700+
  attempts instead of Franzen's 725) — the P=(A+B)·C scheduler's falloff constant is a
  one-line env change. *Kill: paired read inside noise floor.*
- **Y16 [P2]** Two-tier admission: returning games (warm prefix) admitted preferentially
  after the 45% clock mark (B5+B21 composed); new games front-loaded before it.
- **Y17 [P2]** KV-pool telemetry loop (B2 instrumented): log pool occupancy + preemption
  counts per hour into the run log; Y2-adjacent. *Gate: only if >90% observed does any
  B13/B11 KV work un-park.*

**Model & serving block**
- **Y18 [P0]** Challenger builds inherit the F-1024 guard + diag canary (already policy —
  recorded here as a build-gate rule).
- **Y19 [P1]** Sampling-profile A/B on the surviving challenger (temp 0.7 vs 1.0; presence
  penalty) — one env-cell delta, rides an existing paired-baseline day. *Kill: in-floor.*
- **Y20 [P2]** Glimmer re-entry only if both challengers fail AND ≥4 days remain (W49
  stands); Bolt stays parked (GGUF packing).

**Process & compliance**
- **Y21 [P0]** MIT-0 LICENSE + third-party audit cell in every build (W44 — due before
  Oct-26 fork deadline).
- **Y22 [P0]** Fork candidate parser notebooks BEFORE Oct-26 23:59 (W45): Glimmer parsers,
  DFlash drafter examples, rellik13's 16-stream serving variant.
- **Y23 [P1]** Finals robustness scorer: pick finalist 2 by (mu − λ·sd, timeouts=0) over
  paired reads, λ=1 — the teardown's "most robust, not second-best" rule, mechanized in
  ev_tracker (`finals_recommendation()` — add next session).
- **Y24 [P1]** Paper-track data pack: F-1024 case study (guard death trap + rerun-log
  forensics + fail-open repair) joins the determinism/drift/throughput paper (W39/W50).
  *This failure is publishable process knowledge.*
- **Y25 [P2]** Forum escalation thread (only if Oct-24 reads 0.00 again): post the rerun-log
  evidence; ask whether KAGGLE_IS_COMPETITION_RERUN was retired and what replaces it.
- **Y26 [P1]** Seed-diverse local reruns of the offline chamber (S6 analog) before any
  stacked-stack read: 3 seeds × 10 games, flag any lever whose delta flips sign.
- **Y27 [P2]** Cross-account date-shift reads: deliberately fire the SAME config on A and B
  on consecutive days to measure the day-effect directly (our drift slope is inferred from
  mixed configs; a clean n=2 same-config cross-day pair prices it exactly). Costs one slot
  total; worth it only if the freeze decision comes down to drift.
- **Y28 [P2]** Scheduler UCB alternative (B22) stays parked — Franzen's scheduler is in our
  base and un-tuned; tune constants (Y15) before swapping families.
- **Y29 [P1]** Byte-gate for notebooks: builder script refuses to emit a kernel whose
  embedded harness patch md5 ≠ d8dce0d88c5c (or a documented successor) — catches accidental
  harness edits at build time, not on the scoreboard.
- **Y30 [P0]** Watcher institutionalization: every fire day gets a check-log-gate watcher
  (verify RUN_FULL=True + diag present BEFORE submitting). *Receipt: tonight's watcher would
  have caught both 0.00s pre-submission.*

## 5. Risks, kill criteria, compliance (delta vs docs/35)

- **R1 (new): quota-exhaustion mid-week.** Signal: push errors on BOTH accounts. Guard:
  finals stack kernels are pushed and COMPLETE by Oct-30 — submission of an existing
  COMPLETE version needs NO new GPU. Never plan a "push tomorrow, submit today" chain
  inside the last 48 h.
- **R2 (new): the platform changes the rerun plumbing AGAIN.** Guard: Y2 diag on every run +
  watcher log-gate + Y25 forum path. A 0.00 is never submitted blind again.
- **R3: challenger integration burns a cycle without a baseline.** Guard: no challenger fire
  without a same-day incumbent baseline read (paired by account or by the Oct-24 anchor).
- **R4: stacking regression (leviathan lesson).** Guard: Phase-3 stack only composes
  individually verified levers; un-stack rule pre-committed (§3 Oct-30).
- **Compliance:** team merge already done (arc-needs-to-be-agi); kernels publishing disabled
  after Oct-26 23:59 (fork deadline); submitter-authored code → MIT-0 (Y21); third-party
  weights license audit per challenger (Qwen/Apache-2.0 ✓, Gemma terms — verify before CH2);
  no hidden-set data leaves the notebook; everything offline (docker pin + internet=false).

## 6. Ledger cross-refs

- F-1022 → F-1024 chain: memsolve 0.00 → control isolator 0.00 → rerun-log forensics →
  guard root cause → fail-open fix → diag canary → watcher gate. Two slots bought total
  platform immunity; the case study joins the paper track (Y24).
- DRAWS: Oct-23 control 0.00 appended (STRUCT-0, ref 57553794); Oct-24 fix read appends on
  landing. ev_tracker LEVERS: F-1024 (FIRED), memsolve (EXONERATED), challengers (QUEUED),
  base (re-anchor pending). Report: `reports/ev_report_2026-10-23.md`.
- Pool: Section Y1–Y30 appended (620 → 650). Artifacts: `artifacts/daily/2026-10-24/`
  (both fix kernels + metadata), manifest, watcher, `scripts/build_guard_fix_v1.py`.
