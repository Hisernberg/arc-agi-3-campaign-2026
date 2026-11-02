# 08 — Graves and lessons: the failure museum

Every grave below bought a rule that is now part of the daily protocol. Recorded so none of
them has to be bought twice.

## F-1031 — The gateway-patience deaths (Oct-25, Oct-26)

**What happened:** two consecutive fires scored 0.00 with 3411-byte placeholder outputs.
Forensics on Oct-26 proved: the scoring rerun hit a gateway/DNS outage, ran ~60 minutes
(setup + the old 45-minute gateway cap), and the guard submitted its placeholder. The guard
cell was **byte-identical** to the Oct-24 run that scored 26.47 — same code, different platform
behavior. F-1030's original theory (config transplant as the killer) was revised; the agi35
0.00 was the same mechanism.

**Evidence chain:** 3411B placeholders in both runs · rerun lengths ≈ 60 min · guard bytes
identical to a known-good run · 396 teams still scoring Oct-25 (platform alive) · interactive
runs flawless throughout (interactive runs are not scored).

**Rules bought:**
1. The scoring rerun is a separate environment; it must be engineered for (guard-v2: 120-min
   patience, 3600s DNS escape, decision artifact).
2. Interactive receipts prove the code, never the score.
3. A 0.00 triggers forensics before any re-fire.

## F-1030 — The verbatim transplant (Oct-25)

**What happened:** agi35-v1 was a byte-faithful adaptation of a foreign rank-51 config
(LB 35.35). It 0.00'd. Whatever made that config work in its author's pipeline did not survive
the transplant into ours (and the rerun gateway finished it off — see F-1031).

**Rule bought:** never fire a config we did not adapt through our own gates. Foreign ideas
enter as *components*, never as whole notebooks.

## #36 — The rewording grave (Oct-24)

**What happened:** dprime-fix-v3 — a re-anchor of the 33.50 lineage with "hardening" deltas
including prompt-side changes — scored **26.47**, roughly −7 vs the clean config.

**Rule bought:** scheduling deltas are additive constants at proven seams. Prompt rewording is
permitted only per-game via dossier playbooks, never globally.

## The apex-line regression (Oct-20 → Oct-21)

**What happened:** apex-dlex A/B (26.73 / 19.99) and leviathan-v1 (22.47 / 22.33) — each
component green in tests, each draw 3–10 points below the clean engine.

**Rule bought:** single-delta discipline with attribution seams; component σ never projects
onto the leaderboard (see 05).

## The platform-morning massacre (Oct-24, 06:20–11:45Z)

**What happened:** seven consecutive pre-notebook system errors burned the morning; the
eventual 12:45Z resubmission scored 26.47. Two more `error` subs same day. 70 error
submissions exist across the campaign.

**Rules bought:** G1 checks (kernel status, slot state) before every fire; quota-reject probes
designed to be harmless; retry protocol with platform-acknowledged resubmission windows.

## The account-structure collapse

**What happened:** the campaign ran for weeks on a two-account A/B design (the 36.49 uradkr
draw lives on account A). Token rotation and team merging collapsed it into one team with one
daily slot; A/B pairing experiments (Oct-20's dlex pair) died with it.

**Rules bought:** all operational scripts parametrized over owners/versions; same-team kernel
ownership documented (clean-v1 remains directly re-fireable); no plan may assume two slots.

## The auth war (KGAT tokens)

**What happened:** every Basic-auth attempt against the Kaggle API 401'd; four header variants
were tested before the **Bearer** scheme was confirmed. Then the fire endpoint rejected raw
JSON bodies ("missing file_name") twice before the kagglesdk client path was proven.

**Rules bought:** `KAGGLE_API_TOKEN` + kagglesdk is the only fire path; probe scripts pin the
working shapes; every discovery is committed the same hour.

## The sandbox resets (×3 in the final week alone)

**What happened:** the working environment wiped — git history rolled back, `.env` stripped,
`/tmp` toolchain deleted — twice mid-session and once at session start. Untracked secrets were
lost each time; pushed work always survived.

**Rules bought:** push after every completed unit; `.env` rebuild is a 30-second scripted
operation; the worklog is the source of truth, not local state; secrets are scrubbed from
anything that leaves the sandbox.

## The 0.00 ledger (all 20)

Every 0.00 falls into exactly three classes: (a) F-1031 gateway deaths (Oct-25, Oct-26),
(b) F-1030-class unadapted configs, (c) infra errors that reached the scorer. The
classification is why the response is always forensics-first: the three classes have
three different cures, and firing again blindly only burns slots.
