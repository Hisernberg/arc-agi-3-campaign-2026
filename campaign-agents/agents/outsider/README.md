# Outsider Agents — Weekly Outside-View Review Board

Three independent "outsider" reviewer agents give an external overview of the campaign each week and generate ideas grounded in the Milestone-2 thought process (docs/27). They exist because the team inside the campaign develops tunnel vision: the M2 evidence shows the biggest wins came from OUTSIDE the prompt-engineering local optimum (serving forks, KV pools, schedulers) and the biggest losses from unexamined assumptions (advice text, world-model scaffolds, T=0.3).

| Agent | Outside view | Owns the question |
|---|---|---|
| **A — The Systems Sceptic** | Inference/serving engineer from a different field (no ARC history) | "Is your machine converting hours into decisions at the physical limit?" |
| **B — The Adversarial Strategist** | Competition strategist / game theorist (opponent's chair) | "What would the leader do to make sure you stay below them? Are you playing the meta, not just the game?" |
| **C — The Cognition Detective** | Cognitive scientist / game designer (how agents learn novel games) | "Why does the agent keep defending the wrong goal hypothesis, and what would a curious child do differently?" |

## Files

- `AGENT-A-systems-sceptic.md` — full agent definition (self-contained system prompt)
- `AGENT-B-adversarial-strategist.md` — full agent definition
- `AGENT-C-cognition-detective.md` — full agent definition
- `RUNBOOK.md` — weekly cadence, how to invoke, output storage
- `weekly/YYYY-WW-{A,B,C}.md` — one memo per agent per week (Week-1 = 2026-W40 seeded)

## Contract (all three agents)

1. Read ONLY the context pack listed in their file (kept small + current; main agent refreshes pointers).
2. Produce a memo in the fixed template: Outside Overview → Assumption Attacks → 5 Ideas (ranked by EV/effort, each falsifiable) → One Experiment (with kill criterion) → What Would Make Me Quit This Plan.
3. Every idea must state: mechanism (WHY it should move LB), cost (GPU hours / submission slot / CPU), falsification test.
4. Hard constraints they must respect: 1× RTX PRO 6000, 9h wall, no internet on rerun, 1 submission/day/account, target LB 27+ per docs/27.
5. They are outsiders: no loyalty to past decisions; they may say "abandon X".
