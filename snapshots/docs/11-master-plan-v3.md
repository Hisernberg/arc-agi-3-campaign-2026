# Master Plan v3 — Sweep-Informed Rebuild (2026-09-24)

Supersedes plan in `06-improvement-roadmap.md`. Evidence base: `10-kaggle-sweep-2026-09-24.md`
(3,296 teams, 1,104 notebooks, 29 deep-analyzed) + TD-JEPA/AVO/Grid-JEPA web intel.

## 0. Goal & constraints

- Deadline **2026-11-02** (39 days). Current 3.85 (rank 214/3296).
- Target: **≥5.4 within 2 runs, ≥7.0 by mid-October** (THUI/7.10 evidence makes
  this reachable without new science), then world-model track toward 10+.
- GPU: 30 h/week quota, 9 h per ARC run → ≤3 runs/week; **quota is contested by
  non-ARC jobs** → reserve ARC windows; 25-game public local runs (CPU/GPU-short)
  for development; every submission must be fully validated before push.

## 1. What changed after the sweep (root causes of our 3.85)

1. Serving profile caps: `MAX_NUM_SEQS=8` vs 28 workers, KV 5 GiB, batched
   tokens 8192 — the documented ceiling of the whole 4.x cluster.
2. No anim branch: we cannot distinguish animated-non-progress from no-op.
3. Analyzer under-budgeted: yield 60 s (THUI uses 180), timeout 900 s
   (chiakazirim twin test: 1200 s = +0.17), no seed pin, no output policy.
4. No in-sandbox evidence/trajectory structures: the model re-derives history
   every turn instead of searching a ledger.
5. No offline-sim capability (BFS/A*) anywhere in the stack.
6. 8B NVFP4 vs 27B FP8 at the top LLM scores (7.10 / 5.23 / 5.36).

## 2. v6 — "sweep bundle" (next submission; target ≥ 5.0)

Build on v5 (worldmodel-v2, 44/44 green) — keep its runtime-effects ledger +
dead-action flags + budget priors, then add, in risk order:

| # | Change | Evidence | Risk |
|---|---|---|---|
| 1 | KV_CACHE_MEMORY_BYTES 5→16 GiB, MAX_NUM_BATCHED_TOKENS 8192→16384 (keep seqs 8, MTP 3) | amanatar kv16 profile 4.08; 96 GB card | low — serving-only, validated by watchdog |
| 2 | LOCAL_ANALYZER_YIELD_SECONDS 60→180, LOCAL_ANALYZER_SEED=20260825, analyzer_timeout 900→1200, output uncapped | THUI 5.36 + chiakazirim +0.17 | low — config only |
| 3 | Trajectory ledger in sandbox: `trajectory=[{step,level,action,board_changed,level_changed}]` + tool-description line "search trajectory for repeated no-op patterns" | tanakaai24 7.10 | med — bootstrap patch w/ anchor asserts, fail-fast |
| 4 | EvidenceDecisionKernel prelude: `frame.ascii`-keyed evidence ledger; rank = completed-replay > rewarded-replay > unknown(info-gain 1/(1+trials)) > ambiguous > changed > unchanged; `_edk_verify` replays candidate transition fn vs all observed pairs; live-action budget 8 | bang1850 (179/183 local) | med |
| 5 | Batch no-op guard: stop executing a returned action batch before repeating a direction that just left the board unchanged; per-action `board_changed` aggregation | tanakaai24 AGI_8 | low — harness-level, we already have flags |
| 6 | Offline-sim probe cell: enumerate `**/environment_files/**/*.py` + `/kaggle/input/competitions/*`; log count + sample class names to stdout (informational for 110-game question) | new intel | zero |
| 7 | Graceful-stop watchdog: on 4× server failure set `solver._stop_event` so completed levels still score | xiaoyan12 v16 | low |
| 8 | If jakobbrggen anim dataset attachable: graft `animation_awareness=True` + `hard_noop_guard=True` via THUI dual-bundle pattern | THUI 5.36 on both models | med — assert-teeth, fail-open to stock |

Validation gauntlet: all existing 44 preflight checks + new tests (3,4,5,8) vs
real bundle tool_agent (anchor/idempotency/fail-open), 8k-action trace replay
regression, offline-sim probe dry-run on local engine, serving config lint.
**Ship only at ≥50 greens.** If quota frees before v6 is green, v5 goes as-is
(queue order preserved — never burn a slot on unvalidated code).

## 3. v7 — "27B + search side-channel" (run 2; target ≥ 6.5)

1. **Model upgrade path A (preferred)**: Qwen3.8-27B-FP8 (jakobbrggen snapshot)
   or Qwen3.6-27B-FP8 (driessmit1/vrfai snapshot) via H100-wheelhouse v3 —
   **must first verify sm120 (RTX Pro 6000) compat of the wheelhouse vLLM build
   on CPU-side smoke test; fallback path B: Frozenlock/Qwen3.8-27B-int4-AutoRound
   (~18 GB) with MTP n=3** (ghazaros catalog: 2580 tok/s prefill on 5090).
2. **BFS side-channel agent** (zhengxuyu port): offline-sim BFS w/ status-bar
   masking + hidden-field probing + object click candidates + plan cap 1.5× +
   250 s/level give-up; runs in background thread; solution offered to the LLM
   as a tool-provided candidate plan (LLM verifies first 2 steps, then replays).
   Deploy only if probe (#6) shows sources available in rerun; otherwise
   public-set-only for calibration.
3. **DEADSIG veto** (ruichardliu 5.57): (color,size,rect,twins) structural
   signature; class inert K=2 → suppressed from fallback AND LLM clicks;
   any class that ever changed → protected. numpy-only.
4. **GEPA offline prompt evolution** (ghazaros 4.03→): feedback = score +
   levels + analyzer-error trace; artifact `gepa_optimized_prompt.json`
   loaded if present; max_metric_calls 100 offline.

## 4. Small-model / JEPA-class stack (user priority; per-run, in-process)

Design rule from evidence: small models **filter/veto/rank**, never advise in
prose (BlackCat/Sandwich negative results), never block the LLM loop.

- **M1 (v6, CPU, zero-risk)**: novelty/stagnation classifier — 8×8 max-pool
  state key + changed-pixel-bucket rarity (yanggod) + per-level dead-set reset;
  feeds `stagnation` + `novel_states_seen` into tool payload (upgrades our
  existing no-op breaker with footprint-rarity event detection).
- **M2 (v7, small GPU)**: action-effect classifier — 4-conv net (26ch: one-hot
  16 + bg/rarity/edge/row/col + 3 diffs) + action embedding → P(board_changed)
  + P(new_state); trained ONLINE during the run on our own transitions
  (ForgeNet-lite, ~1M params); used to (a) veto predicted no-ops pre-submission,
  (b) rank candidate clicks by predicted novelty. Veto threshold tuned on
  public traces; fail-open.
- **M3 (v8, the Kyutai path)**: TD-JEPA-lite — φ/ψ encoders latent 128 L2-norm,
  64-dim action embedding, successor predictor MLP, EMA target 0.995, TD
  smooth-L1 + one-step + orth losses; **BFS-expert distillation on public games
  locally, then online GPI filtering of the LLM's top-K candidate actions**
  (score = max_g succ(φ,a,g)·g). Deployment-safe even if hidden games ship no
  sources: it learns from live experience.
- **M4 (optional)**: `guychuk/arc-agi-3-grid-jepa` public checkpoint as encoder
  init for M3 (test transfer on 25 public games first).
- **Router (deferred)**: learned per-game route selection (LLM vs BFS vs M2+M3
  filtering) — contextual bandit on (game features, level index, elapsed);
  only after M2/M3 produce stable per-route win rates (P6 of old plan).

## 5. Scheduler & scoring math (110-game reality)

- Per-game budget = remaining_time / games_left (adaptive), give-up at 2.5×,
  soft deadline buffer 600 s, artifact margin 2400 s (xiaoyan12 wave formula).
- Keep `ONLY_RESET_LEVELS=true` (LLM continuity) — do NOT adopt double-RESET
  best-of-N (conflicts; only sensible for tape agents).
- Efficiency lever stays quadratic: plan caps + ddmin-style solution shortening
  on replayed plans (30 s validation budget).

## 6. Variance & reliability (0.46-vs-4.33 lesson)

- Pre-run canary cell: 8 probe LLM calls + tool-call parse check before solver
  start (xiaoyan12 harmony-canary pattern); abort fast if hard failures ≥3.
- assert-teeth on every monkeypatch (anchor count must equal expected).
- Watchdog: /v1/models poll 15 s, 4-failure → `solver._stop_event` (graceful,
  completed levels score), max 2 restarts.
- Usage probe JSONL ~200 B/request (THUI) replacing heavy request logs.

## 7. Ops calendar (39 days)

| Window | Action |
|---|---|
| Sep 24–26 | v6 build + full gauntlet; re-arm push-retry; **pause non-ARC GPU jobs during push window** |
| Sep 26–28 | v6 run → auto-submit; mine traces same day |
| Sep 28–Oct 2 | v7 build (27B smoke on CPU-side compat test + BFS side-channel + DEADSIG); run 2 |
| Oct 2–9 | M2 online-classifier + M3 TD-JEPA-lite training harness on public set; run 3 |
| Oct 9–20 | Iterate best line (3 more runs); start daily kernel-diff A/B on public set |
| Oct 20–30 | Freeze top config; 2 confirmation runs (variance bound); final tuning |
| Oct 30–Nov 2 | No risky changes; last slot only for ≥validated best-known config |

## 8. Decision tree (unchanged discipline)

v6 result ≥ 5.0 → proceed v7 as planned; 3.9–5.0 → keep v6 line, fix measured
bottleneck (per-game level completion vs action efficiency from traces);
< 3.85 → rollback to v4 config exactly, resubmit, investigate canary logs.
