# 15 — APEX v8: the most-advanced build (every part upgraded, validated)

Campaign doc · 2026-09-27 · status: **built + validated, NOT submitted** (user submits manually)

Base: exact pulled 3.85 kernel artifact (`kernels/v4base/`), only cell 14 replaced
(byte-diff enforced: cells `[14]` differ, all else identical to the scored source).
The v8 patch carries the v7.1 state-key fix plus **one more real bug fix** found by
validation (below). Patch: `kernels/apex_v8_patch.py` (≈47 KB). Notebook:
`notebooks/duck-apex-v8/` (kernel id `kragglenote2forwork/duck-qwen3-8-anim-base-35c14d`,
title `Duck Qwen3.8 Apex v8`, same competition/dataset/model attachments).

---

## 0. Design law (unchanged from doc 13 §5, still absolute)

1. **Net-token-negative or neutral** — KV ceiling is ≈3.21 full 32K contexts; every
   injected field must displace more model-token spend than it costs.
2. **Env-switchable per mechanism** — ablation humility (forge's lesson: best runs can
   close everything).
3. **Fail-open** — any patch error → stock Duck behavior; never break the harness.
4. **No autopilot** — the harness never fires actions on its own; it informs, warns,
   and records. (Tycho lesson: model-owned decisions beat harness-repair.)

## 1. What was built (7 mechanisms, [A]–[G])

### [A] ASCII engine — harness-side frame delta (`_AsciiEngine`)
`diff_grids()` diffs the **raw integer grids** (reversible: `format_grid_ascii` maps
color IDs many-to-one, so rendered-ASCII diffs silently miss recolors — found by the
ft09 smoke run and fixed). Output grammar: changed cells `r,c:old>new` (≤28 cells) or
row-RLE `r{rr}:nC,nC...` for big rewrites (+ `win` = active-window bbox of non-background
cells, `md5` frame digest). Injected as `frame_delta` in the tool result only when the
board changed, else the single word `unchanged`.
**Token math**: ~25–80 tokens per step injected vs 200–500 tokens of model-written diff
code + printed boards it replaces → net-negative. The model stops re-deriving *what
changed* and stops misreading it.

### [B] Advanced segmentation — object tracking across frames (`_ObjTracker`)
Imports the bundle's own `segmentation.segment_layer` host-side (fail-open to disabled).
After every executed batch: match pre/post objects by translation-invariant shape hash →
`obj_diff` = `{sp: spawned, de: despawned, mv: moved (from>to bbox), rs: resized}` with
hash-prefix + bbox, cap 8 each, plus a **`mover` role hint** (solo small mover = likely
avatar). `same:1` when nothing changed.
**Token math**: ~30–90 tokens vs the model rewriting flood-fill diff code each turn
(often 300+ tokens, often skipped → missed object events). This is NOOA's "explicit
object state" at minimum cost.

### [C] Tokenizer-level work (`_TokMeter` + soft cap)
- Uses a **real BPE tokenizer** when `tokenizers` + a `tokenizer.json` is reachable
  (model mount), else a class-aware estimator (ASCII-art/JSON lines count at 0.45
  tok/char, prose at 0.30 — measured BPE behavior on grid/coordinate text).
- **Per-step telemetry** into the JSONL log: `tok_result` (tool-result size), section
  sizes offline — no prompt cost, feeds next-iteration tuning.
- **Soft cap `WM_TOKCAP`** (default 700 est-tokens): if the injected knowledge block
  exceeds it, lowest-priority fields drop first (`macro_hint → recent_log → note →
  contradiction → memory → game_notes → previous_level_effects`); ledger/budget/pred
  are never dropped.

### [D] World-model harness — verified facts + contradiction guard + transfer
- v7.1 stack carried intact: per-game priors, typed memory, predict-verify, JSONL.
- **Ledger = facts**: the effects ledger is already harness-verified; v8 adds a
  **contradiction scan** (`WM_FACTS`): if a memory note claims action X is dead while
  the ledger shows changes>0 → `contradiction` flag injected. Tycho's repair-paradox
  becomes a self-correcting loop *without* auto-repair.
- **`previous_level_effects`** (`WM_TRANSFER`): the cleared level's verified summary is
  injected at the next level's start — mechanics that survived the previous scene are
  the best first hypotheses for the next one (hardened cross-level channel).

### [E] LLM + non-LLM hybrid — macro replay memory (`WM_MACRO`)
The harness records each level's **verified action sequence** (≤160). After a RESET, the
world_model block carries `macro_hint`: "re-run prefix (N): ACTION1,ACTION2,…" — the
model re-runs the known-good prefix as ONE batched call instead of re-deriving it.
Non-LLM execution knowledge, zero standing token cost (hint shows only during the
replay window, `len(prefix)+4` actions). This is the cheapest possible form of the
"exact replay" lever every T3+ team uses — no simulator required.

### [F] No-step governor (`WM_NOSTEP`)
Counts analysis-only turns (the public-best has **no guard** here — doc 13 §4.4).
At 2: hard directive. At 4+: directive + cheapest-unexplored probe suggestion from the
ledger. Still no autopilot — the harness suggests, the model fires.

### [G] Prompt v2 (measured +≈140 tokens/turn on the system prompt)
Teaches the new fields (`frame_delta`, `obj_diff`, `macro_hint`), the banker math
("score decays quadratically once actions exceed the human baseline"), and to trust
harness-computed facts over re-derivation. v7's discipline text fully preserved.

## 2. Bug fixes carried

| Fix | Impact |
|---|---|
| **v7.1** state-path key collapse (game id inside `.json` filename) | v7 ran with ALL games sharing one state → world-model machinery dead in every prod run incl. v4 3.85. Regex `(.+)_p\d+_tool_runtime_state\.json$` + legacy fallback. |
| **v8** first-observation ledger wipe | v7's level-sync block treated the first compact `level` (1-based) as a transition from 0 and **discarded the first action's ledger entry per game**. Now: first observation adopts the level without wiping; genuine transitions still wipe. Found by the v8 unit suite. |
| **v8** raw-grid delta | rendered-ASCII diff misses recolors (many-to-one glyph map) — raw int grids are the diff source now. Found by the ft09 smoke. |

## 3. Validation (all green)

| Suite | Result |
|---|---|
| `scripts/test_apex_v8.py` — unit, 13 sections | **61/61 OK** (install/idempotency, accounting regression, ascii engine incl. RLE fallback + window, frame capture end-to-end with callback restore + no wrapper chaining, obj_diff incl. spawn/mover via real bundle segmentation, macro generate/persist/clear, nostep escalation, tokcap drop-order, all switches off, fail-open, JSONL telemetry, predict regression) |
| `scripts/smoke_apex_v8.py` — real offline games | **ALL GREEN**, 138 real steps across ls20 (keyboard, animating), ft09 (click-only), sc25 (pairs): zero exceptions, exact accounting, 74/74 frame deltas match recorded-frame ground truth, obj_diff structurally valid every step, JSONL record count == executed count with token telemetry, macro_hint after mid-run RESET, predict flow intact |
| Notebook build | byte-diff vs scored 3.85 artifact: **only cell 14 differs**; embedded cell == kernel patch source; attachments intact |

## 4. Env switch matrix (defaults ON; set "0" to disable)

`WM_GAME_DATA WM_MEMORY WM_PREDICT WM_JSONL` (v7) · `WM_ASCIIDIFF WM_OBJDIFF
WM_TOKMETER WM_MACRO WM_NOSTEP WM_TRANSFER WM_FACTS` (v8) · `WM_TOKCAP` (int, 700) ·
`WM_LOG_DIR` (default `/kaggle/working`) · `WM_DEBUG=1` prints fail-open tracebacks to
run logs (diagnostics) · `WM_PRIOR_BUDGET` (JSON list; per-game baselines auto-override).

## 5. Expected effects (honest numbers)

- v4 (3.85) ran with the world-model machinery **dead** (v7.1 discovery). v8 with
  machinery alive is the first honest test of the full stack — expected direction:
  ≥ v4, with the biggest lifts on click-only and pairs games (obj_diff + frame_delta
  remove their main failure mode: misread changes) and on RESET-heavy games (macro_hint).
- Risks: injected-block bloat (guarded by WM_TOKCAP + telemetry), prompt-addendum
  interference (bounded at +140 tokens), segmentation import failure on the serving
  image (fail-open → ascii-diff only).
- If v8 < v4: next run is a **mechanism ablation** (switches off in pairs) — the env
  matrix makes this a config change, not a code change.

## 6. Deferred to v9 (designed, not built — token-budget discipline)

- `search_log()` inside the sandbox (PRO-LONG-lite): needs a sandbox-globals channel;
  the JSONL log + note digests already give the model the same facts via `memory`/ledger.
- Actor-requested skill shelf (Tycho P2-1) — after macro replay proves the storage path.
- SQLite typed memory (NOOA +11.8) — only if contradiction flags show prose memory abuse.
- Exact-solver side channel (docs/13 §4 master lever) — gated on the hidden-games
  `.py`-sources probe; zero-risk probe stays scheduled.
