# Oct-26 Fire Record — apex-v11 (D1 Gold Attempt)

## Fire
- **UTC**: 2026-10-26 08:31:03
- **Submission ref**: 57659975
- **Kernel**: `dasshovon/arc26-b-apex-v11` v1 (scriptVersionId 362216406)
- **Status**: PENDING at fire time; score expected ~9h later (17:30–22:00Z window)
- **Description**: Oct-26 apex-v11 v1 NEW code (D1 gold attempt: champion dprime form + wastepack + dossier-v1 25 games + XPACK dossier-v2 categories/transform-tools/SFT/RL-seeds + Qwen3.5-27B-FP8 primary; GPU run complete all receipts ok; LB takes max)

## Pre-fire gates (all green)
- **G1**: kernel status = complete (GPU run finished 2026-10-25 17:39Z, RTX Pro 6000 Blackwell); 0 pending submissions; 0 submissions today (UTC) — daily slot open
- **G2 receipts (from kernel output log, `reports/v11_output.json`)**:
  - `#OURS_WASTEPACK ok` chat_completion + dispatch_tool wrapped death_ledger=1 repeat_guard=1 lookahead=1
  - `#OURS_DOSSIER ok` mounted, prompt_tail installed, errors=0, games=25 (dossier-v1)
  - `#OURS_XPACK ok` mounted (dossier-v2: categories/SFT/RL-seeds; `tools:false` noted — tool registration fail-open, attribution caveat for verdict council)
  - `#OURS_FORM ok version=d_prime` (champion form: priority_value replaced, tail fade 0.4, level_pow=0.5, pace model live)
  - `[Y21:AUDIT] qwen3.5-27b-fp8 weights (primary): dataset eliork/qwen3-5-27b-fp8` — FP8 primary served
  - `submission.parquet` present in kernel output (pre-scoring placeholder — normal; real run executes during scoring with TRUE_SUBMISSION=True)

## Session context
- Sandbox reset wiped local repo mid-session → recovered from GitHub origin (`743d62d`) using `x-access-token` URL-embedded auth
- Fire toolchain rebuilt from scratch this session (`scripts/fire_sdk.py` — official kagglesdk client, Bearer auth via KAGGLE_API_TOKEN; endpoint = POST /api/v1/competitions/submissions/submit-notebook/{comp})
- KGAT tokens authenticate as **Bearer** (not Basic) — all prior 401s explained

## Verdict rules (docs/45-46)
- Score > 33.50 → new board best (LB takes max) → Stage A (≥34) progress; rank map: 34→76, 35→54, 36→43, 37→30, 38.2→20 (gold cutoff, drifting to ~39-40 by Nov-02)
- 0.00 → forensics before any re-fire (F-1030 lesson: no unadapted config transplants)
- Evening verdict council → docs/47; apex-v2 build (stall-knee 80-action fold + act_checked port + v2-layer tool registration fix) targets Oct-27 slot

## Fallback ladder (unused)
1. ~~apex-v11~~ ← FIRED
2. apex-v1 (complete, all receipts green from prior session)
3. wastepack-v1 pure
4. champion dprime redraw v3
5. clean-v1 redraw (33.50 config, A-lane kragglenote2forwork token)

## ⚠️ VERDICT (10:0xZ): apex-v11 scored 0.00 — F-1031 forensics
- ref 57659975: complete, publicScore **0.00**, totalBytes **3411** — the guard's placeholder
  parquet, byte-count IDENTICAL to the Oct-25 agi35 0.00 (also 3411).
- Meaning: the scoring rerun took the RUN_FULL=False path → gateway probe failed inside BOTH
  scoring reruns (Oct-25 + Oct-26). Run completed in ~60 min ≈ setup (~14 min) + 45-min gateway
  poll cap → placeholder → clean exit.
- Guard cell byte-identical between Oct-24 GOOD run (26.47) and the 0.00 runs → **platform-side
  gateway boot/DNS change after Oct-24** (same family as F-1024: rerun env died Oct-21/22).
- F-1030 revision: agi35's "verbatim foreign config transplant" attribution was incomplete — the
  identical placeholder points to the SAME gateway/patience failure. Config swap likely harmless.
- Corollary: validation runs (RUN_FULL=False, 14 min) NEVER exercise serving + agent loop —
  setup receipts cannot catch this failure class.

## Countermeasure shipped: guard-v2 (in apex-v12 v2)
- `_GATEWAY_MAX_WAIT_S` 2700 → **7200** (120 min)
- `_GATEWAY_DNS_DEAD_S` 600 → **3600 if big GPU** else 600 (T4 commit runs keep the fast escape)
- smoke fast-path preserved (`ARC3_FORCE_SMOKE=1` skips the poll entirely)
- `/kaggle/working/guard_decision.json` written with the full decision (visible in our runs)
- 19/19 gates + 13/13 real-module tests; pushed as **v12 version 2** (queued on GPU, docker pinned)
