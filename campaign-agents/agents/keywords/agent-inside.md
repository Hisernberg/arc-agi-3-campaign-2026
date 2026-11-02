# keyword: agent inside — analyze OUR results

1. Collect: new scores (`status`), any local run outputs (`submissions/outputs/*/benchmark.json`), rerun logs if the author account can download them.
2. Per game: `python scripts/kw/kw_pergame.py <label>=<benchmark.json> ...` — levels, score, actions, agent/base efficiency per level, zeros.
3. Greps on every available log (local or rerun): `UNDO executed`, guard fire counts (`noop`, `death`, `repeat`), `RESET` count per game, priority/handover lines (`priority`, `TAIL_FADE`, `handover`), server restarts, `OOM`, `Traceback`, wall-clock used vs 32,400 s, games never started.
4. Attribution: for each game, classify the failure: never-started (allocation), stuck L1 (perception/goal), death loop (guards), efficiency bleed (actions ≫ baseline on cleared levels), run-level infra.
5. Compare against the public-25 reference (skarin audit: `analysis/public25_reference_m2s.md`) to separate "our config" from "the base".
6. Write `reports/kw/inside_<date>.md`: table of games × failure class, 3 concrete hypotheses, each with the trace signal that would falsify it. Feed hypotheses into `plan`.
