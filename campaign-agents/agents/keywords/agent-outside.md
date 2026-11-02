# keyword: agent outside — brainstorm from outside the campaign

Run the three outsider reviewers defined in `agents/outsider/` (A Systems Sceptic, B Adversarial Strategist, C Cognition
Detective) as three independent subagents. Each gets ONLY: the latest `analysis/plan_*.md`, `analysis/results.md`,
`docs/09-techniques-catalog.md`, the latest sweep digests, and its own agent definition. Each must return ≤ 1 page:
(1) the single biggest thing the campaign is wrong about, (2) three falsifiable ideas ranked by expected LB points per GPU-hour,
(3) one thing to stop doing. Memos go to `agents/outsider/weekly/<ISO-week>-{A,B,C}.md`; `plan` must answer each memo in writing
(adopt / test / reject with reason) in `experiments/REGISTER.md`.
