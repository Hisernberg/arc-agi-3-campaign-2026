# 10 — Assets and infrastructure

## 10.1 Datasets (all attached to the armed notebook)

| Dataset | Role |
|---|---|
| `dasshovon/arc26-game-dossier-v1` | 25 games: own probe sessions, recorded traces, playbooks, protocol steps (CC-0 own data) |
| `dasshovon/arc26-game-dossier-v2` | XPACK: categories for 25 games, transform-tool library, SFT CoT seeds, RL seeds |
| `dfranzen/pennyroyal-v253` | harness wheels (third-party, pinned digest) |
| `dfranzen/taaf-kaggle-source-bundle-copy` | harness source lineage (third-party, fork lineage) |
| `eliork/qwen3-5-27b-fp8` | primary model weights (Qwen3.5-27B FP8 repack, Apache-2.0 upstream, Y21-audited) |

Models attached: `dfranzen/albucino-qwen3-8-flash-next-drafter` and
`dfranzen/intel-qwen3.8-flash-next-w4a16-autoround` (drafter ladder).

## 10.2 Kernels (the living fleet)

| Kernel | State | Meaning |
|---|---|---|
| `dasshovon/arc26-b-apex-v12` v2 | **COMPLETE, receipts green** | the armed Oct-27 weapon |
| `dasshovon/arc26-b-apex-v11` v1 | COMPLETE (scored 0.00 via F-1031) | the D1 draw; source base for the "v11g" fallback |
| `kragglenote2forwork/arc26-b-dprime-clean-v1` v1 | COMPLETE (33.50) | the board-best config; **directly re-fireable, zero build** |
| wastepack-v1 / champion dprime redraw v3 | built, verified | fallback ladder items |
| kernels/ (local): urad-r10, r11-uradfix, r111-hfix, v4base | sources preserved | the uradkr lineage that drew 36.49 |

## 10.3 Operational tooling

| Tool | Purpose |
|---|---|
| `scripts/fire_sdk.py` | the proven fire path: kagglesdk + Bearer, argv-parametrized (owner/slug, version, desc) |
| `scripts/fire_oct26.py` | gate/fire/poll logic: kernel status, slot check (UTC-date), verdict polling |
| `scripts/state_probe_v2.py`, `check_state.py` | identity + submissions + kernel probes (Bearer; list = bare array) |
| `scripts/v11_receipts.py` pattern | kernel-output JSONL parsing + receipt greps (G2 gate) |
| `worklog.md` protocol | append-only multi-agent log; every task ID ends with a stage summary |
| `docs/NN-*.md` doctrine | 59 numbered documents — plans, teardowns, runbooks (snapshotted) |
| `DAILY_PROTOCOL.md` | the G1/G2/fire/verdict daily cycle |

**Auth facts (hard-won):** KGAT tokens authenticate as **Bearer** (`Authorization: Bearer
KGAT_...`), never Basic; `KAGGLE_API_TOKEN` env + kagglesdk is the only proven fire path
(raw JSON bodies are rejected); the three KGAT tokens resolve to one competition team → one
daily slot; GitHub push works via URL-embedded `x-access-token` (askpass is unreliable in the
sandbox).

**Environment reality:** the working sandbox resets without warning (git rollback + secret
scrub + /tmp loss). Countermeasures: push after every completed unit; scripted `.env` rebuild;
kagglesdk reinstall is a two-command operation (`/tmp/kgdeps` + `/tmp/kgpkg/kgsrc`);
the worklog is the source of truth.

## 10.4 The idea bank

- **1,015-item idea pool** (docs/40/44 + batches A–D in `snapshots/reports/`): categorized,
  with the D1–D7 levers drawn from it. The stall-knee (#71) and act_checked (#83) — both now
  in the armed weapon — came from this pool.
- **Dossier stall-flag list**: per-game earliest-stall levels, the priority map for D4
  solver diversification.

## 10.5 Parallel track: AGI-2

`arc-prize-2026-arc-agi-2`: board best **30.97** (v35), v37-EXP resolved 27.36, v38 LEG model
ladder receipts banked (Qwen3.6-27B-FP8 primary). The AGI-2 track functioned as the proving
ground for model-ladder operations and several toolchain pieces later reused on AGI-3.
