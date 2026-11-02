# Y22 Fork #6 intel: Forge v5 "Pathfinder" (persistent-memory BFS/MCTS family)

*Source: nihilisticneuralnet/0-46-arc-agi-3-persistent-memory-bfs-arc-solver
(forked to `dasshovon/arc26-fork-pmem-bfs` v1, CPU, 2026-10-25, pre-deadline)*

## What it is — a DIFFERENT family from the duck harness

Single-file agent (`my_agent.py`, 71 KB) combining classical planning + learned
components. No LLM serving at all:

| Component | Class | Idea for our stack |
|---|---|---|
| MCTS over actions | `MCTSNode`, `ucb1` | Orthogonal to model-proposed actions; tree search over action prefixes where the world model is cheap to clone |
| BFS/DFS solvers | `MultiSolver`, `bfs`, `dfs` | Enumerative solvers with max_states cap; `TimeBudget` gates them |
| Persistent memory | `PersistentAEM` | Autoencoder-based cross-level memory — survives level resets (vs our solved-level memory which only stores wins) |
| Prioritized replay | `PERBuffer`, `SumTree` | Priority-sampled experience for the learned policy |
| Attention net | `ForgeNet` + `CBAM` | Convolutional Block Attention Module on frames |
| Time budget | `TimeBudget`, `mark_done` on WIN | Mirrors our R3 game-over death ledger; per-level budget release on win |
| Non-blocking solve | background thread, `choose_action` never blocks (M2) | Keeps the agent responsive to the harness tick — relevant to our PACE/governor interplay |
| Expert demo injection | `_inject_expert_demos` (archive before PER reset) | Warm-start trick |

## Bug-fix list worth stealing (their C1–C8/M1–M8)

- **C1 GameAction enum mutation** — they re-derive actions via `from_name()` every
  call because the harness mutates enum refs. **CHECK our apex-dlex core for the
  same trap** (we pass action objects around; if the harness mutates them
  in-place, our action ledger could be corrupting silently).
- **C2 coordinate consistency** — unified (row=y, col=x) globally. We had an
  F-family bug in the same area historically.
- **C4/C7 ACTION7 (recall/resume?) index corruption** — pai index set to safe
  value 0; games_done not incremented on ACTION7. If we ever port ACTION7
  handling, inherit this guard.

## Verdict on porting

- **MCTS/PersistentAEM family = NOT a this-week lever** (code freeze Oct-31; a
  new solver family needs weeks of validation). Bank for the paper track +
  2027 campaign.
- **Enum-mutation audit (C1) = DO THIS WEEK** — cheap CPU audit of our core;
  if the trap exists it could explain unexplained wasted-action anomalies.
- **TimeBudget mark_done-on-WIN parity check** vs our R3 ledger — one-cell diff.

## Ledger

- ev_tracker: fork #6 banked (idea family: planning+learned hybrid);
  C1 enum-mutation audit → idea pool P1; finals-stack idea: MultiSolver
  governor (BFS for room-scale puzzles + model for language-y levels).

## C1 enum-mutation audit — EXECUTED 2026-10-25, PASS

Audited the live Y19 build (arc26-b-sample-heat-v1, harness-patch cell + agent cells):
- `GameAction.from_id(int(action_id)).name` — id re-derivation fresh each call (same
  defense as the fork's C1 fix);
- `_format_action_display(action.id.name, dict(action.data))` — data dict COPIED before
  any display/ledger use;
- `_guard_action_data(action)` — dedicated data guard already present.
Conclusion: the enum-mutation trap does NOT exist in the apex-dlex/dprime lineage.
No wasted-action anomaly can be attributed to C1. Audit closed, zero changes needed.
