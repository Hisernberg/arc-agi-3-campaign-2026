# 16 — Best-possible-scoring plan (2026-09-27 refresh)

Campaign doc · 2026-09-27 · supersedes doc 13 §5 sequencing · **no submission made by
the agent** (user submits manually; latest manual submission: taaf-flashnext 09-27
07:01 UTC, pending).

---

## 1. LB reality refresh (pulled 2026-09-27 07:3x UTC)

| Rank | Team | Score | Δ vs 9/25 |
|---|---|---|---|
| 1 | Tufa Labs | **27.29** | +8.48 in 2 days |
| 2 | Lord Han Solo | 20.80 | +1.4 |
| 3 | Tong Hui Kang | 20.53 | +9.75 (new entrant) |
| 4 | Yi-Chia Chen | 18.80 | +2.8 |
| 5 | Daniel Franzen | 16.68 | +3.6 |
| 6 | NVARC3 | 16.07 | — |
| 10 | rellik13 | 9.96 | — |
| 16 | Skyfall AI | 7.67 | — |
| … | **us (3.85 best)** | rank ~210+ | — |

Reads: (1) the top is **accelerating** — the 17–18 band that was rank-1 on 9/25 is now
rank 4–5; "9–10 = top ~1.3%" still holds (rank 10 = 9.96, rank 16 = 7.67 — the 9–10
band still lands top-10-ish); (2) scores ≥11 now exist in numbers — the T3→T4 techniques
(docs/13 §3 ladder) are **proven at scale**, not exotic; (3) our position: 3.85 with the
world-model machinery proven DEAD in every prod run — the honest-stack test is the
single highest-EV action available.

## 2. Score math (unchanged formula, re-anchored)

Per-level `min(human/agent, 1.15)²`, game = weighted avg, total = mean over hidden
games × 100. To reach **9–10**: complete L2 on ~all games (Scenario A → ~9.2) or L3 on
~60 games (Scenario B → ~10) at near-human efficiency. From 36/183 public levels today
→ ~10× completed-level mass. The tier ladder says the jumps come from: state discipline
(T2), search/simulation + world-model (T3), exact offline solving (T4/T5).

## 3. The wave plan (GPU-budget compliant: 1 run/day, 3–4 runs/week)

### Wave 1 (NOW): v8 APEX — the honest full stack
- **Built + validated** (docs/15): 61/61 unit, 138-step real-game smoke all green,
  byte-diff only cell 14. Includes v7.1 state fix (machinery alive for the first time),
  raw-grid frame delta, obj-diff tracking, tokenizer-level meter + soft cap, macro
  replay hints, nostep governor, contradiction guard, cross-level transfer.
- **User submits manually** (1 submission; if the daily cap allows, 2× for variance —
  same-code variance is ±0.7).
- Decision tree: ≥4.5 → Wave 2 as-is · 3.5–4.5 → Wave 2 + widen frame_delta cap ·
  <3.5 → mechanism ablation run (config-only: switches off in pairs).
- **Token telemetry** from `nooa_log/*.jsonl` (`tok_result`, per-step) feeds the
  WM_TOKCAP tuning before Wave 2.

### Wave 2 (early Oct): v9 = v8 + measured upgrades, no new risk
- `search_log()` sandbox channel (PRO-LONG-lite) if JSONL shows note-loss events.
- `LOCAL_ANALYZER_TOOL_STEPS` 12→8 (P1-2) if telemetry shows stuck-turn prefill waste.
- Archetype playbooks for unseen games (P1-3, 2-probe classifier).
- Level-start observed-budget line (P1-4).
- Hidden-games probe result folded in (the `.py`-sources question decides Wave 3+).

### Wave 3 (mid Oct): the T4/T5 lever — exact offline solving
- If rerun containers ship game `.py` sources: harness-side solver thread
  (dijkstra/beam/BFS over `deepcopy`'d game) → verified plans → replayed via the
  **macro channel already built in v8** (the plumbing is deliberately forward-compatible).
- If not: Kyutai-style distillation (TD-JEPA + BFS on public 25) is the fallback —
  cost: model training outside the kernel; risk: medium; evidence: 7.37 with zero LLM.

### Milestone-2 (deadline 9/30, requires open-source): go/no-go on 9/28
- Recommendation: **NO-GO for full open-source of the v-series**; the competitive
  value is the harness patches, and Milestone-2's prize pool does not beat a top-20
  main-track finish. If the user wants it anyway, open-source the v4 lineage (already
  superseded by v8) — zero downside.

## 4. Trace analysis of the public-best run results (pending upload)

`results (4).zip` had **not landed** on the server at analysis time (checked
repeatedly 07:00–08:3x UTC 9/27; this is the second silently-failed upload after the
notebook ipynb on 9/26 — please re-upload or share via the Drive folder). The ingestion
pipeline is armed and takes one command:

```
python3 scripts/ingest_results_zip.py "<zip>" --out research/zip-ingest-results-4
```

It auto-detects schemas and produces: per-game score/level/action table, key-vs-mouse
mix, batch-size stats, token/turn telemetry, failure forensics (game_overs, dead
levels, no-progress streaks), and note/feature adoption counts. Findings will fold into
docs/15 §5 (expected effects) and the Wave-2 build list.

What we will look for, ranked by decision value:
1. **Wasted-action mass** (5.1% measured in our v3 traces vs theirs) → nostep/budget tuning.
2. **Action mix per game archetype** (mouse share on click-only games) → P1-3 playbooks.
3. **Turn/token cadence** (inner tool-steps per turn; result sizes) → P1-2 budget + WM_TOKCAP.
4. **Level-transition behavior** (what they inject on new levels) → transfer hardening.
5. **Failure forensics** (game_over loops, dead-level abandonment) → governor thresholds.

## 5. The standing anti-list (unchanged, evidence-locked)

Auto-repair loops (Tycho −5.4) · forced flexible-executable world models (ablation paper:
textual won twice at 8B) · heavy hand-built perception beyond segmentation (Tufa ablation)
· vision context for the 8B under KV ≈3.21×32K · prefix caching on 28-way interleave ·
autopilot action-firing by the harness.
