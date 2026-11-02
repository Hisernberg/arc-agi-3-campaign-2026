# 05 · Public Games Analysis (25 games)

Generated from `environment_files/*/metadata.json` (+ local engine probes). Raw table
produced by `scripts/analyze_games.py`; re-run to refresh.

## Roster with human baselines (per level)

| Game | FPS | LV | Σ human | Human/level (baseline actions) |
|---|---|---|---|---|
| AR25 | 6 | 8 | 748 | 32 50 75 37 89 159 233 73 |
| BP35 | 20 | 9 | 651 | 21 48 44 38 33 87 86 131 163 |
| CD82 | 30 | 6 | 171 | 55 8 41 21 23 23 |
| CN04 | 5 | 6 | 789 | 29 54 85 300 208 113 |
| DC22 | 15 | 6 | 1228 | 59 102 67 98 324 578 |
| FT09 | 8 | 6 | 208 | 43 12 23 28 65 37 |
| G50T | 30 | 7 | 879 | 78 175 179 230 96 54 67 |
| KA59 | 10 | 7 | 730 | 28 109 51 51 33 132 326 |
| LF52 | 30 | 10 | 1339 | 32 81 60 71 205 148 244 109 164 225 |
| LP85 | 20 | 8 | 388 | 17 38 31 16 41 60 26 159 |
| LS20 | 30 | 7 | 776 | 22 123 73 84 96 192 186 |
| M0R0 | 7 | 6 | 1107 | 30 111 203 26 500 237 |
| R11L | 30 | 6 | 233 | 22 33 51 26 52 49 |
| RE86 | 25 | 8 | 1255 | 26 42 86 108 189 139 424 241 |
| S5I5 | 15 | 8 | 638 | 20 89 106 54 162 38 86 83 |
| SB26 | 30 | 8 | 213 | 18 28 18 19 31 23 58 18 |
| SC25 | 20 | 6 | 350 | 36 6 32 83 143 50 |
| SK48 | 30 | 8 | 1070 | 61 177 101 103 230 181 125 92 |
| SP80 | 10 | 6 | 518 | 39 58 25 148 96 152 |
| SU15 | 20 | 9 | 361 | 22 42 26 115 36 31 8 40 41 |
| TN36 | 3 | 7 | 317 | 32 72 26 40 30 55 62 |
| TR87 | 10 | 6 | 414 | 54 58 40 45 71 146 |
| TU93 | 30 | 9 | 462 | 19 16 34 42 123 80 14 23 111 |
| VC33 | 20 | 7 | 447 | 7 18 44 61 131 34 152 |
| WA30 | 5 | 9 | 1843 | 71 119 183 98 368 68 79 442 415 |

## Observations

1. **Cheapest games** (low Σ human): CD82 (171), SB26 (213), R11L (233), FT09 (208),
   TN36 (317) — these are "efficiency polish" targets; every level can plausibly be
   solved near human count, pushing their game score toward the 0.8–1.0 band.
2. **Most expensive** : WA30 (1843), DC22 (1228), RE86 (1255), LF52 (1339), SK48 (1070),
   M0R0 (1107) — long-horizon games; heavy L4–L6 baselines (DC22 L6=578, M0R0 L5=500,
   WA30 L9=442). These reward deep understanding; likely where completion (not efficiency)
   separates teams.
3. **Tight early levels** (L1 human ≤ 25): VC33 (7!), SC25 (36 L2=6), TU93 (19), SB26 (18),
   LP85 (17), SU15 (22), R11L (22), LS20 (22), S5I5 (20), BP35 (21), TU93 (19).
   **L1 efficiency on these games is nearly free score** if the agent acts decisively
   (≤2× human keeps ≥0.25 of the L1 weight; ≤1.15× human hits the cap).
4. **Action-tag mix:** 14 keyboard+click, 4 keyboard-only, 5 click-only, 2 untagged
   (FT09, per API) → agents must be competent at ACTION6 coordinate selection AND
   keyboard sequencing. Click games with small human counts (VC33 L1=7) imply precise
   click targets exist — object-prior heuristics (Reki-style) could pay off.
5. **fps ranges 3–30** — low-fps games (TN36=3, CN04=5, WA30=5, AR25=6, M0R0=7) have
   slower local sim; account for that in local testing throughput planning.

## Level-1 human baseline sorted (efficiency priority list)

VC33 7 · LP85 17 · SB26 18 · TU93 19 · S5I5 20 · BP35 21 · LS20 22 · R11L 22 · SU15 22 ·
CN04 29 · AR25 32 · LF52 32 · SC25 36 · SP80 39 · CD82 55 · TR87 54 · FT09 43 · DC22 59 ·
SK48 61 · G50T 78 · KA59 28 · TN36 32 · WA30 71 · RE86 26 · M0R0 30

## TODO (game knowledge base)

- [ ] Per-game screenshot atlas from local engine (L1 board for each game → analysis/)
- [ ] Trace replay analysis: run Duck locally on public-25, record transitions, identify
      per-game failure signature (no progress / loops / HUD confusion / stuck at LN)
- [ ] Per-game notes file (mechanics hypothesis once known) → analysis/games/<game>.md
