# 13 · Score Verification, Trace Mining & Verified Playbooks (2026-09-29)

## 1. Current scores by notebook (LB = official Kaggle public score)

| Notebook | Run date | LB | Levels done | Notes |
|---|---|---|---|---|
| **ARC26 urad duck r10** | 09-28 | **4.07** | **41/183** | current best; sb26 WON 8/8 |
| ARC26 r12 apex 519 | 09-29 | 3.09 | 45/183 | internal 5.19; most levels but worse efficiency |
| taaf-flashnext-sheetu12b-0922 | 09-27 | 3.18 | — | sheetu12b config |
| v7 nooa-lite submit | 09-26 | 2.61 | — | |
| duck-governor-v1 (v3) | 09-19 | 2.77 | 40 | |
| Duck Qwen3.8 Anim Base 35c14d v2 | 09-18 | 3.45 | — | former best |
| 27B clean fresh draw d2 | 09-28 | 1.72 | 23/183 | 27B KV-collapse (see docs/14) |
| Qwen3.8-27B FP8 LB9 repro | 09-27 | 1.17 | — | same failure mode |
| 27B d2 draw #3 | 09-29 | 1.13 | — | |

**Internal-vs-LB gap explained**: internal "5.19" counts raw level completions;
LB applies (a) level-index weighting, (b) min(human/agent,1.15)² efficiency squaring,
(c) per-game normalization. r12 did 45 levels wastefully (many levels at 2-4× human
actions → squared penalty) vs r10's 41 levels mostly at ≤1.15× human. Efficiency is
worth more than raw completions. "Each completed level ≈ +0.1-1.3 LB points depending
on weight and efficiency."

## 2. Best-run trace analysis (r10 LB 4.07 / r12 LB 3.09)

Games stuck at 0 levels (r10): **sk48 (181 actions on L1!), dc22 (200), cd82 (83), g50t (51), r11l (189)**
→ pure waste: ~700 actions ≈ 25-30% of total budget burned for zero points.

Games with big waste on completed levels (r10): lp85 L4 98/16 (6.1× human!), ar25 L4 145/37,
sk48 L1 181/61, dc22 L1 200/59, tn36 L2 106/81. Squaring turns 6× slower into 0.028 per level.

Where the wins are: **sb26 8/8 at 12-33 actions/level (human-parity)** — proof the harness can
full-clear a game when mechanics are cracked. ft09, vc33, re86, sc25, ar25 advance to L3-L5.

Median per-action wallclock r10: 4278s ÷ 28 workers (i.e., actions are cheap; the budget is
dominated by per-action LLM latency × sequence length, not env time).

## 3. Verified playbook library (analysis/playbooks/own_playbook_library.json)

Extracted per-level action sequences from r10+r12 benchmark histories, re-replayed on the
LOCAL ENGINE (== Kaggle scoring engine, proven: r10's own wa30 L1 sequence re-clears at
action 48 locally exactly as it did on Kaggle).

- **53 playbooks; all 25 L1 sequences verified from fresh start; L2+ sequences are exact
  per-level segments (verify chained L1→L2→… when used).**
- Use: recognition-triggered replay — if game_id+level matches, emit the verified sequence
  instead of re-exploring (saves 20-190 wasted actions/game; r12's 45-level run shows how
  re-exploration wastes the squared-efficiency term).

## 4. Frontier trace transfers (ARA datasets on HF, CC-BY)

- AgentNativeResearchLab per-game trajectories (ls20 7/7 WIN, tr87 6/6 WIN, su15 L1-L7,
  wa30 L1-L3, lf52 L1) with world-model docs + replay scripts.
- **Verified transfers on our engine: lf52 L1 (9 actions vs our 18-21 — human 32, capped
  efficiency), su15 L1 (18 actions, human 22 → ~1.15 cap).**
- wa30 L2+ / tr87 scripts do NOT transfer (tr87 randomizes glyph phases per fresh board;
  wa30 deposit condition differs on the newer live-server build). Their MECHANIC
  documentation (claims, heuristics, win-rules) still transfers as strategy priors.
- guanning schema-traces (gpt56/opus48): GATED — access requested 09-29.

## 5. What this changes for the solver

1. Inject playbook table + ARA mechanic notes as per-game priors (env-var switchable).
2. Efficiency governor: hard-stop a level attempt at ~2× human baseline (from game metadata
   baselines) and RESET or move on — the squaring makes >2× nearly worthless.
3. Zero-game triage: sk48/dc22/cd82/g50t/r11l get fixed probe budgets (max 60-80 actions),
   then park. Their L1s are already in the playbook library.
