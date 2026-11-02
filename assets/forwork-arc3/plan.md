# ARC-AGI-3 research and submission plan

[Deep mechanism review](../reports/ARC3_MECHANISM_DEEP_REVIEW.md) adds historical activation tracing and fourteen CPU failure contracts. The next research queue is complete action/observation identity, helper invocation and no-tool recovery, game-local memory, then validated world-model search and matched mode comparisons. Interior-only hashes, mouse-name-only predictions, disabled features and prompt-only action caps cannot support a gain claim. These research primitives are not integrated into the frozen production notebook.

[Top-ten continuation plan](../reports/TOP10_TOMORROW_PLAN.md) adds the October 12 research results and October 13 priorities. Current cutoff targets: ARC2 48.75; ARC3 38.84.

**Today, 12 October: research and CPU preparation only. Tomorrow, 13 October: one account-B submission, conditional on the live gates. From 14 October: research recommendations; no further automatic submissions until the user says `continue`.** The root workflow owns the actual schedule and account verification. Existing repo documents with different automatic dates are historical instructions.

## Tomorrow's concrete choice

Resubmit the existing COMPLETE **`kragglenote2forwork/arc26-b-dprime-v2d` version 2**, immutable script version **357087759**, after matching the live source to [production_manifest.json](production_manifest.json). Archived result: **30.35**, ref **57056539**. The related clean-D-prime version's archived best is **33.50**. Preserve that 33.50 submission as an existing best candidate; a later lower draw does not erase it.

This choice uses the current full-model configuration and does not require a new saved GPU run merely to redraw. If the version, hash, identity, daily slot, competition status, quota accounting or host rules do not match, do not substitute an untested notebook. Record the failed gate and publish the recommendation in chat. Explicitly verify whether an official rerun consumes the user's remaining quota; its historical scoring path can run much longer than the 30–40-minute engineering-session cap. Never reinterpret a nine-hour scored run as a 40-minute GPU job or silently cut its game budget to fit a different assumption.

The exact-code local reproduction is [candidates/arc3_v2d_reproduction.ipynb](candidates/arc3_v2d_reproduction.ipynb). It preserves the baseline's scored branch and eight-minute three-game smoke branch. No new performance improvement is asserted.

[live_verification.json](live_verification.json) now passes the saved source/output checks: canonical code hash matches, same script-version submission is COMPLETE, raw smoke metrics reconcile and the parquet placeholder schema reads back. The raw outputs are the earlier saved commit, not new play today. The runner must still check authenticated identity, the current daily slot, competition validity and quota accounting immediately before tomorrow's action.

## Resource allocation

Treat the stated **three to four Kaggle GPU hours** as a shared quota pool: conservatively 180 quota minutes with 60 reserved. ARC2 L4x4 development costs 2× wall time; ARC3 hardware-specific charging remains unconfirmed. Reserve time for ARC2 as well. Use existing saved artifacts for tomorrow's official choice; spend new GPU time only on information that changes a decision.

| Stage | Machine | Maximum engineering time | Decision |
|---|---|---:|---|
| Source, notebook, branch, data and artifact checks | CPU | No GPU | Reject malformed, drifted, stale, fabricated or incomplete candidates |
| Deterministic public-game action and lifecycle checks | CPU | Short selected-game panels | Verify mechanics, RESET/UNDO, event attribution, cache isolation and output schema |
| Serving compatibility | DGX if already available; otherwise Kaggle | Count startup in the cap | Verify checkpoint, parser, image path, reasoning-history key, speculative head and KV limits |
| One baseline and one candidate breakage screen | Short GPU sessions | About 20 minutes each, each ≤40 minutes | Three-game ft09/sc25/re86 control panel; detect regressions, not rank candidates by hidden score |
| Paired policy-quality experiments | Prefer DGX with pinned target-equivalent stack | Only after breakage pass | Equal wall time, same snapshot/checkpoint, matched concurrency; do not extrapolate CPU replay to LLM quality |
| Large selected-game engineering validation | GPU | **30–40 minutes including startup** | One highest-priority hypothesis; no all-25 sweep by default |

Cancel promptly for startup incompatibility, malformed tools, persistent server death, OOM/retractions, missing gateway, failed artifact integrity or an already-exhausted session budget. Keep exact runtime/model/request settings and diagnostic receipts for every attempt. Reusing a live model across independent experiments saves startup only if isolation and model/config fingerprints are preserved; do not launch parallel full-model stacks.

## First prepared improvement: E-138 prompt screen

[candidates/arc3_e138_prompt_screen.ipynb](candidates/arc3_e138_prompt_screen.ipynb) adds the existing `ARC3_PREFER_TOOL_CALLS=1` system bullet and a fail-closed preflight check to v2d. The harness patch, serving cell, D-prime, lifecycle and game budgets are unchanged. This is CPU-prepared and **not eligible for submission**. Three cells differ: explanation, one env flag, and preflight.

Why this first: archived stalls are measurable, and the candidate changes one model-visible instruction with no new model or parser path. Why the gain is uncertain: long steps often occur before eventual clears, and the model already calls Python during many of them. There is no measured effect size for this flag.

Before promotion, perform a baseline and candidate comparison at the same time, checkpoint, parser and concurrency. The existing ft09/sc25/re86 three-game panel is useful for breakage. Require no crashes/OOM, the flag present in the actual system prompt, valid tool dispatch, healthy prefix reuse, no sustained no-tool/refusal loop, no increase in output truncation, and no large tokens/action or actions/minute regression. Absolute gates such as ≥9 actions/minute are tied to a particular archived three-stream machine; use the paired baseline ratio on the actual machine instead of carrying that number to a different device.

For policy quality, repeat matched passes on a small preregistered panel and report per-game clear rate, median actions per cleared level, total game score with zeros retained, time to first clear, tokens/action and crash rate. Include easy controls and the target failure families. A single seed is a coarse screen. Bootstrap paired game/run differences with confidence intervals only after enough independent runs exist; the available three-game smoke does not support a confident hidden-score claim. If there is no supported gain, keep the baseline and retire the flag.

## Highest-priority engineering work

| Priority | Work | Expected benefit mechanism | Evidence required |
|---|---|---|---|
| 1 | Record live gateway interaction gaps and source/server liveness | Distinguish censored scoring from a weak policy | Actual gap logs and current host rules; no fake heartbeat game actions |
| 2 | Structured failure ledger keyed by full observed state and mechanic hypothesis | Avoid repeating fatal/no-information moves while preserving evidence | Replay semantics, hidden-state caveats, bounded memory and equal-time play |
| 3 | Camera registration with world-coordinate uncertainty | Prevent treating scrolling scenery as moving objects | Annotated bp35/lf52/ls20 frame transitions and rotated/recolored transfer cases |
| 4 | Learn an intervention-to-change matrix for click controls | Offload verified ft09/vc33-style algebra and pattern constraints to exact code | Held-out predictive transitions, mismatch cancellation, tiny search budgets |
| 5 | Retain checked functions and explicit data arguments | Save repeated code tokens without stale layout memory | Existing 27 CPU contracts plus trace-level usage measurement |
| 6 | A small online mode coach over Stock/Probe/Execute/Re-examine/Recover | Allocate thinking to uncertainty and execution to settled plans | Real matched play; no oracle game ID, source code, future clear counter or human baseline features |
| 7 | Full persistent REPL, then executable factorized world model | Reduce regeneration and enable planning on learned rules | Process timeout recovery, per-game isolation, memory limits, cache versioning and meaningful GPU A/B |
| 8 | SFT or small coach learning on blinded successful trajectories | Improve reusable decisions under constrained inference | Fixed game-family holdout, no code-informed eval, data lineage, baseline comparison before packaging |

These are ranked experiments, not additive predicted score gains. An operational fix may protect a valid run without changing intelligence; an algorithm may improve a public game yet harm an unseen one. Keep both outcomes in the write-up.

## Mode design and controls

Use the user-supplied modes as a proposed action policy, not as automatically proven prompt improvements. Keep the selected baseline's actual temperature **0.7** until a paired experiment justifies a change; the pasted Son Stock mode's 0.6 describes another configuration.

Probe: one or two discriminating actions; Hypothesize: predict a transition in code; Execute: batch only a validated plan and stop on mismatch/level change/death; Re-examine: compare hypotheses to recorded transitions; Challenge: test a credible rival; Recover: identify the actual cause before repeating a route; Next Level: retain supported mechanics and test the new element. Avoid firing all these modes every turn or adding a long public-mechanics catalog to every request.

A deterministic first coach can use new-level/death/prediction-mismatch/stall observations. It must expose its reason and budget, enforce caps in code, and log the active mode/version. A learned coach is a later experiment. Its input must be available at inference time and its held-out games must never provide training decisions.

## Selective game panels and generalization

Use the original three-game panel for compatibility. For scientific experiments, balance a small panel by mechanics: one scrolling game (bp35 or lf52), one attribute/energy game (ls20), one attachment/order game (sk48), one temporal cooperation game (g50t), and one cheap pattern/quantity control (ft09 or vc33). Change only the games relevant to the current hypothesis; do not spend GPU to play every public game on every variant.

Choose game-family held-outs before fitting a model or coach. A rotated/recolored copy of a trained game measures within-family transfer. Starting from a saved hard-level state changes the discovery problem. A synthetic trajectory produced with source-code access is a solver demonstration, not blind game discovery. Keep these in separate columns and labels.

## Resubmission and model-promotion criteria

Use an immutable scored version for a redraw, one official submission at a time, with an idempotency receipt and an available daily slot. Promote an experiment only after its runtime checks pass and repeated actual play supports the targeted mechanism without clear regression on controls. Compare the experiment to the unchanged baseline; do not accept notebook-page rank, one lucky public draw, or an attractive title as evidence.

When a scored result arrives, first classify it: healthy completed run, explicit crash/error, possible censoring, version/config mismatch, or normal completed draw. Preserve all draws and zero-score games. An unexpected score triggers diagnosis and repeated controls; it does not prove which flag hurt. Update forecasts using own comparable per-draw results, with uncertainty, and exclude external page maxima from a single-family fit.

Maintain separate **best observed public score** and **best validated configuration**. A best-of-many public draw is selected on noise as well as capability. Select the eventual final two using known valid immutable artifacts and held-out/repeated evidence, subject to current competition rules; do not claim public luck guarantees private rank.

## Research cadence and write-up

Daily `research` and `search` refresh dated notebook versions, discussion changes, primary papers and leaderboard snapshots; `inside` joins own runtime/results to immutable source; `outside` challenges score attribution and unseen-transfer claims; `plan` chooses the next smallest discriminating experiment; `build` makes one reversible version; `cpu` validates deterministic contracts; `gpu-small` and `gpu-panel` record resource receipts; `validate` compares actual outcomes to the preregistered claim; `analysis` produces tables/figures. `submit` remains gated by the root one-shot authorization window.

Weekly, deduplicate the idea bank by mechanism and retire experiments that did not help. Retain negative findings. Publication-quality evidence is an exact source/model/data chain, a clear control, useful diagnostic metrics, uncertainty and a reproduction command—not a long list of named components. Top 1–3 is an objective; neither the current public recipe nor a limited GPU budget supplies evidence that it will achieve that rank.

## Pending evaluation eligibility

The live ARC2 staff clarification introduces a separate one-pending/running limit. The deterministic runner blocks either track while an evaluation remains active, rechecks eligibility at 09:30, 15:30 and 21:30 Seoul on October13, and permits at most one actual write per competition. Prior pending ARC2 entries must finish; they are not retried for recovery. [Staff post](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/discussion/747515).
