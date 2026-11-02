# `build` — runbook

Turn one REGISTER ticket into a version through the funnel (`CAMPAIGN_OS.md` §3). Input: ticket id (e.g. `E-140`, `v31`).

1. Read the ticket (hypothesis, mechanism, predicted band, kill criterion) and the current base text (ARC-2: the latest gated notebook; ARC-3: `track-b/<date>/kernel/`).
2. Write the change as anchored, reproducible edits (a `build_vN.py` with `replace_once`, or a documented cell diff). One unmeasured model-visible change per version.
3. Stage 1 CPU: nbformat, AST per cell, use-before-import per `%%writefile` module, cross-cell names, mount audit; offline paired eval where the layer allows (ARC-2: saved candidate pools / train-1000; ARC-3: D′ simulator, per-game sim).
4. Stage 2 small GPU with fail-closed gates (ARC-3: ≤ 40-min smoke + preflight + smoke gate + throughput probe; ARC-2: 1-h commit + `scripts/gate_v30_output.py`).
5. Record receipts in `experiments/REGISTER.md` (stage, gate results, verdict) and `BUILD.md` next to the kernel; set eligibility in `analysis/next_submission.json` only when every gate is green.
