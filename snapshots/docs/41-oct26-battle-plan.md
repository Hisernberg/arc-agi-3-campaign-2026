# 41 · Oct-26 BATTLE PLAN — wastepack-v1 fire day (written 2026-10-25 13:00Z)

## 0. Situation (start of planning)

- **Oct-25 slot consumed**: AGI35 config-swap → **0.00** (ref 57627860, kernel complete, no
  failureMessage). F-1030. Root cause: the AGI Boys env block is an interface contract with THEIR
  patch (TAIL_FADE deadline wiring / _PriorityGate handover). Anchor **26.47 stands** (attempt-8,
  ref 57594680); ratchet verdict = REJECT, draw logged.
- **LB**: rank 106/4799, best 33.50, 64 subs. Team `arc-needs-to-be-agi` (dasshovon + kragglenote2forwork).
- **Sweep complete**: 718 notebooks listed, 30 pulled, 12 deep-mined → 112-entry idea pool
  (docs/40). F-1030 lesson encoded: port mechanisms, never env blocks.
- **Next slot**: Oct-26, **dasshovon (B lane)** per user directive.

## 1. The Oct-26 submission: `dasshovon/arc26-b-wastepack-v1`

**Base**: byte-identical champion `arc26-b-dprime-fix-v1` (the 26.47 anchor build) with FOUR
enumerated deltas — no harness edits, no prompt rewording, everything fail-open:

| Δ | What | Why (evidence) | Fail-open? |
|---|---|---|---|
| D1 | header md updated | ledger | n/a |
| D2 | env: `ARC3_DEATH_LEDGER=1`, `ARC3_DEATH_REPEAT_GUARD=1`, `ARC3_DEATH_GUARD_LOOKAHEAD=1`, `ARC3_WM_WIPE_ON_GAME_OVER=0` | death ledger ships OFF in dfranzen's arm but **ON in the M2-top lineage** (v29); fatal-prefix lookahead blocks whole doomed batches ("nothing is spent"); keep-notes-on-death neutral-to-positive [shiiin9] | config-only; flags read at call time |
| D3 | NEW cell 24 "context-efficiency pack": W1 USER-boilerplate dedup (affectify EXP-105: **-24.5% input tokens**, 19/23 lines identical across USERs), W2 identical-snippet refusal in-turn (TAAF F4: real stall 46 min / 35 calls / 0 actions), W3 turn counter; hasattr contracts raise on drift | two most-measured context levers in the sweep, both absent from our base | whole cell try/except → prints `#OURS_WASTEPACK disabled` → vanilla champion |
| D4 | stats print after run (`#OURS_WASTEPACK stats {...}`) | forensics at zero slot cost | try/except |

**Design guarantees**:
- Patch cell (cell 5) md5 UNCHANGED (verified G2).
- Guard cell / D' priority cell byte-identical (G6/G8).
- Worst case for ANY component = vanilla champion behavior (T4/T7 tested on the REAL patched module).
- Kernel metadata identical except id/title (G10).

**Verification done (2026-10-25)**:
- Build gates **10/10 GREEN** (`scripts/build_wastepack_v1.py`).
- Unit tests **8/8 PASS vs REAL patched harness** (`scripts/test_wastepack_v1.py`): dedup
  str+parts, safety, real-module install, refusal + turn boundary, wrapper integration,
  idempotency, contract-raise, env flips.
- Known quirk (pre-existing, all 20+ public builds identical): dfranzen's published patch's final
  hunk is truncated mid-hunk; Kaggle's git applies it (sample-heat + agi35 kernels ran COMPLETE
  today), local git 2.47 needs the final hunk trimmed for testing only.

**Expected value**: waste elimination attacks the efficiency term directly
(level_score = (human/ai)² — every saved action compounds). Death-ledger lineage (M2-top) is the
strongest measured guard upgrade we don't run yet. Downside bounded at vanilla-champion re-draw.

## 2. Verdict rule (pre-committed, unchanged)

- Baseline = **26.47** (anchor). Noise floor ±1.9.
- **> 28.37** → PROMOTE (wastepack becomes new incumbent; anchor moves).
- **26.47 – 28.37** → NOISE BAND: keep anchor, do NOT promote, log draw.
- **≤ 26.47** → REJECT (wastepack dropped; champion config returns for Oct-27).
- Any 0.00/error → treat as F-chain event, forensics before ANY re-fire.

## 3. Fire-day runbook (Oct-26, B lane)

1. **~08:00Z** — push kernel: `KAGGLE_API_TOKEN=<B_TOKEN> venv/bin/kaggle kernels push -p artifacts/daily/2026-10-26/push_b_wastepack_v1/`
2. **Poll kernel status** (foreground `fire` script pattern — sandbox kills background procs):
   - COMPLETE → gate G1 pass.
   - ERROR → read log; ONE retry allowed after 60-120 min cooldown; second failure → fallback ladder.
3. **Gate G2**: no pending submission (allowance free).
4. **FIRE** (CreateCodeSubmission, description per template) → ref logged to `reports/oct26_draw_wastepack.json` + `submit_log.jsonl`.
5. **Verdict poll** every ~30-60 min; on complete → apply §2 rule; write `docs/42-oct26-live.md`.
6. **Fallback ladder** (if wastepack kernel cannot be fired):
   a. **Y19 sample-heat v1** — temp 0.7→1.0 single lever; 9/9 gates; kernel already ran COMPLETE today; un-fired.
   b. Champion re-draw (`arc26-b-dprime-fix-v1` v3) — pure variance wash, still useful (2nd clean reading of the anchor band).
7. **Parallel (A lane)**: read probe v12 (F-1029 heal) status → COMPLETE → tonight build CH1 v4
   (`build_ch1_qwen35_v1.py`, 14/14 gates) as the model-track challenger; ERROR → CH1 stays parked,
   Y25 escalation draft stays warm.

## 4. Week horizon (scored-slot-days remaining ~7: Oct-26 → Nov-02 freeze)

| Day | Primary | Track |
|---|---|---|
| Oct-26 | **wastepack-v1 fire** (this plan) | F-1029 heal read; CH1 v4 decision |
| Oct-27 | verdict-driven: if wastepack ≥ noise band → wastepack-v2 (add #71 stall-knee into D' patience term; measured 2.8σ by author) else single-lever re-draw | CH1 v4 fire if healed |
| Oct-28 | Y25 build start: **DF-WM `act_checked()` port** (idea #83, 372 lines stdlib, fail-open install pattern proven by this pack) | — |
| Oct-29 | **best-of day** (frozen calendar): re-fire best confirmed config | Y25 smoke |
| Oct-30/31 | Phase-3 stack + code freeze | Y25 fire if gated |
| Nov-01 | finalists | — |
| Nov-02 23:59 | **DEADLINE** | — |

## 5. Danger register (read before ANY deviation)

1. **Never re-fire on the same day after a 0.00** without forensics (F-1022/F-1030 pattern: two
   draws burned on un-understood failures = the death trap).
2. **No prompt rewording** (sweep: -43% run). Additive text only, A/B'd.
3. **No config transplants** from other families (F-1030). Env flips only for flags that exist in
   OUR bundle (G5 checks this).
4. **Sandbox kills background processes** — all polling is foreground (`loop N` ≤ 560s windows).
5. **One slot per day** — G1+G2 gates before every fire; auto-fire only from the gated script.
6. **Noise floor**: a single reading never promotes. Anchor moves only on > 28.37.

## 6. Ledger

- Idea pool: docs/40-oct26-idea-pool.md (112 entries, evidence-tagged).
- Build: `scripts/build_wastepack_v1.py` → `artifacts/daily/2026-10-26/push_b_wastepack_v1/`.
- Tests: `scripts/test_wastepack_v1.py` (8/8 vs real patched harness).
- Forensics: `scripts/oct26_forensics_f1030.py` → `reports/oct26_sweep/f1030_forensics.json`.
- Sweep data: `reports/oct26_sweep/notebooks_master.{json,csv}` (718), `leaderboard_full.csv` (4,799),
  sources in `artifacts/forks/oct26_sweep/` (30 notebooks).
- F-1030 lesson → F-chain: F-1024 → F-1025 → F-1026 → F-1028 → F-1029 → **F-1030 (config
  transplant without interface contract = 0.00; port mechanisms not env blocks)**.
