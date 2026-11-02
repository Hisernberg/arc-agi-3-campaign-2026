# 04 — Innovations: what this campaign originally built

Ordered by validated impact. "Validated" means the component-test or receipt evidence, with the
end-to-end score evidence stated honestly where it exists.

## 1. The D′ slot-priority allocator — the engine

**What:** a replacement for the harness's default slot-priority formula. D′ prices every game
slot by action-efficiency and level pace, with a guarded formula that fails open to the harness
default:

- `eff` terms: `eff_const=300, eff_pow=2.5` — slots whose actions historically convert to
  progress get exponentially weighted priority.
- `pace` terms: `pace_pow=0.4, pace_ref=30000` — slots progressing slower than the reference
  pace decay gracefully instead of being starved outright.
- `action` terms: `c_action=0.1, action_scale=115` — action-count normalization.
- `token` terms: `c_token=0.9, token_scale=225000` — token-budget normalization.
- `tail fade 0.4, lin_floor 0.1, rel_pow 0.5` — tail behavior and floors; `fresh-first removed`
  (the harness's novelty bias was actively harmful); budget bands `b1=10, b2=14, b3=16`.

**Evidence:** the single largest end-to-end jump of the campaign (27.67-era → 33.50, +5.8) and
the ownership of every strong draw since (clean D′ μ≈30.5, eis-recovery μ≈30.2). This is the
most validated component we have.

## 2. The stall-knee fold (D2, EXP-106) — scheduling constant with the strongest sweep signal

**What:** measured across the sweep, agent priority decays flatly after ~80 consecutive stall
actions. The fold makes that empirical knee explicit inside D′:

`priority *= max(0.1, 1/(1+(a−80)/40))` — knee 80, halflife 40, floor 0.1.

**Why it matters:** the harness otherwise keeps feeding budget into slots that stopped
converting. The fold is a post-FORM wrap of `tool_agent.priority_value` at the same proven seam
as D′ itself — additive constants only, fail-open to the exact v11 priority on any exception.
**Signal size: 2.8σ** in the sweep — the strongest scheduling constant we measured.

## 3. act_checked() — simulator-verified batching (D2, flagship agent-loop upgrade)

**What:** when the model proposes a batch of actions, the notebook injects a bootstrap that
makes the agent execute **one action at a time**, verifying each against the model's own
`simulate()` of the game state. A divergence raises `PredictionMismatchError` with an explicit
message — remaining batch actions are cancelled to save budget — and the model re-hypothesizes
instead of compounding a wrong world-model across the batch.

**Why it matters:** in a budget-scored interactive environment, one wrong batch is the most
expensive failure mode. act_checked converts it into a cheap, early, recoverable error.
Fail-open chain: no `simulate()` → plain batch; bootstrap literal not found → no injection
(telemetry `act_lit_count`); injection is line-scoped, indent-agnostic, compile-guarded.
**Receipt:** `{'stall': True, 'act_checked': True, 'errors': 0}` on the live GPU run.

## 4. Wastepack — the context-efficiency pack

**What:** wraps `chat_completion` and `dispatch_tool` to kill the three silent budget leaks:
repeated identical messages/lines (dedup), re-asking about known-dead ends (death_ledger),
and re-running already-refuted action sequences (repeat_guard), plus one-step lookahead.
**Receipt:** `death_ledger=1 repeat_guard=1 lookahead=1`, dedup counters live, errors 0.
**Evidence:** green in every apex run; end-to-end attribution still pending (see 05).

## 5. The game dossier (v1 + v2) — 25 games of structured self-knowledge

**What:** a Kaggle dataset built from our own probe sessions and recorded traces:
- **v1:** per-game playbooks, recorded traces, protocol steps, prompt-tail injection.
- **v2 (XPACK):** per-game categories, a transform-tool library (rotation and friends),
  SFT chain-of-thought seeds, and RL seed data — the substrate for the 1,015-item idea pool
  (docs/40/44, batches A–D).

**Why it matters:** it converts single-run experience into a persistent, versioned asset the
agent re-reads every rerun — the only mechanism in the campaign that accumulates across days.
**Known gap:** the transform-tool library currently fails open (`tools: False`) — the prompt
knowledge installs, the callable tools do not. The v13 fix is specified (07).

## 6. Guard-v2 — the rerun-survival layer

**What:** the first and last cell: detects rerun-vs-interactive, verifies the target GPU,
probes the game-service gateway DNS with **120-minute patience and a 3600s DNS-escape** (vs the
45-minute cap that died twice), takes a smoke fast-path when the environment is degraded, and
writes `guard_decision.json` — a machine-readable artifact of what the environment looked like
and what the run decided.

**Evidence:** on Oct-26 it tracked a real **3612-second DNS outage (87 tries)** and committed a
valid placeholder instead of crashing. This is the component that stands between the whole
stack and another 0.00.

## 7. The receipts system itself

Every layer emits `#OURS_*` log lines with structured state; the fire gate greps them in the
kernel output before any submission. This turned "we think it's installed" into a machine-
checkable preflight — the reason the F-1031 forensics could prove byte-identical guards and
the reason attribution is possible at all.

## 8. Provenance discipline (Y21 AUDIT)

Every dataset and model carries an audit line: origin, license, digest. FP8 repacks of
Apache-2.0 upstream weights are documented as third-party public-shareable. This is what makes
the stack safely reproducible and the campaign auditable after the fact.

---

## 9. Transition-graph priors + human-par pace + endgame switch (D3, v13)

Three bounded, multiplicative priority factors built from the game dossier's *measured*
data rather than model vibes: per-game action priors where 0.0 means cheatsheet-measured
dead (8 of 25 games have explicit "never repeat ACTIONn early" lists — parsed by regex);
a per-game human par (parsed from "first levels ~a-b actions (human)" in all 25 cheatsheets)
that tightens exploration when >25% behind pace; and a per-mechanic-family endgame switch
that tilts priority toward known-good actions past a threshold. Every factor is bounded
(x0.65-1.35 total band), fail-open, and carries hit-count telemetry so post-run forensics
can see what actually engaged. Original to this campaign — no public kernel does this.

## 10. Mechanic-true game taxonomy + dataset dual-naming fix

v2's keyword classifier degenerated (17/25 games in one bucket). v3 classifies by *mechanic
signals in the cheatsheets* into 6 balanced families (CLICK-PRECISION 3, HIDDEN-SEQUENCE 5,
DEAD-ANIM-HYBRID 2, DEAD-ACTIONS 4, ANIMATED-TIMING 8, BUDGET-PACED 3) with per-family
strategy/traps/priors/pars. Additionally ships transform modules under BOTH names
(ours_transforms.py + transforms.py) with a runtime exec self-heal — killing the
import-name-mismatch failure class that produced v12's tools=False receipt.
