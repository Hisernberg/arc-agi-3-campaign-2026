# 15 · The Plan: 4.07 → 60/183 → 90/183 levels (2026-09-29)

## Where we are (verified 09-29)

- Best LB 4.07 = 41/183 levels, mostly L1-L3, mostly human-parity efficiency.
- Leaderboard: #1 45.33, #2 36.73, #3 26.55. 90 levels at good efficiency ≈ 35-55 LB
  (top-3 territory); 60 levels ≈ 14-25 LB (top-25).
- One submission/day per account; ~4 weeks left (deadline 11-02). Milestone-2 open-source
  cut due 09-30.

## Score arithmetic (why this plan is shaped the way it is)

per level: min(human/agent, 1.15)² × level-index weight / Σweights, averaged over games.
- A wasteful L1 (2× human) scores 0.25 of its weight — HALF the level's value burned.
- Deep levels are worth multiples of L1 (weight = level index): L5 of a 7-level game
  is worth 5× L1. Reaching L4-L7 on 10 games beats L1 on 25 games.
- Verified playbooks (our own Kaggle-proven sequences) convert "explore 50-190 actions"
  into "replay 8-50 known-good actions" — freeing 30-50% of the time budget per game.

## Phase 0 — Playbooks + efficiency governor (build today, submit tomorrow)

1. Ship `PLAYBOOK_MODE=1`: embed own_playbook_library.json; on game+level recognition,
   emit the verified sequence (fail-open to normal policy on any board-hash mismatch).
2. Embed ARA verified transfers (lf52 L1 9-act, su15 L1 18-act) — they beat ours.
3. Efficiency governor: hard cap per level at 2.0× human baseline (from metadata);
   on breach → RESET once, then park level. Zero-game triage list: sk48, dc22, cd82,
   g50t, r11l capped at 60 actions each.
4. Expected: same level count, big efficiency gain + 3-5 extra levels from freed budget
   → **LB 7-12**. All env-var switchable, 30+ preflight greens before submit.

## Phase 1 — Model swarm two-lane + mechanic priors (2-4 days)

1. Two vLLM lanes on the 96GB card (docs/14): 8B NVFP4 fast lane (24-26 workers)
   + 27B NVFP4/FP8-KV deep lane (4-6 workers) with router (stuck > 25 actions or level ≥ 3).
2. Inject ARA world-model mechanic notes as per-game strategy priors for
   ls20 / su15 / tr87 / wa30 / lf52 (win-rules, claims, heuristics — prose in prompts,
   not scripts; they transfer even where replay scripts do not).
3. tr87 algorithmic solver: the ARA doc gives the complete win-rule (8 dihedral transforms,
   legend substitution) — implementable as pure code given frame parsing; no LLM needed.
   Same for su15 L2-L3 recipes and ls20 key-delivery geometry.
4. Expected: 55-70 levels → **LB 15-25** (top-10 range).

## Phase 2 — Deep-level capability (week 2+)

1. Skill library from bestiary `agentica_lite` (predicate library + stalemate triggers).
2. ericmao ARC-AGI-3 LoRA adapters on the deep lane (sft-v3 / grpo / human100 A/B).
3. JEPA-lite frame-prediction head for cheap "what-if" action screening (M1 spec).
4. Optional fast-lane swap test: Ornith-1.5-35B-A3B agentic NVFP4 (2.5× decode).
5. Expected: 70-90 levels → **LB 30-50** (top-3 range depends on field movement).

## Risks & mitigations

- **Two-instance serving instability on Kaggle** → fallback: single 8B lane + Phase-0/1
  non-model gains (still the bulk of the plan).
- **Board-hash mismatch on playbook replay** → fail-open to normal policy (never stall).
- **Rule compliance**: playbooks/mechanics derive from public external data (allowed,
  disclosed in documentation; winner-obligations reproducibility satisfied by repo).
- **Multi-account rule**: Kaggle rules prohibit entering/submitting from multiple accounts
  — consolidate to ONE account for submissions immediately (flag raised to operator).
- **1/day budget discipline**: never burn a slot without 30+ preflight greens + local
  benchmark ≥ current best internal score.

## Milestone-2 (due 09-30) go/no-go

Open-source cut is required for milestone prizes. The repo (docs, playbooks, governor,
swarm design) is publishable as-is. GO: publish after Phase-0 submit, keeping the
Kaggle-token layer out. The competitive edge (fresh playbooks + swarm serving) stays
ahead of any copied snapshot.
