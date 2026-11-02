# 34 — THE AMBITION DOCTRINE: Speed / Altitude / Depth / Range applied to the ARC-AGI-3 endgame

*Created 2026-10-22 (Task 34), user-ordered: internalize the four ambition axes + Grandmaster
method (validation shield, three-phase pipeline, EDA, disciplined iteration, forum probing)
and rebuild the campaign around them. Trigger context: memsolve-v1 read 0.00 (F-1022) and
the user asked why results keep worsening.*

**Hard calendar (discovered this session): submissions due 2026-11-02, papers 2026-11-08.**
Slot budget remaining: Oct-23..Nov-01 = 10 UTC days × 2 accounts ≈ **20 slots total** (A returns
~Oct-24). Every doctrine below is calibrated to that budget.

---

## 0. The altitude reframe (what this campaign is actually optimizing)

Task-level question we have been answering: "which notebook do we submit today?"
Outcome-level question: "how does the LB score ratchet upward?"
System-level question (THIS doc): **"what machine converts 20 remaining slots into the
highest expected final score?"**

A slot is not a submission. A slot is one pull of a noisy, drifting, hidden-game bandit.
The machine has six stages, each with an instrument:

```
IDEA SUPPLY          FILTER              GATE                FIRE           READ             VERDICT
council 610 ideas -> ev_tracker mu    -> build gates +    -> one call at  -> ev_tracker   -> pre-committed
400 personas          n>=3 drift-adj    offline play         window open     DRAWS append    verdict zones
(sweep automation)    (THIS SESSION)    + control pairing    (fire script)   (THIS SESSION)  (no deliberation)
```

The Oct-22 memsolve 0.00 happened because stage 2 and stage 3 were weak: a lever with
**n=1 public provenance (+1.4, inside the 1.9 noise floor)** went to a slot without a
control pairing and without any offline gate. The Grandmaster rule we violated is the
oldest one: *the public leaderboard is a trap; local validation is the source of truth.*

## 1. SPEED — same work in less time (the latency ladder)

| Iteration tool | Latency | Slot cost | Status |
|---|---|---|---|
| LB draw (rerun) | 6–20 h + read wait | 1 slot | scarce — endgame currency |
| Offline full-play commit-run (#196 pattern) | GPU-hours, no slot | 0 slots | **BUILD NEXT** (needs A quota) |
| 8k-action replay parity gate | minutes | 0 | exists from day-2 kit, port to this comp |
| Byte-gate builds (md5/compile/position) | seconds | 0 | mature (9/10-gate scripts) |
| EV tracker refresh | seconds | 0 | **NEW this session** |

Speed doctrine:
- **S1. Push-ahead pipeline.** Kernels are pushed and COMPLETE before their window opens
  (control kernel done since Oct-21 17:2x; fire = 1 API call at 00:0x UTC). Never build
  inside the window.
- **S2. Fire-at-window-open.** Session death before 00:00 UTC nearly cost Oct-22's slot
  (#212). Procedure: verify gate → immediate fire on window-open discovery. Arm everything
  before closing a session (W38).
- **S3. Quota SLO.** A-account 30h weekly GPU quota hit zero Oct-21 and stayed zero for
  ~3 days (#207). New SLO: forecast own smokes, keep ≥1 account ≥30%, never both at zero
  in the same week.
- **S4. Verdict latency.** Score lands → verdict ≤1h (zones pre-committed; ev_tracker
  recomputes bands automatically). Deliberation is a bug.

## 2. ALTITUDE — the goal beyond the goal

- **A1. Pre-registration.** Every manifest entry carries a `question` field + kill/confirm
  criteria BEFORE firing (Oct-23 manifest already does). A slot that answers no
  pre-registered question is waste — death-trap class, same tier as resubmission.
- **A2. Slots become confirmations, not experiments.** Experiments run free (offline play,
  replays, byte forensics); slots confirm on the hidden set. With 20 slots left the
  ratio must be ≥3 free experiments per slot.
- **A3. Endgame calendar (backward-planned from Nov-02):**
  - Oct-23: control isolator (armed).
  - Oct-24..26: control on A (paired read) + one Tier-A lever with full gates (R3-recording
    half via solved-memory channel, or macro-actions if replay numbers prove out).
  - Oct-27..29: second lever + n=3 reads; promote best pair into the base.
  - Oct-30..Nov-01: **Phase 3** — stack every verified lever onto the best base; final
    draws ride the stacked config; stop changing code after Oct-31.
  - Nov-02: submissions close. Nov-08: paper due (see R7).
- **A4. Explore budget.** Bandit arithmetic: 20 pulls, each lever verdict needs n≥3
  (mu-based). Maximum number of NEW levers we can afford to *evaluate* by Nov-01: **3–4**.
  Choose them by EV, not novelty. Everything else = base redraws (+1–2 each, #100).

## 3. DEPTH — raw material first, instruments second

What a field-leading expert does that we were not doing: go one level below the leaderboard
number to the underlying data and measure what nobody publishes.

- **D1. Structural finding (this session): rerun parquets are per-game score tables.**
  Placeholder schema = `row_id, game_id, end_of_game, score` (one dummy row, 2648 B).
  Rerun outputs = one row per game (3411 B ≈ zero-score rows, 3767 B ≈ 110-game leviathan
  run). We cannot download rerun contents (kernels/output returns the public-run
  placeholder; rerun is a black box — F-1022), but **totalBytes metadata leaks the game
  count**. Build the size→games estimator (W13/W22): every future draw's totalBytes is
  logged in DRAWS notes.
- **D2. Offline set = our CV.** The bundled games (pennyroyal-v253 + taaf-bundle) play
  end-to-end in a commit-run WITHOUT a submission (#196). That is the only place we get
  per-game, per-level telemetry (levels solved, actions/game, exception sites). Build the
  per-game matrix there (W12) and target modules at blocker classes.
- **D3. Drift is quantified now.** clean-dprime slope = **−0.63/day over 8 draws**
  (ev_tracker OLS). eis-recovery σ=0.17 (n=3) — same config, near-deterministic; day
  effects dominate. All bands are drift-adjusted from today; nobody may quote a raw mu.
- **D4. Adversarial assumption audit (the memsolve lesson).** "Solved-level memory is +EV"
  rested on ONE public read (31.46) vs family mu 30.1 = +1.4, inside the 1.9 floor. The
  provenance halo ("LB-proven, same patch family") did the persuading the data couldn't.
  New rule: **any lever whose provenance is a single public read starts at
  provenance-priority B** and rides behind a control, no matter whose notebook it came from.
- **D5. Outside judge.** The ev_tracker board + pre-committed zones are the judge; agents
  and humans alike may not overrule a zone without a new pre-registration.

## 4. RANGE — import fields, not personas

Anti-roleplay rule: each field contributes an instrument or a gate, never a voice.

- **R1. Statistics → sequential testing.** Stop rules: a lever with 2 draws below kill-zone
  is dead (no third draw). Lever reads are drift-adjusted mu n≥3; single draws decide
  nothing.
- **R2. Operations research → slot allocation.** Control-first, then mu-exploit, 1 explore
  slot per 3 days, n_target=3 per lever (ev_tracker §5 is the allocator).
- **R3. Reliability engineering → loud-fail.** The Oct-22 hazard: cell 4's silent
  placeholder path means a lost rerun flag scores 0.00 with zero visible error. Spec (W7):
  placeholder emits a marker row (`row_id=PLACEHOLDER, score=-1`) + distinctive log line +
  abnormal byte size; a 0.00 that is *silent* must become impossible. Required in every
  future build (memsolve v2, any lever).
- **R4. Game AI → options & world models.** Macro-actions (move-until-blocked, repeat-N)
  and K-rules generate→test→prompt-survivors stay the two Tier-A agent levers
  (#125/#126); imagination rollouts bench-only (#127, hidden-cost caution #189).
- **R5. Cognitive science → module families.** Object permanence (track entities across
  frames — transient_pixels native support exists, #134/138) and affordance maps
  (key→effect tables learned in first N actions) are the two human-ARC-inspired module
  slots in the queue after R4.
- **R6. Forensics → byte-level evidence culture.** Rerun black box + parquet byte-size
  discriminator + od-verified module diffs (#214) are the standard; terminal/repr is never
  evidence.
- **R7. Publishing → the paper track (#210).** Cross-account determinism + drift
  decomposition + throughput doctrine is a publishable method (papers due Nov-08, zero
  slots). Draft due Oct-28 — it also forces our own instrumentation clean.

## 5. Grandmaster mapping (the four rules, operationalized)

| Grandmaster rule | Our instrument | Where it lives |
|---|---|---|
| Local CV is the only truth | offline full-play commit-run + ev_tracker drift-adj mu | D2, §3; scripts/harness/ev_tracker.py |
| Public LB is a trap | noise floor 1.9 + paired reads + provenance tiers | ev_tracker §2/§3; D4 |
| One variable at a time | single-lever doctrine + control pairing | #215 amendment, D-2026-10-22-04 |
| Record everything | DRAWS DB (append-only) + ledger + byte forensics | ev_tracker, IDEAS_LEDGER |
| Forum probing | daily sweep + md5/feature census (#155/177) | scripts/sweep_notebooks_daily.py |
| Phase discipline | MVP base ✓ → fast single-lever iteration (NOW) → endgame stack (Oct-30+) | A3 calendar |

## 6. Self-audit: where we broke Grandmaster rules (honest ledger)

| # | Violation | Cost | Fix (status) |
|---|---|---|---|
| V1 | memsolve fired on n=1 provenance halo, no control pairing | 1 slot (0.00) | control-first doctrine #215 + Oct-23 control (armed) |
| V2 | silent placeholder path could mask a lost rerun flag | diagnosis opacity | loud-fail spec W7 (required in all future builds) |
| V3 | both accounts' GPU quota ~zero same week | A blind 3 days | quota SLO S3 (live) |
| V4 | session died pre-window; fire at 08:42 | nearly lost slot | fire-at-window-open S2 (live) |
| V5 | repeated temptation to read single draws as verdicts | 2 wasted lever slots Oct-20/21 | ev_tracker zones (live) |

## 7. What this doctrine executes tomorrow (Oct-23)

1. 00:0x UTC: verify gate → fire **control** arc26-b-dprime-recal-v1 (pre-registered
   question + zones in manifest; isolator for the memsolve 0.00).
2. Score lands (evening): append to DRAWS; verdict ≤1h per zones:
   in-band 26–30 → base healthy, memsolve implicated, R3-recording lever enters gating;
   0.00 → platform breaker, escalate forum, hold all fires; <26 → recompute bands.
3. Run ev_tracker refresh + rebuild bands for Oct-24 lever pick.
4. A-account: rebuild push_a as byte-identical control BEFORE quota reset (~Oct-24);
   push+commit+submit = paired control read n=2.

*The machine, not the notebook, is the deliverable. — end of doctrine*
