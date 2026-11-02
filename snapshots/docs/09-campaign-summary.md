# 09 · Campaign Summary Report (Setup Day — Sept 19, 2026)

**Campaign:** ARC Prize 2026 – ARC-AGI-3 (Kaggle) · **Team:** Kragglenote2 Forwork
**Prepared by:** Super Z multi-agent session (research sub-agent + main agent)

---

## 1. Executive summary

The campaign infrastructure is now fully operational: competitive intelligence gathered,
the complete Duck solver source recovered and understood, a **GPU-free local development
loop** established (all 25 public games run offline on CPU via the competition wheels),
the first improvement variant (**duck-governor-v1**) built and unit-tested against the
real solver code, and a private GitHub repository consolidating all knowledge, plans and
tooling. Current best score **3.45**; leaderboard #1 is 18.81; the highest-leverage
confirmed lever in the literature (executable world models + probe discipline) maps
cleanly onto our architecture and is sequenced for the coming week.

## 2. Position assessment

| Metric | Value | Read |
|---|---|---|
| Our best submission | 3.45 (Sept 18) | ~11 submissions, improving ~+0.5/week organically |
| Leader (Tufa Labs) | 18.81 | Duck harness authors — our base, heavily iterated |
| #2–#4 | 11.04–13.12 | No public write-ups; gap to top-5 ≈ +2.4 |
| Run variance | ±0.4–1.0 | 1.79→3.45 observed on near-identical configs |
| Time left | M2: Sep 30 · Final: Nov 2 | 11 days to M2, ~6.5 weeks to final |

Score granularity: each newly completed level ≈ **+1.5–3 points** total (level-index
weighted, completion-capped, squared efficiency). Path to double digits = converting
stuck-at-L1/L2 games into L3–L4 finishes across most of the 110 hidden games.

## 3. What was delivered today

1. **Research dossier** (`docs/03`, `research/`): scoring methodology confirmed (RHAE,
   1.15 cap, level weighting); Tufa Duck architecture fully documented; SOTA survey
   (Schema 99%, NVIDIA AVO 100%, Tycho 100%, SwarmOS, Strands — all harness-first
   approaches); Kaggle-viable M1 runner-up recipes (Reki, forge).
2. **Solver source recovered**: Duck bundle (61 MB Kaggle dataset) downloaded and
   analyzed — `tool_agent.py` (2,063 lines) turn loop, tuning surface (14 env knobs +
   solver config), serving profile `kv5-bf16-mtp3-c8-cg32`, ACTION7/UNDO handling.
3. **Local CPU engine**: `arc_agi` + `arcengine` wheels installed in venv; offline
   Arcade plays all 25 games; API↔local consistency validated (25/25 identical).
4. **Game knowledge base**: metadata table with per-level human baselines
   (`docs/05`), L1 board atlas (text + PNG), efficiency-priority ordering (VC33 L1=7
   actions … WA30 Σ=1,843).
5. **First variant built & tested** (`notebooks/duck-governor-v1.ipynb`):
   - *No-op-loop governor*: counts consecutive real actions with `board_changed=false`;
     injects escalating notices at 3/6/10 into the tool result — directly attacks the
     squaring-punished waste mode (research finding #10, Duck prompt lessons).
   - *Schema-lite addendum*: numbered mechanic hypotheses, refutation tracking,
     discriminating-probe selection, search-over-probing preference, RESET discipline.
   - *Engineering safety*: idempotent, fail-open, mirrored across by-value imports
     (a real bug found and fixed during testing), 6-case unit suite against the REAL
     solver module — all green.
6. **Automation** (`scripts/`, `docs/08`): Kaggle API clients (leaderboard, submissions,
   datasets), daily loop orchestrator with variant table + submission rules, kernel-push
   bootstrap, rollback rules.

## 4. Week-one plan (detailed in `docs/07`)

Daily cadence from Sat 9/20: one variant/day, submitted 2× (variance harvest); GPU
exhausted → resubmit best. Variant sequence: governor-v1 (Sat) → budget triage (Sun–Mon)
→ world-model loop v0 (Tue–Wed) → context engineering (Thu) → best-of-week (Fri).
M2 open-source freeze prep begins 9/26.

## 5. Risk register (top 5)

1. **Public-25 overfitting** — mitigations: generic (never per-game) changes; 2× same-day
   submissions; ablate on ≥2 games.
2. **GPU quota burn** — mandatory local dry-run + unit tests before any Kaggle run.
3. **Variance misread as signal** — results log tracks config fingerprints; rollback rule
   if variant < best − 1.0.
4. **Serving instability on rerun** — watchdog already in fork; smoke-test cell runs
   `/v1/models` check before play (in notebook 12 lineage).
5. **Credential hygiene** — tokens live only in gitignored `.env` + askpass helper;
   recommendation: rotate both tokens after the campaign (shared in plaintext chat).

## 6. Decision log (today)

| Decision | Rationale |
|---|---|
| Ship Governor v0 before world-model loop | Zero behavioral risk, targets confirmed waste mode, testable CPU-only |
| Keep ACTION7/UNDO disabled | Tufa evidence + upstream source has no mapping; ablation later |
| Keep Qwen3.8-NVFP4 serving profile unchanged | Profile already A/B-winned (notebook 11/12 sweep); revisit only after harness changes land |
| Local-first verification protocol | M1 medalists' lesson: public Kaggle scores are noisy; iterate free, submit once |
