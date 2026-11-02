# 07 — Future architecture: the best-possible submission, v13 and beyond

This is the blueprint for climbing from the 33.50 engine into the 38+ gold zone — everything
the council would build with the remaining slots, plus the architecture we would run with
unlimited time. Ordered by expected value per unit of risk.

## 8.1 v13 (D3, Oct-28) — the four concrete deltas

1. **Transition-graph priors (per-game).** The dossier already holds recorded traces. Convert
   them into per-game action-transition statistics (which action from which screen-class yields
   progress) and inject them as a prior over the agent's first-k exploration. Cheap to build
   (data exists), directly attacks the exploration budget — the resource D′ already prices.
2. **KM-style pace table.** A per-(game, level-archetype) empirical completion-pace table from
   the traces, feeding D′'s `pace_ref` per slot instead of one global constant. D′ was built
   for this extension; it's a one-line seam.
3. **Endgame phase switch.** Traces show late-level behavior differs qualitatively (small
   state space, high reset cost). A phase detector that switches the priority weighting in the
   endgame (favor confirmation over exploration) is additive and fail-open by construction.
4. **Fix the XPACK tool registration** (the `tools: False` fail-open). The dossier's transform
   tools were meant to be *callable* inside the agent loop, not just prompt text. The fix is
   specified: import-path hardening + registration retry + telemetry. If it lands, the model
   gains verified rotation/transform operations mid-episode.

Single-delta discipline applies: all four are independent seams; the council promotes only
what the Oct-27/28 verdicts attribute positive.

## 8.2 v14 (D4, Oct-29) — solver diversification

- **Per-category solver strategies.** The 25 games cluster into categories (dossier v2). Each
  category gets a strategy head: exploration-heavy for maze-likes, transform-heavy for
  manipulation-likes, memory-heavy for hidden-rule games. Category detection is already built.
- **Drafted simulation depth.** The drafters (qwen3-8-flash class) are fast enough to run
  candidate rollouts against `simulate()` *before* the primary model commits a batch —
  act_checked generalized from "verify one action" to "test K plans, commit the survivor."
- **Stall-game specialists.** The dossier flags games where every draw stalls at the same
  level; those get dedicated playbook overrides (the one place where per-game prompt edits are
  justified — never global rewording, #36 law).

## 8.3 Rerun-hardening architecture (the platform-war doctrine)

The two 0.00s taught that the scoring rerun is a separate, hostile environment. The
architecture that survives it:

1. **Checkpoint-resume inference.** Persist per-game partial results to `/kaggle/working` as
   the run progresses; the submission parquet is rewritten continuously, so any environment
   death still leaves the *best state achieved so far* rather than a placeholder.
2. **Degraded-mode inference ladder.** If the primary 27B cannot serve within the rerun budget,
   fall back to the 8B drafter as the acting model rather than emitting a placeholder —
   converting a guaranteed 0.00 into an expected 20–28. The guard already detects the
   condition; this gives it a better action than placeholder.
3. **Time-budgeted full-run decision.** Guard-v2's smoke fast-path generalizes: if the gateway
   returns at minute 100 of a 120-minute window, the run should have a *pre-computed* reduced
   plan (fewer games, full depth) instead of an all-or-nothing one.
4. **Support-channel integration.** When forensics proves platform causation (F-1031 class),
   the ticket goes in with refs and timings the same hour — Oct-24's incident was acknowledged
   via the platform's own retry advice.

## 8.4 The variance architecture (how the top of the board is actually reached)

- **Max-statistic farming.** With redraw spread of 5.7 observed on the engine, the expected max
  over k draws of a μ≈33.5 config grows roughly +1.2 (k=3), +1.6 (k=5) at the planning floor,
  more with the real spread. The final slots are worth ~2 points *by themselves* if the μ
  holds — this is why D5–D7 exist.
- **μ-shift stacking.** Each validated +0.5 raises the whole farm. The compounding is the plan:
  D2 (+stall-knee/act_checked) → D3 (+priors/pace/endgame) → D4 (+category heads) each shift
  the farm's μ, and the farm converts μ into max-score.
- **Two-track insurance.** Keep one fully-verified "guaranteed-completes" config (clean-v1
  class) permanently fireable as the day's fallback if the flagship's receipts go amber.

## 8.5 The research bets (beyond this competition's clock)

- **RL on recorded traces.** The dossier's RL seeds are the substrate: train the drafter class
  to predict action-outcomes (a learned `simulate()`), then let act_checked use the learned
  simulator instead of the model's ad-hoc one. This is the highest-ceiling item: it converts
  every future run into training data and every run's failures into a better world model.
- **SFT CoT distillation.** The CoT seeds in dossier v2 define the reasoning format that
  survived our games; distilling the 27B's successful trajectories into the 8B drafter would
  make the fast model a credible verification engine (feeds 8.2's drafted simulation).
- **Cross-game skill graph.** Categories are currently flat. A graph (skills × games) would
  let the agent transfer a discovered mechanic (e.g., a transform sequence) to unseen games
  with matching in-degree — the actual ARC-AGI thesis, applied to our interactive setting.
- **Self-tuning D′.** The allocator's constants (eff_pow, pace_pow, bands) were hand-fit from
  sweeps. A bandit over D′ constants across redraws — using each day's scored draw as the
  reward — turns the redraw farm into a constant-optimizer for free.

## 8.6 What we would NOT do again (negative architecture)

- Verbatim foreign configs (F-1030: 0.00). Adapt or don't fire.
- Prompt rewording as a "fix" (#36: the re-anchor lost ~7 points).
- Layering multiple untested deltas into one fire without attribution seams (the apex-dlex /
  leviathan lesson: 4 draws, −3 to −10 each, unattributable afterwards).
- Trusting an unvalidated rerun path (F-1031: two dead slots).

---

## Post-v13 ladder (post-Oct-26 arena, docs/50)

- **v14 theme: memory + telemetry.** effect-table persistence across RESET, online
  dead-action learning (3-strike), family strategy/dead/par lines in a bounded MEMORY
  block, JSON repair pass, server watchdog + warmup ping, score/pace/latency receipt lines.
  Gate: every delta CPU-tested; one experimental delta max per fire.
- **v15 theme: search + serving research (flagged, not slot-ready).** BFS-light frontier
  search guided by tgraph; spec-decode with Flash-Next NVFP4 MTP (dual-server if VRAM
  fits: 27B FP8 + flash ~43GB < 96GB); vision branch (grid->PNG + STEP labels, Qwen3.8
  multimodal) behind A/B flag; graceful flash-only degradation.
- **Model ladder** (docs/51): Qwen3.8-27B-FP8 primary -> 3.5-FP8 fallback -> Flash-Next
  W4A16 incumbent -> GGUF q4 CPU emergency. Qwen-3.8-family only (directive); 3.8-Max
  open-weights watch.
