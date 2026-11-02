# Outsider Agents — Weekly Runbook

## Cadence (every Monday, or after any LB-moving event)

| Step | Who | Action |
|---|---|---|
| 1 | Main agent | Refresh context packs: update `analysis/results.md` ledger, weekly behavior digest, gate statuses; confirm `docs/27` pointers still valid. |
| 2 | Main agent | For each agent X ∈ {A, B, C}: open a new chat/session and paste the FULL content of `agents/outsider/AGENT-X-*.md` as the system prompt, followed by: "Week: YYYY-WW. Context pack files: <paste or attach the listed files' contents>. Produce your memo." |
| 3 | Main agent | Save each memo to `agents/outsider/weekly/YYYY-WW-X.md` verbatim. |
| 4 | Main agent | Cross-review: dedupe overlapping ideas, convert the top ≥3 ideas into REGISTER entries (E-1xx) with falsification criteria, or file a reasoned rejection (rejection reason must quote the agent's mechanism). |
| 5 | Main agent | Feed Agent B's slot schedule into the week's submission plan; feed Agent A's experiment into the GPU plan; feed Agent C's behavior experiment into the CPU patch queue. |
| 6 | Main agent | Append one line per accepted idea to `worklog.md`. |

## Invocation patterns

**Pattern 1 — inside this CLI (preferred):** `Task` tool with `subagent_type: general-purpose`, prompt = "You are <agent>. Read <agent file>, read <context pack>, output memo to <weekly path>." (This is how Week-1 memos were seeded.)

**Pattern 2 — any external LLM:** paste the agent file as system prompt + attach the 4–5 context files. The agent files are deliberately self-contained.

**Pattern 3 — automated weekly:** the same patterns wrapped in a cron/scheduled session; outputs land in `weekly/`.

## Quality bar (memo acceptance)
A memo is accepted only if: (1) it follows its template, (2) every idea has mechanism+cost+falsification, (3) at least one assumption attack targets something the team currently BELIEVES (not a strawman), (4) Agent B's schedule fits the 1-sub/day/account constraint.

## Anti-tunnel-vision rule
If two consecutive memos of the same agent repeat an idea the team rejected without new evidence, the team must either run the falsification test or publicly (in worklog) explain with numbers why the agent is wrong. Silence is not allowed — that is how tunnel vision wins.

## Week-1 (2026-W40) status
Seeded with three memos produced from the full Milestone-2 research pack (docs/27 + research/milestone2/*). See `weekly/2026-W40-{A,B,C}.md`.
