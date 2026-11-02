# 01 · Competition Overview

## Facts (verified 2026-09-19)

| Item | Value |
|---|---|
| Competition | ARC Prize 2026 - ARC-AGI-3 (Kaggle) |
| Total prizes | $850,000 ($150K progress + $700K grand bonus for 100%) |
| Entrants / Teams / Subs | 14,592 / 3,138 / 35,701 |
| Evaluation | 110 hidden interactive games (55 public LB, 55 private LB) |
| Submission | Kaggle Notebook, internet OFF, ≤ 9 h runtime, CPU or RTX 6000 (g4-standard-48) |
| Milestones | M1 Jun 30 (done: Tufa/Reki/forge) · M2 **Sep 30** ($25K/$7.5K/$5K) |
| Entry deadline | Oct 26, 2026 (must accept rules) + team merger deadline |
| Final submission | Nov 2, 2026 · Winners Dec 4, 2026 |
| Prize condition | Winners must open-source their solutions |

## ARC-AGI-3 environment

- Turn-based, hidden, interactive environments ("games"). Frames = JSON with a grid
  (max 64×64), cell values 0–15, origin (0,0) top-left.
- Actions: `RESET`, `ACTION1–5` (simple), `ACTION6` (needs x,y), `ACTION7` (extra; in
  practice = UNDO in many games). Available actions per game revealed via metadata.
- 3 states: `NOT_FINISHED`, `WIN`, `GAME_OVER` (only RESET valid in GAME_OVER).
- Multi-level per game; levels get harder; RESET keeps the current level in competition mode
  (`full_reset=false` for level resets).
- Competition evaluation uses a live gateway at `http://gateway:8001/` during rerun;
  interactive dev uses bundled offline environment files.

## Progress prize structure

**Final leaderboard $75K:** 40/15/10/5/5 K. **Milestones $75K:** M1 (Jun 30) 25/7.5/5 K —
won by Tufa Labs, Reki, forge. **M2 (Sep 30):** 25/7.5/5 K — *live in 11 days*.
**Grand bonus $700K** only if a team hits 100% (split 350/175/70/70/35 K).

## What matters strategically

1. **Milestone 2 (Sep 30) is the nearest prize window.** Top-3 on M2 date earns $25K/$7.5K/$5K.
   Currently #1 is 18.81 — reaching top-3 in 11 days is a stretch; M2 notebook must be public
   open-source by Sep 30.
2. **Final leaderboard (Nov 2) is the main target.** ~6.5 weeks of iteration remain.
3. Score is mean-over-games → **mid-tier consistency beats solving 2 hard games**.
   Every game that completes levels 1–3 cheaply adds real points.
4. Since scoring averages all 110 games, **avoiding catastrophic time waste** on one game
   (brute force) is as important as solving another.

## Hidden vs public games

25 public games (this repo has all of them) are for development only. The 110 hidden games
are same-distribution but different. Local public scores correlate imperfectly
(M1 bronze medalist warned "local public-game scores are an unreliable leaderboard proxy") —
use them for relative A/B comparisons (same seed, same games), not absolute predictions.
