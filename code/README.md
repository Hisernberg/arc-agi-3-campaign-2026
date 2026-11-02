# code/ — scrubbed operational artifacts

Everything here was extracted from the private campaign repos with a credential scan
(Kaggle tokens, GitHub/HF PATs, basic-auth strings — all excluded by pattern before commit).

| Path | What it is |
|---|---|
| `endgame-v63/` | Final-day kernel builder (v63 validation builds): `scripts/build_v63_finalday.py` + builder notebooks + selection receipts. The build scripts contain their own anti-leak scrub lists. |
| `endgame-v45s/` | Endgame builder v45s / v44-mixture (same family). |

## The fire-day operating protocol (prose; the runnable versions stayed private)

The campaign's single most load-bearing process artifact. Two submission slots per day,
one per account, leaderboard keeps the max — so every fire must be * survivable *.

### Pre-flight gate matrix (run before every push/fire, fail-closed)

| Gate | Check | Failure action |
|---|---|---|
| V0 | Syntax/import of every cell (`ast.parse` / `py_compile`) | no push |
| V1 | Cell count + byte budget vs competition limits | no push |
| V2 | Docker image pin matches the verified family pin | no push |
| V3 | Armor markers present (6/6 S14 keepalive/warmup/heal greps) | no push |
| V4 | Zero drift: to-be-fired `scriptVersionId` == receipt-verified version | no push |
| V5 | Description/keyword receipt embedded in the submission | no push |
| V6 | Deadline math: fire time + empirical verdict latency vs cutoff | no push |
| V7 | Human/agent fail-closed review — any unexplained doubt | no fire |

### Fire-day timeline template

1. **T-1 day:** build → gates V0–V5 → freeze (no further edits; drift = re-gate).
2. **T-0 00:05Z:** submission window opens; fire per gate matrix V6–V7.
3. **T-0 +minutes:** receipt capture (ref, scriptVersionId, byte size, description).
4. **T-0 +9–15h:** verdict watch; every verdict gets an attribution before the next decision.
5. **0.00 verdict ⇒ forensics, never a blind re-fire** (byte-for-byte diff vs last completed run).

### Armor checklist (what "S14" means concretely)

- keepalive heartbeat thread (survives slow gateway phases inside the scoring rerun)
- startup warmup reset (first-actions determinism after boot)
- **mount self-heal** (v25): re-resolve the dataset mount by content marker (`_find_input`)
  across the mounted filesystem instead of trusting a single resolved path
- retry with backoff on gateway errors; never exit non-zero on transient infra failures

### Ledger discipline

Every fire appends one line to the worklog: task ID, what advanced, evidence (refs/shas),
next step. Every verdict updates the score ledger with an attribution. This repo's
`data/` directory is exactly that discipline, exported.
