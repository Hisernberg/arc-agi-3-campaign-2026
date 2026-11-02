# 02 · Scoring Methodology (RHAE) & Strategic Implications

Official name: **Relative Human Action Efficiency** (docs.arcprize.org/methodology).

## Formula

```
per-level score  = min( human_baseline_actions / agent_actions , 1.15 )  ... if level completed
                 = 0                                                     ... if not completed
per-game  score  = Σ(level_score_L × L) / Σ(L)        for L = 1..N (level-index weighted)
completion cap   = Σ(L of completed levels) / Σ(1..N) (can't exceed by efficiency alone)
total score      = mean(per-game score over all games) → 0–100%
```

- **Human baseline** = upper-median first-time human player per level (not speedrunners).
- **Cap 1.15×**: being 2× more efficient than human does not pay beyond 1.15/level.
- **Squaring**: `min(h/a, 1.15)` is *squared* (docs example: raw 0.5 → 0.25). Being 2× slower
  than human on a level = 0.25; 4× slower = 0.0625; 10× slower = 0.01.
- **Level weighting**: later levels weigh more (level index = weight). Completing level 5
  is worth 5× level 1 within a game.
- **All environment actions count** (exploration, failed probes, RESET). Tool calls,
  LLM reasoning tokens, retries *outside* the environment do not count.

## Implications (ranked by leverage)

1. **Completion dominates.** A level not finished = 0 regardless of how close you were.
   The single biggest score lever is converting "stuck on level 1–2" games into
   "reached level 3–4" games. Score improvement 0→a few levels >> efficiency polish on
   an already-solved game.
2. **Early-level efficiency matters as much as late-level completion.** Because squaring
   punishes waste quadratically: finishing L1–L3 with 2× human actions yields
   (0.5²)·(1+2+3)/ΣW contribution, roughly halving game score. Duck's "batch verified
   action sequences" directly targets this.
3. **The 1.15 cap** means: once you're at human-level efficiency, further optimization of
   that level is worthless. Redirect budget to unfinished levels/games. The practical
   target is ~human-parity per level, not superhuman.
4. **Level weighting + completion cap interact:** completing the FINAL level of a game is
   disproportionately valuable (unlocks the remaining weight mass). A game stuck at L4/6
   is capped at 10/21 ≈ 47.6% even with perfect efficiency.
5. **RESET costs an action.** Re-randomizing a stuck level can be correct (human baselines
   imply ~20–500 actions/level), but RESET spam destroys efficiency. Prefer RESET when
   current-level state is provably unrecoverable (e.g., dead-end puzzle states).
6. **Budget allocation per game (9 h, 110 games, 28-way concurrency):** naive equal split
   (≈ 4.9 min/game) is wrong. Allocate by marginal expected score: games stuck at L1 with
   negative learning signal get less; games advancing get more. Duck's analyzer timeout
   (900–1200 s) implements this coarsely; smarter triage is a roadmap item.

## Worked example (why we score 3.45, leader 18.81)

Suppose agent completes L1–L2 with exactly human actions on 7 games, nothing elsewhere:
game score = (1²·1 + 1²·2)/Σ(1..N≈6..10 weights) ≈ 0.20–0.43/game → total ≈ 3.4–4.3.
Leader 18.81 ≈ finishing ~L3–L4 with ~1–1.5× human actions on most games.
**Each completed level ≈ +1.5–3 total points. That is the granularity of our roadmap.**

> **Correction 2026-10-09 (analysis/sim):** the harness's own scorecard, reproduced to 1e-14 on skarin's 100 records, applies the cap *after* squaring — per level `min((human/agent)², 1.15)` — and caps the game score at the completion fraction Σ(cleared L)/Σ(1..N). The formula above squares the capped ratio; the rankings it produces are identical, the absolute values differ (e.g. 33.3 vs 41.3 on the same simulated run).
