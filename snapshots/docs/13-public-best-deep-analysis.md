# 13 — Public-Best Notebook Deep Analysis: `taaf-flashnext-sheetu12b-0922`

Campaign doc · 2026-09-27 · status: analysis only, **no submission made** (user submits manually)

---

## 0. Provenance and identity

**Uploaded file**: `taaf-flashnext-sheetu12b-0922 (1).ipynb` — did not land on the server disk
(upload failed silently; `/home/z/my-project/upload/` verified twice). Analysis below is **not
weakened** by this, because the filename + our local assets pin its identity with near-certainty:

| Evidence | Conclusion |
|---|---|
| Name prefix `taaf` | Tufa ARC-AGI Framework — the Tufa Labs public submission notebook lineage |
| Name infix `flashnext` | Runs `qwen3-8-flash-next` (Qwen3.8-Flash-Next-NVFP4) — the exact model we serve |
| Name infix `sheetu12b` | Author handle of the fork; a community copy-and-run of the public Duck harness |
| Name suffix `0922` | Sept 22 build — newest public revision of that line |
| Local bundle `SOURCE_IDENTITY.json` | Baseline dataset `keithtyser/taaf-duck-qwen38-flash-next-nvfp4-mtp-smoke-v1`, MIT-licensed, "public-25 and competition-ready vLLM serving bundle" |

The public Tufa notebook we hold (`taaf_kaggle_run_share.ipynb`, 17 cells) states it plainly:
*"You will only find infrastructure and diagnostics in this notebook; the actual solver code is
in an attached dataset."* A fork like sheetu12b's therefore = **the same Tufa infra + a dataset
bundle + (usually) a small customization-hook cell**. We possess the full solver source of that
bundle (4,400 unchanged baseline files verified by manifest SHA-256), so this analysis reads the
*entire effective program* the notebook executes, not just notebook cosmetics.

**What this notebook is on the leaderboard**: the best publicly copyable score — i.e. the score
ceiling of "stock Duck harness + Qwen3.8-Flash-Next-8B". That makes it our direct competitive
reference point: whatever our v-series achieves above it is attributable *purely to our harness
patches*, which is exactly the experiment we want clean.

---

## 1. The complete stack, layer by layer

### Layer 0 — Notebook shell (17 cells, pure plumbing)
Detects real competition rerun via `KAGGLE_IS_COMPETITION_RERUN` and switches diagnostics off +
soft deadline on. Installs `arc-agi` from the offline wheelhouse (`--no-index`), locates the
source bundle by **marker file** (not fixed mount path — robust to Kaggle mount-layout changes),
resolves every attached dataset/utility-script mount, writes a setup-env JSON handoff, puts
bundled repos on `sys.path` **and** writes a `.pth` file so child processes (the serving stack)
see them too, unpickles `deploy_target.pkl` + `benchmark_initial.pkl`, exposes a customization
hook cell, then runs. Two details worth copying:

- **`_wait_for_gateway`**: polls `api/games` up to 600 s before swapping in the live game list —
  the Kaggle gateway boots asynchronously and a naive run would race it.
- **Teardown in `finally`**: teardown commands run even when the run raises, so the serving
  stack never leaks GPU memory into the scorer's view of a crashed run.
- Offline (interactive) mode plays the **bundled competition environment files** end-to-end with
  no gateway, and still writes a valid placeholder `submission.parquet`. This is why Duck
  iteration is fast and why our own local-CPU loop (built independently in Task 1) matches.

### Layer 1 — TAAF framework (`taaf/`, 7,813 lines)
- `Solver` base class: strict lifecycle contract (`setup()` → `run_games()` → `teardown()`), a
  **must-yield-every-5s rule**, and a documented cancellation protocol (on `CancelledError` the
  solver must `finish_game()` every still-playing game and re-raise; `finish_game()` reads the
  task's cancelling state to pick `cancelled` vs `gave_up`). This is why Duck runs die cleanly
  at the 32,400 s wall instead of forfeiting.
- `Benchmark` (480 L): holds games, `n_passes`, optional `game_weights`, orchestrates the run,
  skips its own JSON/HTML/sidecar saves in minimal-diagnostics mode.
- `game.py` (688 L) contains a **local mirror of the official scorer** (v0.9.8):
  `level_score = min(115, (baseline/actions)² × 100)` for completed levels, weighted average,
  capped by `max_weights/total_weights × 100`. Having the true score formula *inside the agent's
  runtime* is what powers time/budget-aware play (below).

### Layer 2 — Serving stack (the KV-budget holder)
From `SOURCE_IDENTITY.json` (`serving_recipe`):

| Setting | Value | Why it matters |
|---|---|---|
| server | vLLM `0.1.dev20073+g8e685d198` (pinned image digest) | reproducibility |
| quantization | `modelopt_fp4` (NVFP4) + PLE CPU-offload patch | fits 135 GB model on one RTX Pro 6000 |
| native MTP | `mtp`, **3 speculative tokens** | big decode speedup on an 8B |
| `max_model_length` | 32,768 | our KV ceiling: ≈3.21 full contexts |
| `max_num_seqs` / concurrency | 28 / 28 workers | matches 25 public games (all playable in parallel) |
| **`prefix_caching`** | **False** | deliberate: 28 interleaved conversations thrash the prefix cache; the KV spent caching shared system prompts across 28 concurrent sequences is KV taken from live sequences. Also a hint: their prompts are long but *per-game-divergent early*, so hit rates would be low. |
| chunked prefill | True (primary) | latency smoothing under 28-way load |
| parsing | `reasoning_parser=qwen3`, `tool_parser=qwen3_coder` | model-native thinking + tool-call syntax |
| watchdog | 15 s interval, 5 s request timeout, 4-failure threshold, 2 restarts | server liveness without burning competition time |

Fast-start mode (`TAAF_KAGGLE_FAST_START`) skips every verification not owned by the run
(weight re-hashing, recursive cache scans, synthetic preflights) — boot time is competition
time.

### Layer 3 — HarnessSolver (`inference/framework/solver.py`, 1,278 L)
- **Concurrency model**: one `ThreadPoolExecutor` sized exactly to `concurrency` (they document
  why: `asyncio.to_thread`'s default executor caps at `min(32, cpu+4)` and would silently cap
  real concurrency below 28), asyncio semaphore + `gather` over `shield`ed tasks, 120 s cancel
  drain, then `_finish_remaining` finalizes scores for everything still playing.
- **Per-game session** (`_HarnessGameSession`): owns `state_path` (the JSON runtime-state file
  the sandbox reads), transcript, viewer events, token baseline. `should_stop()` = run not
  playing ∨ stop event ∨ engine WIN ∨ per-game 7,920 s elapsed ∨ action cap.
- **`play()` loop**: `analysis_step += 1` → write runtime state → `analyzer.analyze(...)`.
  Retryable failures (network) re-enter the *same* analysis step with 1 s backoff;
  `yielded_control` results re-enter too (time-budget yield, not a failure). Engine GAME_OVER is
  answered by a **harness-side auto-RESET** (`_execute_auto_reset`) — no LLM call is spent
  re-learning that the game is over.
- **`step_env`** — the single chokepoint for every real action:
  - validates `action`/`actions` (never both), MOUSE forced to integer `row`/`col` clamped 0–63
    (legacy `x`/`y` **rejected** — kills a whole class of model confusion),
  - per-action validity check against `current_state.available_actions` (invalid → structured
    error carrying the *current* valid list, so the model self-corrects in the next tool call),
  - executes the batch, breaking early on `run_complete`/`game_over`/`level_completed`
    (`stop_reason` recorded), sums rewards, and returns a **compact result dict**: `executed,
    action_num, level, score, reward, state, valid_actions, board_changed, done,
    level_completed, game_over, run_complete, action_display, batch_index/size, requested/
    executed_count, stopped_early, stop_reason, run_elapsed_seconds, time_remaining_seconds`.
  - `board_changed` = previous grid ≠ new grid (pure harness fact, no model judgment).
  - **Every action result carries the remaining per-game time.** The model can pace itself.
- **Reward shaping**: `reward = Δlevels_completed / number_of_levels` — dense, aligned with the
  official scorer, cheap.
- Token accounting: `_analyzer_reported_tokens` diffs a per-session baseline at every action, so
  `generated_tokens` attached to each engine action is exact even across batches.

### Layer 4 — ToolAgent (`inference/agent/tool_agent.py`, 2,064 L) — the agent brain
**One tool: `python`.** Everything else is code the model writes. Turn structure:

1. `_build_user_prompt`: previous-step summary ("executed N actions: …; level transition /
   game over / same level"), state line (step, level, observed max level), valid actions,
   four lines of tool guidance, the **world-model revision mandate** ("BEFORE EXECUTING NEW
   ACTIONS YOU MUST ALWAYS GIVE THE REVISED VERSION OF THE WORLD MODEL"), the carried world
   model (`_summarized_knowledge_lines`), and a first-turn vs later-turn focus hint.
2. Up to **12 inner LLM calls** per turn (`LOCAL_ANALYZER_TOOL_STEPS`), each trimmed to the
   context budget (`32K − reply_reserve − 512`), tool-forced to `python`, with:
   - no-tool-call → nudge ("You have not acted yet. Investigate first…"), loop continues;
   - tool call → dispatch sandbox; if a real step executed → **break** (one turn = one batch);
   - context-overflow error → trim harder (extra 512 tokens) and retry, then force-reduce;
   - `should_stop` or turn-time-budget → `yielded_control` result, control returns to solver.
3. History persistence: keep the **last 30 assistant turns** (`_PERSISTENT_HISTORY_ASSISTANT_TURNS`),
   token-budget-trimmed from the oldest block; on any exception, revert to pre-turn history
   (`preserve_history=False`) — a poisoned turn never contaminates the future context.
4. Response hygiene: `<think>` stripped, tool-call markup recovered from reasoning/content if
   the parser produced none, malformed-JSON arguments reported back as structured errors.

**The world-model note system** (this is the heart):
- `_extract_scientist_note` parses labeled blocks out of the model's own prose: `World model:`,
  `Goal model:`, `Action model:`, `Recent findings:`, `Open questions:`, `Plan:`,
  `Cross-level notes:` (fallbacks: `Hypothesis:`, `History check:`, `Next test:`).
- Persisted harness-side in `_summarized_knowledge`, **re-injected in every user prompt** — so
  the notes survive context trimming *by construction* (they are rebuilt fresh each turn
  regardless of how much old history was dropped).
- On `level_transition`/`run_complete`/`game_over`, per-level keys are wiped
  (world/goal/action model, findings, questions, plan) but **`cross_level_notes` survives** —
  a deliberate cross-level transfer channel.
- `_update_summarized_knowledge_from_assistant` runs on *every* assistant content, with or
  without a tool call.

**Sampling/config defaults** (all env-overridable): temperature 0.6, top_p 0.95, top_k 20,
thinking ON, max output unset, tool output cap 1,024 tokens (4,096 chars), python timeout 30 s,
seed −1.

### Layer 5 — Python sandbox (`python_tool_sandbox.py`, 577 L)
- **Subprocess isolation**: `python -I -S -c <bootstrap>` in its own process group (SIGKILL via
  `killpg` on timeout), tempdir cwd, scrubbed env, `RLIMIT_CPU = timeout+1`, `RLIMIT_FSIZE 1 MB`,
  `RLIMIT_NOFILE 32`.
- **Whitelist execution**: ~60 safe builtins + 14 stdlib modules, guarded `__import__`. The
  segmentation source is **spliced verbatim into the bootstrap** (`inspect.getsource`), so the
  sandbox needs no project imports.
- **JSON-line IPC with mid-Python `action()`**: the model's code can call `action([...])` any
  number of times *inside one tool call*; each call sends the action to the host, the host
  executes a real env step, returns the compact result + refreshed frame payloads, and the
  sandbox refreshes `current_frame/history/transitions/previous_frame/last_action_result`
  **before the next Python statement runs**. This is a closed perception→search→act loop inside
  one tool call — the single most powerful mechanic in the design.
- `transitions` are reconstructed in-sandbox from history; sanitized tracebacks show only
  `<python_tool>` frames (no harness internals leak, fewer tokens).
- Host side has a reader thread + deadline loop, so a hung sandbox costs exactly its timeout,
  not the game.

### Layer 6 — Typed perception (`segmentation.py`, 204 L)
- 4-connected flood-fill components in reading order (stable IDs), each node = `id, color,
  hash, pixels, boundary, children` + `adjacency_list`.
- **`hash` = translation-invariant object identity** (color + shape normalized to bbox origin,
  SHA-1 16-hex) — the model can track "the same object" across frames, spot duplicate objects,
  and detect motion/spawning *without burning tokens re-describing bitmaps*.
- `boundary` = Moore-neighbour contour trace reduced to corner points (compact outlines).
- `children` = true nesting tree (innermost encloser), computed by border flood-fill per
  candidate encloser.
- Exposed lazily (`frame.segmentation` property, cached per view) and documented exhaustively
  in the prompt — including the trap warnings (`history[-1].frame` is the *current* frame; use
  `previous_frame`/`last_transition.before_frame` for diffs).

### Layer 7 — Prompts (`prompts.py`, 114 L — dense, every line earned)
Six addenda assembled into one system prompt: game overview (multi-level framing, observe-plan-
act per turn, "solve the entire game", fewest actions), structured runtime state contract,
optional multimodal note, visual-game guidance (**HUD/timer-bar warning with "DON'T DO THIS!"**,
no-avatar warning, re-ground after score jumps), Python guidance (segmentation-first viewing,
no full-board scans, ephemeral calls, restricted imports, **BFS/search emphasis**, "stop probing
and search in the inferred state space", never print full boards, batch verified sequences,
stop on terminal flags), and tool-session rules (one tool, many calls per step, 30 s cap,
output budget). Prompt text teaches *semantics and failure modes*, not just API syntax.

### Layer 8 — Action naming (`action_names.py`)
`ACTION1..6 → UP/DOWN/LEFT/RIGHT/SPACE/MOUSE` in both directions. The model plans in semantic
space; the engine receives engine IDs; MOUSE data is normalized to `row`/`col` end-to-end.
Tiny file, outsized effect on an 8B model.

---

## 2. Why this wins — mechanism-level analysis

1. **Code-as-action with mid-code environment access.** The model doesn't emit an action token
   per step; it writes a *program* that may inspect typed state, run a search (BFS over the
   inferred world), and call `action()` several times — with each call's observation refreshed
   before the next statement. For a small model, offloading per-step control flow to Python is
   worth more than any prompt engineering. This is NOOA's "code as action" + "programmable loop
   engineering" realized with minimum machinery.
2. **Typed object perception replaces token-expensive vision.** The segmentation gives an 8B
   text model structured "eyes": object identity that survives motion (hash), containment
   (children), and adjacency. The prompt then *bans* whole-board ASCII scans. The result: board
   understanding costs ~hundreds of tokens instead of 4K+ of raw grid, protecting the 32K
   ceiling and the KV budget.
3. **The world-model note system is compaction done right.** Notes live in harness memory, are
   re-injected every turn, and survive context trimming by construction. Per-level notes are
   wiped on level change (correctly — the scene invalidated them), while `cross_level_notes`
   persists (mechanics often transfer). This is the same insight PRO-LONG formalized
   (arXiv:2607.20064: append-only searchable history +18 pp at 4–6× fewer tokens) in a cheaper
   form — but only for what the model *thinks* to write down.
4. **Harness-computed facts anchor the model.** `board_changed`, `valid_actions`,
   `levels_completed`, `time_remaining_seconds` are all ground truth from the engine. The model
   never has to trust its own memory about whether the board changed. NVIDIA's "harness beats
   model" lesson (RHAE 183/183) is visible here in miniature.
5. **Score-formula awareness.** Per-level efficiency is quadratic in actions
   (`(baseline/actions)²`), so the harness *shows* the model the remaining per-game time every
   step and (in our fork) the human-budget prior. The design pushes the model toward banking
   levels cheaply rather than grinding.
6. **Failure hygiene everywhere.** Invalid action → structured error + valid list; terminal
   state → terminal payload with no execution; auto-RESET without an LLM call; poisoned turns
   reverted; hung sandboxes killed at exactly 30 s; server watchdog restarts. Nothing compounds.

---

## 3. Delta vs our v4 (`duck-worldmodel-v1`, LB 3.85) and v5

Our kernels are built **on this same bundle** — so everything in §1 is already ours. The delta
is our patch cell (20,870 chars, wrapper `duck_worldmodel_v1_1`, idempotent + fail-open):

| Mechanism | Stock Duck (this notebook) | Our v4/v5 | Verdict |
|---|---|---|---|
| REPL + mid-Python `action()` | ✔ | ✔ (inherited) | parity |
| Segmentation typed perception | ✔ | ✔ (inherited) | parity |
| World-model notes (model-authored, labeled blocks) | ✔ | ✔ + our discipline addendum | we add hypothesis discipline |
| Per-action effects ledger (`changed/tried` per level) | ✘ | ✔ harness-computed | **ours ahead** |
| Dead-action flags (3+ tries, 0 changes) | ✘ | ✔ | **ours ahead** |
| Human-budget prior per level (watch at 1×, over at 2×) | ✘ (time only) | ✔ | **ours ahead** |
| Per-game offline-probed `game_notes` (25 games) | ✘ | ✔ | **ours ahead** |
| No-op-loop governor (3/6/10 notices) | advice-only | ✔ hard counters | **ours ahead** |
| RESET discipline | ✘ | ✔ prompt rule | **ours ahead** |
| Cross-level transfer channel | ✔ (`cross_level_notes` survives) | ✘ not exploited | **Duck ahead — adopt** |
| Searchable append-only log | ✘ | ✘ | open (P0, §5) |
| Harness object-diff per step | ✘ | ✘ | open (P0, §5) |
| Verified-vs-hypothesis memory separation | ✘ (notes are unverified prose) | partial (ledger is separate) | merge needed (P0, §5) |

**Reading**: our v-series already beats this notebook on harness-side per-game facts and
discipline; the public-best's remaining structural advantages over *us* are (a) the
cross-level transfer channel, and (b) whatever its author tweaked in the customization cell —
unknowable without the file, but bounded: the hook cell is 1–3 lines by design and the Tufa
infra is identical. The score gap between "public-best" and our v4 therefore comes mostly from
*what the model does inside the same machinery* (serving parity assumed), which is exactly what
our P0/P1 items below target.

---

## 4. Weaknesses found in the design (source-level read)

These are concrete, verified gaps in the public-best itself — each one is an attack surface for
our next kernel:

1. **No cross-game knowledge.** Every game starts blank; nothing learned in game *k* helps game
   *k+1*. `cross_level_notes` transfers across *levels within a game* only. (Our `game_notes`
   cover the 25 public games, but nothing covers *unseen* semi-private games.)
2. **World-model notes are unverified prose.** `_extract_scientist_note` harvests whatever the
   model claims, in whatever format it happens to use (a slightly-off label = silent loss), and
   reinjects it as authoritative. Tycho's lesson (arXiv:2607.28287: transition match ≠ correct
   abstraction; auto-repair 83.07 < actor-requested 88.49) warns exactly this: *remembered*
   abstractions can be wrong. The notes are never checked against the effects ledger.
3. **No searchable persistent log.** History beyond the last 30 assistant turns is dropped by
   token budget. A fact learned at turn 5 survives *only if* it made it into a note. PRO-LONG's
   +18 pp came precisely from making the full history searchable instead of discarding it.
4. **No-step turns have no guard.** The nudge loop can burn up to 12 inner calls producing
   analysis without a single `action()`; consecutive no-step turns aren't counted anywhere. A
   small model can spin. (Our governor only counts *real no-op actions*, not no-action turns.)
5. **Object diffs are re-derived by the model every time.** Segmentation is exposed, but the
   harness computes no per-step object diff (spawned/despawned/moved via hash matching) — the
   model rewrites that diff code each turn, or skips it and misreads changes.
6. **Inner tool-step budget is generous (12)** — right for a strong model, wasteful when a
   small model rambles; each wasted call costs a full prefill of the (long) context.
7. **Multimodal plumbing exists but is off by default** (`MULTIMODAL_CONTEXT`); enabling it for
   flashnext would cost ~1–2K tokens/image under a KV ceiling of ≈3.21 full contexts. Keep off;
   the text-side typed state is the cheaper sense.

---

## 5. Adoption & improvement plan (ranked; token-budget checked against KV ≈ 3.21 × 32K)

Design law for every item: **net-token-negative or neutral** (KV constraint), env-var
switchable (ablation humility; forge's lesson: be able to turn everything off), fail-open
(any patch error → stock Duck behavior).

### P0 — high EV, low risk, ship next kernel (v6 / duck-worldmodel-v3)

- **P0-1 · Harness object-diff per step** (≈80–150 tok/step injected, replaces 200–500 tok of
  model-written diff calls → net negative). After each batch, compare segmentation hashes
  between pre/post frames: `{spawned: [(hash,color,bbox)], despawned: [...], moved: [...],
  size_changed: [...]}` (hash-prefix + bbox only, cap at 8 entries each). Inject as a
  `obj_diff` field in the tool result. *Mechanism: the model stops re-deriving object motion
  and stops missing it.* This is NOOA's "explicit object state" at minimum cost.
- **P0-2 · PRO-LONG-lite: append-only searchable log + `search_log()`** (net ≈ 0: writes are
  one JSONL line per step host-side; reads only when the model asks). Log every step
  `{step, level, action, board_changed, stop_reason, note_digest}` + world-model note versions.
  Expose `search_log(pattern, last_n=5)` inside the sandbox (stdlib `re` over the file).
  Prompt line: "Older context may have been trimmed; `search_log('KEYWORD')` recovers past
  findings." *Mechanism: nothing learned is ever lost, at zero standing cost.* This is the
  single best-evidenced external result available (+18 pp, arXiv:2607.20064, and it *reduces*
  tokens 4–6×).
- **P0-3 · Verified-memory merge (sync_state)**. Promote the effects ledger + obj_diff to
  authoritative status *inside the note block*: inject as `Facts (harness-verified):` before
  the model's `World model:` prose, and add one prompt line: "If a note contradicts a Fact,
  the Fact wins; revise the note." Optionally flag direct contradictions harness-side
  (e.g. note claims "ACTION3 does nothing" while ledger shows changes > 0 → append
  `⚠ contradiction`). *Mechanism: converts Tycho's repair-paradox from a hazard into a
  self-correcting loop without any auto-repair machinery.*
- **P0-4 · Cross-level transfer hardening** (adopt the public-best's channel, then go one
  better): keep our existing discipline addendum but (a) instruct the model to always maintain
  a `Cross-level notes:` line with mechanics confirmed by ≥2 levels, and (b) preserve the last
  level's final effects-ledger row as `previous_level_effects` injected at level start —
  mechanics that survived the previous scene are the best first hypotheses for the next one.

### P1 — medium EV, needs local measurement first

- **P1-1 · No-step governor**: count consecutive turns with `step_executed=False`; at 2, inject
  a hard directive + a suggested cheap probe; at 4, have the harness fire one *deliberating
  probe* itself (highest-validity, lowest-risk action — e.g. the action with highest unknown
  changed-ratio) with a notice. Env-gated `NOSTEP_GOVERNOR=on/off`.
- **P1-2 · Inner-step budget 12 → 6** for the 8B (the turn already breaks on step execution,
  so the cap only bites on stuck/rambling turns), saving up to 6 prefills per stuck turn.
  Measure on 3 CPU-traced games before shipping.
- **P1-3 · Game-archetype priors for unseen games**: extend `game_notes` from "per-game
  strings for 25 known IDs" to a 2-probe classifier: after step 1–2, harness classifies
  {click-responsive, keyboard-movement, sequence-gated, timer-bar-HUD} from board-change
  patterns and injects the matching playbook block. Covers the semi-private set where our
  per-game notes don't exist.
- **P1-4 · Level-start budget line**: we already inject human-budget for known games; add the
  *observed* per-level action counts of the current run so the quadratic-decay warning is
  grounded in this run, not just the prior.

### P2 — M1+ / explicitly gated

- **P2-1 · Actor-requested skill shelf (Tycho 88.49 lesson)**: sandbox gains `save_skill(name,
  code)` / `load_skill(name)`; only stores what the model explicitly asks to keep; **no
  auto-repair, no auto-invocation**. Token cost: skills are re-shown only on request.
- **P2-2 · JEPA-lite novelty sanity**: cheap hash-embedding surprise score per step, exposed as
  `novelty` field. Never drives actions autonomously; only a salience hint. (HAL/JEPA line:
  useful as *signal*, dangerous as *driver* — matches our "never autopilot" rule.)
- **P2-3 · Typed memory store (NOOA +11.8 pp lesson)**: SQLite `mem_write/mem_query` with
  supports/contradicts edges, replacing free-text notes *only if* P0-3's contradiction flags
  show the model actually abuses prose memory. Heavier; defer.

### Explicitly NOT adopted (with reasons — keep the anti-list)

- Auto-repair loops on failed skills (Tycho: −5.4 pp vs actor-requested).
- Forced flexible-executable world models (ablation paper: textual beat flexible-executable
  twice on low-capability models — that is us at 8B).
- Heavy hand-built perception beyond segmentation (Tufa's own ablation: "hand-crafted tools
  actually hurt"; Anim15/forge: best runs close extra machinery).
- Vision context for the 8B under our KV ceiling (§4.7).
- Raising `max_num_seqs` beyond 28 or turning prefix caching on (KV thrash under 28-way
  interleave; Duck's choice is correct and now understood).

---

## 6. What we verified about parity (sanity for the campaign)

| Dimension | Public-best lineage | Ours |
|---|---|---|
| Model | Qwen3.8-Flash-Next-NVFP4 (RadixArk, pinned rev) | identical |
| Serving | vLLM pinned digest, MTP×3, fp4, 32K, 28×28, prefix-cache off | identical |
| Runtime budget | 7920 s/game, 32400 s total, 28 workers, timeout 900 s | identical (cell 13 asserts 32400) |
| Scoring mirror | `min(115,(baseline/actions)²×100)` weighted | inherited |
| Concurrency plumbing | custom pool sized to concurrency (documented trap avoided) | inherited |
| Fail-open patch discipline | Tufa: customization hook | ours: idempotent wrapper + fail-open + tests |

**Bottom line**: the public-best is our own foundation, run clean. Our edge must (and can) come
from the P0 set: verified memory, searchable history, free object diffs, cross-level transfer —
each independently env-switchable, each token-negative or neutral, each backed by either the
2026 literature or our own trace analysis. That is the concrete path from 3.85 toward the 9–10
band without touching the model or the serving stack.

---

## 7. Appendix

### A. Source map (what each file does)
```
duck_bundle/
├── taaf-kaggle-bundle.json / SOURCE_IDENTITY.json   # identity, serving recipe, run contract
├── setup_commands.json / teardown_commands.json     # serving lifecycle
├── serving_setup.py / serving_teardown.py           # vLLM boot (fast-start, gates, watchdog)
├── benchmark_initial.pkl / deploy_target.pkl        # pickled run configuration
└── src/
    ├── tufa-arc-agi-framework/src/taaf/             # L1: benchmark + solver contract + scorer mirror
    │   └── kaggle/taaf_kaggle_run_share.ipynb       # L0: public notebook (infra only)
    ├── ARC3-Inference/inference/
    │   ├── agent/tool_agent.py          # L4: turn loop, notes system, trimming, retries
    │   ├── agent/prompts.py             # L7: six addenda
    │   ├── agent/python_tool_sandbox.py # L5: subprocess REPL + action() IPC
    │   ├── agent/runtime_state.py       # frame/history JSON persistence
    │   ├── agent/segmentation.py (utils)# L6: typed perception
    │   ├── agent/action_names.py        # L8: semantic action names
    │   ├── agent/vision_context.py      # optional multimodal (off)
    │   └── framework/solver.py          # L3: concurrency, sessions, step_env, auto-RESET
    └── sglang-rtxpro6000/               # (unused by this recipe; vLLM is the server)
```

### B. Key env-var matrix (agent-behavior surface)
`LOCAL_ANALYZER_TOOL_STEPS=12` · `LOCAL_ANALYZER_TOOL_OUTPUT_TOKENS=1024` ·
`LOCAL_ANALYZER_TOOL_TIMEOUT=30` · `LOCAL_ANALYZER_TEMPERATURE=0.6` · `TOP_P=0.95` ·
`TOP_K=20` · `LOCAL_ANALYZER_ENABLE_THINKING=true` · `LOCAL_ANALYZER_CONTEXT_WINDOW=32768` ·
`MULTIMODAL_CONTEXT=(off)` · `TAAF_RUN_AS_SUBMISSION` · `TAAF_MINIMAL_DIAGNOSTICS` ·
`ONLY_RESET_LEVELS=true` (pinned level-reset-only semantics) · `TAAF_KAGGLE_FAST_START`.

### C. Provenance note
Uploaded file absent from disk at analysis time (checked 2026-09-27 07:0x, twice, after wait).
Identity pinned via filename anatomy + `SOURCE_IDENTITY.json` manifest match (4,400 unchanged
files). If the actual `sheetu12b` customization cell differs, it can only touch `bm`/`bm.games`/
`bm.solver` post-load — re-run `scripts/dump_nb.py` on the file when available and diff cell
count against the 17-cell public original.
