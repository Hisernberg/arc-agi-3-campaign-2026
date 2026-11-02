# docs/27 — DECODED: the 6.0 "taaf-flashnext-sheetu12b-0922" (AGENTFIX build) — full teardown

2026-09-30 · Artifact: uploaded executed notebook `taaf-flashnext-sheetu12b-0922 (2).ipynb` → saved as `notebook-intel/taaf-flashnext-sheetu12b-0922-v2-score6.ipynb` (+ cells extracted to `notebook-intel/v2_cell_*.py`). This file is an **executed run** (papermill 2026-09-22 15:42→17:52 UTC, 7823 s, RTX Pro 6000) — outputs included, i.e. we hold its ground-truth run report.

## 1. What this notebook is

Same TAAF/keithtyser base as the 5.19 Gold notebook — **serving is byte-identical** (`kv5-bf16-mtp3-c16-cg32-ctx16k`: 5 GiB KV, 16 seqs, MTP3, cudagraph 32, ctx 16384 via `LOCAL_ANALYZER_CONTEXT_WINDOW`, no prefix cache; 28-way games; 7920 s/game; 9 h notebook budget; analyzer timeout 900 s). The entire delta is ONE new cell: **`AGENTFIX` (138,149 chars, cell 10)** — six-plus measured agent-loop repairs applied as runtime patches to the shipped bundle, each independently env-switchable, plus **ARM P** (board-image upscale) and **F19** (contact sheet). Duck prompts/policy untouched ("c16's schedule with a repaired agent").

**The 6.0 is a draw of this exact config.** The owner never re-ran the notebook after 9/22 — recent higher scores are Kaggle-side rerun draws (variance farming again, σ≈1.5, docs/23 §2.5).

## 2. Shipped config — ground truth from the run's own `AGENTFIX LIVE` output

| Fix | State | What it does |
|---|---|---|
| **F1 images** | **ON** | history keeps text only (current prompt keeps its image); flat per-image token cost (120 tok) instead of `len(b64)//3`; reply safety margin 6144 tok |
| **F3 memory** | **ON** | tolerant labeled-block parser (exact-prefix matching silently dropped "World model (revised):" / "Plan (next):"); **game_over no longer wipes the world model** — it's a level RETRY, not a new level |
| **F13 anim frames** | **ON** | arcengine returns a LIST of frames per action; stock harness reads only the last. Patch persists up to 6 intermediates (keep 3 entries) as ASCII in runtime state; model reads them in the sandbox via `last_transition.frames` |
| **F19 contact sheet** | **ON** | when an action animated, ONE extra image rides with the newest user message: contact sheet of [intermediates … final board], ≤8 panels, integer NEAREST upscale 4, ≤1.0 MP, frame-index labels, coordinates-only text ("act in ORIGINAL board coordinates") |
| **F9 timing** | **ON** | per-step chat/tool token+time telemetry (observability only) |
| **ARM P** | **ON** | board image upscale **4 → 12**: the 64×64 board renders 768×768 px instead of 256×256 (3× linear, 9× area vision fidelity), verified end-to-end through the exact render call path |
| F2 result / F4 loop / F5 no-impact / F6 action7 / F7 ledger / F10 stall / F11 dedup / F13b summary | off (flags present) | measured defect fixes held back — see §4 |

## 3. Its own validation run (ground truth, 7200 s cap, 21/25 games finished)

Per-game score = triangular level-fraction ×100. **Total 228.74 → mean 9.15 over 25 games · 39 levels · 2,167 actions.**

| Game | Level | Score | Actions | | Game | Level | Score | Actions |
|---|---|---|---|---|---|---|---|---|
| ft09 | 4/6 | 47.62 | 65 | | sp80 | 1/6 | 4.76 | 44 |
| lp85 | 5/8 | 41.02 | 124 | | cn04 | 1/6 | 4.76 | 47 |
| ar25 | 4/8 | 27.78 | 141 | | ls20 | 1/7 | 3.57 | 90 |
| sc25 | 3/6 | 19.43 | 135 | | tn36 | 1/7 | 2.82 | 41 |
| vc33 | 3/7 | 19.42 | 114 | | dc22 | 1/6 | 2.41 | 112 |
| re86 | 3/8 | 15.79 | 145 | | su15 | 1/9 | 2.22 | 58 |
| ka59 | 2/7 | 10.71 | 154 | | wa30 | 1/9 | 2.22 | **370** |
| tu93 | 3/9 | 8.86 | 111 | | lf52 | 1/10 | 1.82 | 92 |
| sb26 | 2/8 | 8.33 | 67 | | bp35 | 1/9 | 0.44 | 73 |
| tr87 | 1/6 | 4.76 | 33 | | **sk48** | **0/8** | 0.00 | 80 |
| | | | | | **cd82** | **0/6** | 0.00 | 71 |

Reading: mean internal 9.15 with efficiency-multiplier ≈ 0.57–0.66 → the observed LB band 5.19→6.0. **The genome's raw ceiling is ~9; every point of efficiency recovery converts 1:1 toward that ceiling** — exactly the lane our playbooks own.

## 4. The measured evidence embedded in their comments (paper-grade A/Bs we inherit)

1. **F13 is the only fix that ever moved the hidden LB: 3.20 → 3.71 (+0.51).** A harness-authored per-turn TEXT summary of the same frames **failed (2.57)**: *"Frames yes, narration no."* The model must PULL frames via python; pushing narration doesn't transfer.
2. **F1**: median **8 obsolete boards per request ≈ 26% of the token budget**; stock estimator charged images ~442 tok vs 70–100 real (5–8× overcharge) → real reasoning/tool results got evicted. After F1 the real prompt reaches ~1.0× budget (review 4: r11l 32,036/31,744) — hence margin 6144 (4096 rejected: 6.4% of replies wouldn't fit).
3. **F2 rationale**: **81% of acting calls returned NO structured result** (model printed to stdout instead) — the harness's own `_describe_last_outcome` was dead code.
4. **F4 rationale**: sk48 burned **46 min / 35 calls / 0 actions** on three identical snippets (and indeed sk48 = 0/8 again in this run).
5. **F5 rationale**: the HUD band (action-budget bar) flips **1–2 cells on EVERY action in 25/25 public games** — pollutes `board_changed` signals.
6. **F19 rationale**: a sibling harness ships every frame as one labelled sheet image and never narrates; ported verbatim from `all_twenty_five_continuity_retry_candidate_20260916`.
7. **Refusal lesson**: v3's bounded refusal of known no-ops "misled the model" — they now execute again but tag `repeat_of_known_no_op=n`.

## 5. What changes in OUR build (docs/24 v9 layer addenda, all Track S, all portable)

| Priority | Port | Effort | Expected |
|---|---|---|---|
| P0 (10/2, with L2) | **F1** history-image strip + flat image cost + margin 6144 | small (same hook we patch) | protects 26% of budget; unblocks 16K ctx without eviction |
| P0 (10/2) | **F3** tolerant parser + no-wipe-on-game-over | trivial | world model survives retries |
| P0 (10/2) | **ARM P upscale 12** | one env + accessor pin | 9× board pixels for the vision model |
| P1 (10/3, with L3) | **F13** intermediate frames into sandbox (`last_transition.frames`) | medium — we own arcengine locally, frame lists already exist in our replays | their +0.51 hidden-LB component |
| P1 (10/4) | **F19** contact sheet (≤8 panels, scale 4, 1 MP, coordinates-only line) | medium (PIL composition) | visual continuity without narration |
| P2 flags | F2 always-return result, F4 identical-snippet guard + act-now notice, F5 HUD-masked change counting + no-op tagging, F7 ledger | medium | their OFF set = our L3/L4 design (region tracking, ledger) — converge and adopt both |
| Probe | `ONLY_RESET_LEVELS=true` — RESET keeps the level in the arc_agi client | tiny | if true on the hidden rerun, cheap retries change playbook design |

Never port: F11 dedup (they default it off; Affectify's dedup is different — ours stays kill-switched), F13b narration (measured harmful), refusal-of-no-ops (measured harmful).

## 6. Strategic reading for the week

- Their fix set and our docs/24 v9 are **complementary, not overlapping**: they repair perception/memory/token-economy of a cold-start agent; we add memory-as-code (53 playbooks), value-corrected allocation, and efficiency discipline. Their zero-point games (sk48, cd82) and 370-action wa30 are exactly what our playbook lane + stall knee eliminate.
- Ceiling arithmetic now evidence-backed: their genome (no playbooks, cold L1) means 9.15 internal → LB ~6.0 on a good draw. Our v9 = their fixes + 25 free L1s + sb26→L8 chain + value tickets → internal 11–14 plausible → **LB 7–9 realistic, 10+ on a good draw** — consistent with docs/25 §4 and it strengthens the top-10 case.
- σ≈1.5 draw variance reconfirmed at the top of the public table — the 3–4 nightly Track-S re-draws (docs/26 §3) are justified by the leader's own behavior.
- Attribution: credit Scott Le Grand (TAAF serving + agentfix), keithtyser (bundle), Tufa Labs (Duck) in the notebook header; our deltas documented in REGISTER.

**Register:** logged as **E-111** (analysis artifact; ports tracked under E-103/E-106 gates).
