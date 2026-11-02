# ARC26 v63 FINALDAY (Nov-2, 2026) — post-lock validation vehicle

Competition scoring is sealed (finals selection locked 05:45 UTC Nov-2; leaderboard
closed Nov-1 23:45 UTC). v63 is the all-ideas validation build, run for R&D only —
it contains NO submission path.

- `arc26-nvarc-v63-finalday.ipynb` — GPU FULL (5.5h box): v44 mixture-of-solvers
  chassis + the decoded 34.86 leader's student mount `sorokin/qwen3_4b_grids15_sft139`
  wired as the v38 ladder PRIMARY (27B FP8 stays as fallback; qwen3 parsers kept).
  Staged for the Nov-7 00:00 UTC weekly GPU-quota refresh.
- `arc26-nvarc-v63-finalday-solo.ipynb` — GPU SOLO (1.45h rerun box + 30min commit):
  pushed to dasshovon 11:29 UTC Nov-2 and RUN within the 1.98h receipted quota.
- `arc26-nvarc-v63-finalday-cpu.ipynb` — CPU RUN (free pool): pushed to the
  kragglenote2forwork lane 11:29 UTC Nov-2; GPU legs fail-open, base artifact lands.
- `v63_coords_*.json` — push receipts (slug + version + UTC timestamp).
- `finals_selection_receipt.json` — the sealed finals decision (56842535 @ 32.64 +
  56901303 @ 31.81, operator-ratified; strict top-2 by score).
- `scripts/build_v63_finalday.py` — the builder (37-cell v44 surgery, byte-identity
  + AST checks + forbidden-token sweep).

Simplified student channel note: the leader's full sandbox-verified code-induction
harness (150KB dependency web) is receipted as the post-competition upgrade path;
v63 routes the student through the PROVEN leg stack as ladder primary instead.
