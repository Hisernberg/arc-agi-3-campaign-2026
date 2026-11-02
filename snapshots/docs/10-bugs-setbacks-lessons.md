# 10 — Bugs, Setbacks & Lessons Learned (ours + competition-documented)

**Date:** 2026-10-08 · Companion to `09-techniques-catalog.md`. Everything here is either (a) documented by a competition source with numbers, or (b) happened to us with dates and costs. Read before touching the kernel.

---

## 1. Competition-documented bugs & setbacks (with sources)

### Serving / infra
| Bug | Effect | Source / fix |
|---|---|---|
| **vLLM KV-cap applied blind**: cap read against "Initial free memory" BEFORE 81.8 GiB of weights load; profiling skipped when cap is manual. 6.5 GiB KV OOM'd 6 min into serving (94.70/94.97 GiB = 278 MB free, died on a 308 MiB conv activation) | run dead, 30 of 45 min without server | duck-18 (Lohit) M-ledger; fix: measure, leave 2.5× headroom |
| **Watchdog restart path regression**: restart passes `enable_chunked_prefill=False`; an overridden `MAX_NUM_BATCHED_TOKENS` below context (32768) fails validation → BOTH restart attempts failed | 30 of 45 min with no model server | duck-18: leave the env var UNSET so restart falls through to 32768 |
| **One huge weight shard breaks prefetch/loader alignment**; startup unreliable | boot flakiness | dfranzen: reshard into smaller shards |
| **W4A16 boot JIT-compiles Triton/TileLang kernels into empty /tmp each session** (142.6 s vs 6.0 s on NVFP4) | minutes lost per cold start | hknight/Lohit M87: tar caches to working dir, re-attach as dataset |
| Borrowed CUDA toolkit had no lib64/, dangling libcudart symlink | JIT linking fails | duck-18 `_repair_cuda_libs()` |
| Kaggle kills runs with no actions in a window | dead run during slow boot | Sovereign: `ARC3_WARMUP_ACTION_GAMES=1` (counted auto-RESETs) + 900 s first-retry |

### Harness logic
| Bug | Effect | Source / fix |
|---|---|---|
| **ACTION7 advertised but rejected**: duck raw fork's `ENGINE_TO_MODEL_ACTION` omits ACTION7 → `to_engine_action("ACTION7")` = None → solver.py:627 rejects before the engine. **0 executions in 3,566 actions** while advertised in 6 games on every turn; 4 of those games are perpetual-zero (g50t, sk48, sp80, tn36) | model told an action is legal and cannot use it | Lohit v14.14 patch; dfranzen's UNDO→ACTION7 wiring avoids it. **Lesson: grep rerun logs for `UNDO executed > 0`** |
| **Flat 999999 priority** made every game tie at startup → arrival order only | scheduler silently degenerate | dfranzen: subtract queue position |
| **Shared guard-override slot**: death guard consumed the single armed slot → a mouse-only game observed **291 model replies and 1 executed action** | effective deadlock | dfranzen: per-guard-kind slots |
| **18,012-char reasoning turn hit the output cap and executed nothing** | whole turn wasted | dfranzen: `ARC3_PREFER_TOOL_CALLS` hint; reasoning-effort ladder |
| 46 Ki window: the 30-assistant-message cap was the binding limit, so token drain alone changed nothing | trim not effective | dfranzen: `ARC3_HISTORY_TURN_DRAIN` |
| Trimming overshoot: nominal 28k–40k band actually realized 14k–38k with ~6k blocks | budget mismatch | dfranzen: calibrated estimates (rejected a floor — it raises trim frequency ~½ again and cuts cache hits) |
| Turn yield in seconds bought 2,140 vs 3,829 tokens on two backends | every serving change silently retuned the yield | dfranzen: yield-by-tokens (2,048) |
| Backend never showed >13 concurrent requests with 14 games | capacity silently idle | dfranzen: diagnostic census → admission=slots |

### Agent behavior (failure-mode taxonomy)
| Mode | Evidence |
|---|---|
| **Hypothesis lock-in / tunnel vision** | dominant failure in RGB paper + ARC's GPT-5.5/Opus-4.7 analysis ("Solved The Level, Didn't Learn The Game" — L1 luck hardens a wrong theory) |
| **Wrong level of abstraction** (game mapped to Tetris/Frogger/etc., analogy hijacks action selection) | ARC official 160-replay analysis |
| **Guard deadlocks** | Kepler: two guards with complementary conditions deadlocked the agent (fix d37660e) |
| **Aggressive reset discipline collapse** | sp80 fell 82.16 → 14.29 coinciding with added reset discipline |
| **Search under a mistaken model** | sp80: ~4.1×10⁸ candidate configs explored while 15/4,670 transitions unexplained — "responding to counterexamples" beats "expanding search" |
| **Naive whole-board change as progress** | shrinking budget bar changes pixels every step → use 4-cell interior crop |
| **Mistaking HUD/edge bars for gameplay** | Duck prompt explicitly warns against clicking segmented edge bars |
| **Single action per turn, over and over** | GPT-5.6 terra/luna; fixed by prompt reorganization, not model revert |
| **Confirmed-knowledge lock-in in memory files** | Retrodict: 4+ games fell after reframing "confirmed" → "working model" |

---

## 2. Our campaign's bugs & setbacks (dated, with costs)

| Date | Setback | Cost / lesson |
|---|---|---|
| Sep 18 | First real submission scored 3.45 (Duck base) | baseline established; everything above it is harness+config |
| Sep 19 | Governor v1 = 2.77 (below base) | our first no-op-loop breaker *hurt*; fail-open design kept for later, discipline prompt kept neutral |
| Sep 20+ | env resets wiped `~/.local` + `/tmp` twice, killing kaggle package + armed background scripts | **created persistent venv `/home/z/my-project/.venv-kaggle`**; every watcher must be re-checkable from files, not memory |
| Oct 6 | F+D custom stack (fable layer + Osaka D′ on super base) scored **20.77** vs super-family μ≈26.8 | mixing layers without paired evidence = regression; parked the line. Lesson: **one changed layer at a time, or you can't attribute** |
| Oct 6 | kaggle.json auth silently rejected; KGAT works only via `KAGGLE_API_TOKEN` env | auth quirk documented in scripts |
| Oct 7 | output download first check misread "no parquet" (partial download); SDK response field was `resp.content` not `result` | verify with list_kernel_session_output before concluding |
| Oct 7 | **Armed submit watcher died in an env reset** before firing; today's slot would have been missed | re-armed PID 1853 Oct-7 17:11 UTC with log file `reports/oct8_submit_watch.log`; lesson: **every armed automation needs a self-evident log + a manual fallback script** |
| Oct 7 | super-v2 commit run was a 12-min 5-game smoke, yet scored 27.38 → decoded that **Kaggle rescores the committed code (full 25 games), commit output only gates** | the free-redraw engine exists because of this; also means commit runs only need the placeholder gate |

---

## 3. Distilled lessons (rules we operate by)

1. **The rerun is the product; the commit is just a gate.** Never spend GPU on scored-run-length commits; 33-second placeholder + `RUN_FULL` gate.
2. **One layer at a time, paired by game, P≥0.90** — otherwise you're drawing lottery tickets and attributing noise (dfranzen's significance harness exists for a reason).
3. **Variance is a resource, not a nuisance.** Same-config redraws are free score draws; the LB keeps the max.
4. **Every guard must be overridable and per-kind.** Hard blocks foreclose hidden-state mechanics; shared slots deadlock.
5. **Prompt changes before machinery.** The Gold solution disabled most of its own machinery; the wins were prompt+perception+allocation.
6. **Keep thinking, keep evidence, trim rarely and hugely.** Cache reuse IS score on a fixed GPU budget.
7. **Advertise nothing the harness can't execute.** Grep for "executed > 0" (ACTION7 lesson).
8. **Interior-crop everything** (guards, dead-signatures, diffs) — the HUD lies.
9. **Local runs must match competition arithmetic** (parity math) or their scores mislead.
10. **Automation must survive environment resets:** persistent venv, scripts on disk, logs on disk, and a manual one-command fallback for every armed process.

---

## 4. Pre-mortem for the Oct-8/9 window (what could go wrong)

| Risk | Probability | Mitigation |
|---|---|---|
| Watcher dies again before 00:05 UTC | low (log monitored) | manual: `.venv-kaggle/bin/python scripts/submit_m2top_a.py` after 00:00 UTC |
| Kernel `arc26-m2top-v1` rerun fails (OOM / boot) | low (same stack as sujan's 31.93 draw; warmup action + 900s retry present) | check rerun status Oct-8 evening; a failed rerun does NOT consume the slot's score but DOES consume the day → resubmit next day |
| Draw lands 29–31 (μ band) | ~40% | redraw Oct-9 (same version); P(two draws ≥31) ≈ 0.8 |
| GPU quota still walled Oct-10 (resets 00:00 UTC) | — | v2 improvements are committed ONLY after quota returns; until then all improvement work is offline (code + tests + paired local CPU checks) |
| A v2 config change regresses μ | medium if we touch many layers | v2 shortlist is capped at 3 changes (catalog §6 items 2–5), each independently toggleable by env flag |

## 5. Added 2026-10-08 (research day)

| Date | Setback | Cost / lesson |
|---|---|---|
| Oct 8 | B's draw of the sujan "m2top" copy scored **23.65**; cell-level teardown shows that notebook has no D′ and only a buggy prompt hook — the Oct-8 plan's "μ ≈ 31 D′ family" counted non-D′ draws | one slot inside the plain-M2S distribution; lesson: **verify a family membership from the notebook's cells (hash vs base), never from a title or description**; `kw_sweep_kernels.py` now does the hash diff automatically |
| Oct 5–8 | B's `arc26-m2s-d-prime-pure` commit ERRORED: `AssertionError: model dir not found: /kaggle/input/models/dfranzen/intel-qwen3.8-flash-next-w4a16-autoround/transformers/default/1` (mount-path layout differs between sessions) | B has no D′ version to redraw until re-committed; lesson: **every kernel resolves input paths with fallbacks (sujan cell 4 pattern) and fails fast with the path list printed** |
| Oct 8 | Forum: dataset/model mount failures (`ERRORED_MOUNTING_DATASET`, CPMP) and 6–17 h commit queues | commit placeholders the night before; a version that is not COMPLETE is never submitted (`kw_submit.py` guard) |
| Oct 8 | Catalog rows for a notebook were taken from its description, not its code; three rows were wrong | **teardowns are cell-hash diffs + code quotes**, stored under `analysis/teardowns/<date>/`; the catalog gets a dated corrections section, never silent edits |
| Oct 8 | Account A's state could not be verified from this session (no A token in the environment) | tokens as environment secrets (`KAGGLE_API_TOKEN_A/_B`), never pasted into chat; rotate the three tokens that were pasted today |
| Oct 8 | A's Oct-8 draw (ref 56947228, `arc26-m2top-v1` v1, D′ build) ended in a Kaggle system error on the rerun; commit was clean | one A slot lost; lesson: a rerun ERROR is retried exactly once (Kaggle's own instruction), and a second ERROR marks the *version* suspect; `kw_status.py` now surfaces `error_description` |
