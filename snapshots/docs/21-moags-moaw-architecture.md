# docs/21 — MOAGS · MOA+WorldModel · MOAW: New Architecture Stack for ARC-AGI-3

Date: 2026-09-30 · Task 14-d · Companion: docs/20 (Qwen-AgentWorld analysis), docs/22 (updated plan + evaluation)

## 0. What we are building (one paragraph)

Three composable system-level architectures that turn our single-model harness into a **mixture-of-experts stack at the system level** — where the "experts" are entire agents, solvers, and world models rather than FFN slices. **MOAGS** routes each game/level/moment to the right solver specialist. **MOA** fans action proposals across heterogeneous models and aggregates them. **MOAW** verifies every candidate through an ensemble of world models before a real action is spent — protecting the efficiency-squared term that r12 proved is our biggest LB leak (internal 5.19 → official 3.09). Qwen-AgentWorld-35B-A3B (docs/20) is the foundation of MOAW; the two qwen 3.8 versions are members of MOA.

```
                    ┌─────────────────────────────────────────────────┐
                    │                MOAGS ROUTER (bandit)             │
                    │  signals: L1-playbook match, mechanism fingerprint│
                    │  solver leaderboard, dead-end counter, progress  │
                    └──────┬──────────┬──────────┬──────────┬─────────┘
                           │          │          │          │
                    ┌──────▼───┐ ┌────▼────┐ ┌───▼────┐ ┌───▼─────────┐
                    │ PLAYBOOK │ │ EXACT/  │ │ POLICY │ │ WM-GUIDED   │
                    │ EXECUTOR │ │ ALGO    │ │ MIXTURE│ │ PLANNER     │
                    │ (53 lib) │ │ SOLVER  │ │ = MOA  │ │ (beam in    │
                    │ free     │ │ (tr87,  │ │ below  │ │ imagination)│
                    │          │ │ symbolic│ │        │ │             │
                    └──────┬───┘ └────┬────┘ └───┬────┘ └───┬─────────┘
                           └──────────┴────┬─────┴──────────┘
                                           ▼
                    ┌─────────────────────────────────────────────────┐
                    │ MOAW VERIFIER  (imagination gate, pre-commit)    │
                    │ W1 zero-shot AgentWorld-35B-A3B                  │
                    │ W2 ARC-LoRA world model (native fidelity)        │
                    │ W3 tabular transition memory (exact, seen states)│
                    │ W4 algorithmic per-mechanism simulators          │
                    │ output: outcome distribution per candidate action│
                    └──────┬──────────────────────────────┬───────────┘
                        agree→commit                disagree→conservative
                                                      real probe / deep lane
```

## 1. MOAGS — Mixture of Agentic Game Solvers

**Definition.** A learned router that assigns the *currently active game-level-moment* to one (or a weighted blend) of heterogeneous solver specialists. Analogy: MoE is to layers what MOAGS is to the whole agent loop — top-k routing over "solver experts" with a small gating network over cheap features.

**Solver experts (all already exist or are planned in docs/19):**

| # | Expert | Cost per step | Where it wins |
|---|---|---|---|
| S1 | Playbook Executor — 53 verified playbooks, L1 reuse, sb26 L1–L8 chains | ~0 tokens | levels matching library entries; 25/25 games have L1 coverage |
| S2 | Exact/Algorithmic Solver — tr87-style symbolic + per-mechanism (gravity/keys/collision) models | CPU | mechanics already reverse-engineered from public frontier traces (su15 L1–L7, ls20 7/7) |
| S3 | Fast Policy Swarm — 8B NVFP4, 24–26 workers, PLAYBOOK_MODE hints | low | broad exploration, token-cheap |
| S4 | Deep Policy — Qwen3.8-27B NVFP4 (v1) 2–6 workers, ericmao-style adapters where base matches | high | stuck states, mechanism discovery |
| S5 | WM-Guided Planner — beam search in imagination (§3) | medium | efficiency-critical levels (a > 1.5h) |

**Router.** A contextual bandit (LinUCB or even softmax over scored features — NOT an LLM) over features: (i) best playbook similarity of current frame, (ii) mechanism fingerprint from recent frame deltas (objects, gravity signs, key/door counts), (iii) per-game solver leaderboard from all our recorded runs, (iv) rolling dead-end/progress counters, (v) actions-used vs human-baseline ratio (efficiency pressure ⇒ escalate to S5/S2). Trainable offline from our 2M+ recorded transitions with per-solver counterfactual labels — no online exploration cost.

**Why this is more than a diagram:** our current harness already hard-codes 60% of it (playbook hints, two-lane vLLM, governor). MOAGS = (1) env-var switches become router outputs, (2) the router is learned instead of hand-tuned, (3) S2/S5 get real implementations instead of TODOs. Phased rollout in docs/22 keeps each step gated.

## 2. MOA — Mixture of Agents (policy level), adapted for action spaces

**Definition.** Standard MOA (propose → aggregate → refine across multiple LLMs) mapped to a 6-button action space where "refinement" means *verification and selection*, not text editing:

1. **Propose (fan-out, decision points only).** At every step, S3 (8B, n=4 samples) + S4 (27B, n=1–2) + S5 planner top-1 propose candidate actions with short rationales. Continuous-action steps skip the fan-out (momentum movement) — trigger only at decision points (new room, item pickup, fork, post-death).
2. **Aggregate.** Layer 1: reliability-weighted vote (weights = per-game per-solver historical success, same table as router feature iii). Layer 2: the aggregate is a *distribution*, not an argmax — ties and low-margin cases escalate to S4 or MOAW disagreement resolution.
3. **Refine/verify.** The top-2 candidates go to MOAW (§3). Nothing is committed on vote alone.

**Token budget guard:** fan-out only at decision points (~15–25% of steps in our traces), n_total ≤ 6 proposals, each proposal ≤ 64 tokens rationale. Estimated overhead vs current single-model: +18–30% tokens on decision steps, −40–70% wasted real actions if MOAW holds ≥85% accuracy. Net strongly positive under the squared-efficiency penalty.

## 3. MOAW — Mixture of Agentic Worlds (the novel layer)

**Definition.** An ensemble of world models with *complementary priors*, producing an outcome distribution `P(next state class | frame, action)` for every candidate action — and an agreement signal that gates commitment.

| World | Prior | Strength | Weakness |
|---|---|---|---|
| W1 zero-shot Qwen-AgentWorld-35B-A3B | 10M+ agentic trajectories, 7 domains | broad dynamics priors; OOD robustness | never saw game grids; 32K-think token cost (compress to 1–2K) |
| W2 ARC-native world LoRA (Mode C, docs/20) | our 2M+ transitions | highest in-distribution fidelity expected | blind outside seen mechanics |
| W3 tabular transition memory (append-only, PRO-LONG-style) | exact dict over hashed (frame, action) | **perfect** where we've been | zero generalization |
| W4 algorithmic simulators | symbolic per-mechanism (gravity/keys/collision) | exact within mechanism + cheap | needs mechanism ID, brittle at boundaries |

**Agreement protocol:**
- All available worlds agree on outcome class → commit candidate (or if class = no-op/death, skip — saved a real action).
- W3 exact match exists → W3 overrides all (ground truth).
- Disagreement → (a) if any world says "death/softlock", veto; (b) else pick the candidate with best expected progress under the W2-weighted mixture and, if the action is cheap to recover from (no irreversible state), spend the real probe; (c) irreversible + uncertain → escalate to deep lane with explicit "unknown" flag.
- Every real transition (agreed or not) is logged back into W3 and queued into W2's next fine-tune round — **the ensemble self-heals toward exactness**.

**Why MOAW is the crown layer:** it is the only component that directly attacks the squared efficiency term *and* manufactures clean training data for everything else (paper paradigm 1: counterfactual rollouts for RL). Nobody on the LB leaderboard is running anything like it in public notebooks — the public frontier is single-model harnesses plus raw compute (Tufa Labs).

## 4. Memory & serving budget (RTX PRO 6000 96 GB)

| Config | Weights | KV left | Workers (8B / WM / 27B) | Verdict |
|---|---|---|---|---|
| Current dual-lane (docs/17) | ~33 GB | ~55 GB | 24–26 / – / 4–6 | incumbent |
| MOAGS-lite (8B + 27B + router) | ~33 GB | ~55 GB | unchanged | Phase 0.5 — no new VRAM |
| + MOAW sidecar (W1 AWQ-INT4 ≈ 20 GB) | ~53 GB | ~35 GB | 10–12 / 2–4 / 2 | Phase 1 — KV budgeted per docs/17 lesson |
| Full stack (W1 bf16 34.7 GB instead of AWQ) | ~68 GB | ~20 GB | 8 / 2 / 1 | only if AWQ fidelity insufficient |
| Flash-Next NVFP4 endgame (~60 GB, single model replaces 8B+27B) | ~60 GB | ~28 GB | lane-free | gated on `qwen4_exp` serving support |

Note: W3 (dict) and W4 (CPU) cost no VRAM. W2 shares W1's instance as a LoRA adapter (vLLM multi-LoRA) — that is the point of building W2 on the W1 skeleton.

## 5. Failure modes & defenses

| Failure | Defense |
|---|---|
| W1 imagination wrong on grids (domain shift) | §3 probe gate (≥85% outcome accuracy) before any MOAW authority; W3 override; veto logic favors safety |
| Router misroutes (bandit cold start) | default = incumbent dual-lane behavior (S3); router earns authority per-game only after offline validation |
| Token blow-up from fan-out + imagination | decision-point-only triggers; hard per-step token ceiling; MOAW calls batched; sleep/wake sidecar |
| KV collapse when 3rd instance added (docs/17 lesson) | budget KV before adding; degrade 27B to 2 workers; AWQ before bf16 |
| 1 sub/day burned on a broken stack | all gates offline (engine equivalence proven); PLAYBOOK_MODE + router behind env vars; smoke-run on ls20/tr87 local replay before every submission |

## 6. Novelty check (why this is genuinely undiscovered)

- Public ARC-AGI-3 artifacts (our sweep, docs/10/13): single-model policy harnesses, trace replay, brute-force action search. No system-level routing, no verifier ensemble, no world-model layer.
- NVIDIA AVO (docs/12) hit 183/183 with a harness-first design — proof that *system architecture > raw model* is the winning axis. MOAGS/MOAW is a strict superset of "harness > model" with a learned router and an imagination gate.
- Qwen-AgentWorld itself is 3.5 months old and targeted at productivity-agent domains; no known use of it (or any LWM) as a game-playing verifier ensemble. MOAW as defined — heterogeneous world ensemble with agreement-gated commitment and self-healing logs — is, to our knowledge, unpublished anywhere.

## 7. Expected impact (fed into docs/22 evaluation)

- MOAGS-lite (routing + playbook/algo experts formalized): +1–3 LB over Plan A alone (removes cross-contamination of lanes).
- MOA proposal/vote: +0.5–2 via fewer dead-ends on mid levels.
- MOAW with passing fidelity gate: the efficiency shield is worth **+3–8 LB** at our action counts (mechanism: pushing a≈2h levels toward a≈1.5h multiplies per-level factor ~1.8×; compounding across 15–25 levels), and it is the prerequisite for Phase 2's 70–90-level ambition.
- Risk-adjusted (P(fidelity gate) ≈ 0.55 zero-shot, ≈ 0.8 after Mode-C LoRA): the stack remains the highest-EV build we have.
