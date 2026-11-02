# Cross agent notes

One note per run, same content in both repos: `agents/cross/<date>.md`. Catalogue in `CAMPAIGN_OS.md` §5.

## 2026-10-10 — seed

- **Categorization**: ARC-2 has an R6 semantic-family taxonomy for the 120 eval tasks (HF `Nabidnur/arc-agi-2-solution-methods`) and hidden tasks are train-sized; ARC-3 has 55 public games in classes with level-index weighting. Both plans allocate budget by category (ARC-2 v31 retry pass / caps; ARC-3 PACE / TAIL_FADE).
- **Anchored greedy selection**: ARC-2's exact-verified families (precision 1.0) are anchors for candidate selection (S6); ARC-3's D′ priority is a greedy allocation over slots. The ARC-3 twin of S6 is "verified level-advancing action rules first, free exploration second".
- **Redraw under max()**: both competitions keep nondeterministic scored reruns and deterministic validation; daily redraws are the variance engine; new versions must beat the family μ, not a single draw.
- **Fail-closed gates**: ARC-2 `gate_v30_output.py` ↔ ARC-3 preflight + smoke + throughput gates. Lesson of 2026-10-10 (A's crashed output submitted): no gate, no submission, in either competition.
- **Measured-not-claimed**: public-notebook sweeps in both competitions found no technique that beats the base family outside rerun noise; author LB claims are never adopted (ARC-2 perfpatch 6–10 % not 2×; ARC-3 14-stream / spec-4 / NVFP4 all negative when measured).
