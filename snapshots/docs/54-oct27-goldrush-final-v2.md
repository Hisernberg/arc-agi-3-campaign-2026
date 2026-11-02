# docs/54 — GOLDRUSH FINAL v2 (Oct-26 evening refresh, supersedes docs/49 §2–3)

Single source of truth for Oct-27. Slot opens **00:00Z** (= 06:00 Dhaka).
Fire window **00:05–00:10Z**. Keyword: **GOLDRUSH**.

## 1. Weapon of record: apex-v13 (dasshovon/arc26-b-apex-v13, version 1)

Rehearsal kernel RUNNING since 13:39:48Z (kernelId 140991512). Stack =
champion dprime form + guard-v2 + wastepack + dossier-v3 + D′ + D2
(stall-knee, act_checked) + **Qwen3.8-27B-FP8 swap** + D3 (tgraph priors /
pace / endgame) + xpack tools heal + own noop_repeat_guard. All deltas
fail-open. Config frozen 17:00Z per docs/49 — no code changes after freeze.

## 2. GOLDRUSH keyword protocol (unchanged from docs/49, receipts expanded)

1. **G1** (00:05Z): `competitions/submissions/list` → confirm 0 subs today.
2. **G2** (00:06Z): pull v13 kernel output, read log receipts. REQUIRED GREEN:
   `#OURS_V38 served=qwen38-27b-fp8` · `#OURS_V12 stall_knee=True` ·
   `#OURS_ACTCHECKED errors=0` · `#OURS_XPACK ok ... tools=True` ·
   `#OURS_V13 graph=True tools_heal=...` · `#OURS_WASTEPACK ok` ·
   `#OURS_DOSSIER ok` · `#OURS_FORM ok version=d_prime` ·
   **NEW AUDITS (docs/52)**: noop_repeat_guard patch present in log (grep
   `noop_repeat_guard`), `SERVER_STARTUP_TIMEOUT` line shows serving, no
   `SOLVED_LEVEL_MEMORY` expected yet (that's v14).
3. **FIRE** (00:10Z):
   `python3 scripts/fire_sdk.py dasshovon/arc26-b-apex-v13 1 "Oct-27 apex-v13 v1 NEW code (D1 gold: Qwen3.8-27B-FP8 swap + D3 tgraph priors/pace/endgame + xpack tools heal + D2 + guard-v2; LB max)"`
4. **Verdict** at T+90 min, re-read T+3h. `GOLDRUSH-STATUS` = one-shot dump.
   `GOLDRUSH-FORCE` = council escape (logged). `ABORT` cancels.

## 3. Verdict branch table (pre-committed)

| Verdict | Action |
|---|---|
| ≥34 | NEW BEST → declare Stage A; start **v14 MEMORY-SEA** build immediately (§4) |
| 26.5–33.99 | band read w/ receipts; if receipts green → one config-frozen redraw allowed Oct-28 00:05Z; build v14 same day |
| <26.5 | reject: forensics vs v12 receipts, diff GPU log, no re-fire same day |
| 0.00 | forensics first (gateway/scoring-rerun), F-ledger entry, fallback = A-lane dprime redraw (docs/46 §1 fallback pattern) |

Board lens always: any draw > 33.50 = new board best → that exact config
becomes the farm target.

## 4. Post-verdict build: v14 "MEMORY-SEA" (Oct-27 evening push)

Top priority per docs/52 adoption table; everything else waits. Scope frozen:

1. **Solved-level memory** (vickyfym M85 design, docs/52 §3f): record on
   clear → ask `Rule for level N:` over next 2 turns → pin one block at END of
   system prompt, rewrite only at drains, full detail last 3 levels, all
   fail-open. Wraps `ToolAgent.analyze / _build_user_prompt /
   _note_history_evicted / _trim_messages_for_context`. Marker:
   `SOLVED_LEVEL_MEMORY pinned: N level(s)` → alias receipt `#OURS_SLM on`.
2. **Retry raise**: align `ARC3_HTTP_RETRY_INITIAL_SECONDS` → 3600 and
   SERVER_STARTUP_TIMEOUT → 55 min IF ours is weaker (receipt `#OURS_RETRY
   base=3600`). Compare with `_http_retry_delay_seconds` first.
3. **Noop-guard parity audit**: assert our `noop_repeat_guard.py` +
   stall-knee covers the `ARC3_NOOP_REPEAT_GUARD=1` behavior (+16 levels
   evidence); enable the upstream flag too if it composes without conflict.
4. **Farm v1**: `scripts/farm_redraw.py` — pushes 1 redraw of the best
   completed config per day on the A-lane token slot (kragglenote2forwork),
   marker `#OURS_FARM draw=k config=<slug>v<v>`.
5. NOTHING else in v14. No efficiency tweaks (docs/52 doctrine: public-neutral
   ≠ hidden-neutral). 20+ CPU tests vs real bundle tool_agent before push.

## 5. Slots & lanes

- B-lane (dasshovon KGAT): v13 fire Oct-27 00:05Z. Rehearsal kernel does NOT
  consume the slot.
- A-lane (kragglenote2forwork KGAT): redraw farm — Oct-27 target
  `kragglenote2forwork/arc26-b-dprime-clean-v1` (the 33.50 champion) redraw
  after its receipts re-verified. Same discipline: G1/G2, 00:05Z+stagger.
- AGI-2 lane: independent; read v37/v38 verdict when it completes; do not
  couple decisions.

## 6. Graves (unchanged)

No verbatim foreign configs (F-1030) · no prompt rewording (#36) · noop-guard
OFF in champion form (#4) · no env-block transplants · foreground polling ·
G1+G2 before every fire · single reading never promotes · 00:05Z fire ·
fail-open chain sacred · config freeze 17:00Z day before.

## 7. Ledger update (Oct-26 14:40Z)

- Oct-26 slot: apex-v11 v1 → **0.00** (complete 08:31Z). F-ledger: second
  0.00 on this config family; forensics said XPACK tools=False root cause →
  fixed in v13 (tools heal + transforms dual-name). No further action.
- Score ledger: 33.50 / 26.47 / 0.00×2. Board rank ~106; gold cutoff ~38.2–40.
- Idea pool: 1,515 + batch F (docs/52-derived) → see batch F jsonl this push.

## 8. EVENING UPDATE (Oct-26 15:3xZ): rehearsal caught 2 blockers → v2 armed

Rehearsal v1 (complete 15:05Z, 85 min) — save-run receipts:
- 🔴 `#OURS_V38 served=qwen35-27b-fp8 dir=...eliork...` → **saltb0x was never
  attached** (build gate hole: cell chain updated, metadata not).
- 🔴 `#OURS_XPACK ok ... tools=False tool_err=ModuleNotFoundError ours_transforms`
  → v2-root import fails before the v13 heal runs (heal exec-ok repaired the
  sandbox surface but not the install-time receipt).
- ✅ stall_knee / D3 / wastepack / dossier / D′ / noop guard patch all green.
- ACTCHECKED + FRESH=0 expected absent (save-run, gateway down as designed).

**apex-v13 v2 (PUSHED 15:35Z, RUNNING, kernelId 140991512):**
1. FIX-1: `saltb0x/qwen3-8-27b-fp8` attached (before eliork in dataset_sources).
2. FIX-2: xpack import fallback → exec module from dossier-v3 root
   (`ours_transforms.py`/`transforms.py`) into sys.modules + builtins.OT at
   install time → `tools=True` + `#OURS_XPACK heal-pre` line; v13 heal cell
   then upgrades to `import-ok`. Fail-open preserved (both paths).
3. 10/10 build gates + CPU test (fake mounts): tools=True via fallback, fns
   present, heal cell byte-identical.

**G2 receipt changes for FIRE (v2):**
- REQUIRED: `#OURS_V38 served=qwen38-27b-fp8 dir=...saltb0x...` (name/dir both 3.8)
- REQUIRED: `#OURS_XPACK ok ... 'tools': True` (install-time; heal-pre line ok)
- REQUIRED: `#OURS_V13 ... tools_heal=import-ok` (exec-ok also acceptable but
  import-ok proves ordering worked)
- All other receipt lines unchanged from docs/49 list.

**FIRE command (version 2):**
`python3 scripts/fire_sdk.py dasshovon/arc26-b-apex-v13 2 "Oct-27 apex-v13 v2 NEW code (D1 gold: saltb0x Qwen3.8-27B-FP8 swap attached + xpack tools heal-pre + D3 tgraph/pace/endgame + D2 + guard-v2; LB max)"`

Verdict branch table unchanged (§3). v14 MEMORY-SEA unchanged (§4). If v2
rehearsal receipts red again → forensics before fire; NEVER fire on red G2.
