# docs/49 — Oct-27 GOLD plan of record + KEYWORD protocol

Built Oct-26 evening (13:00-14:30Z wave). This doc is the single source of truth for tomorrow.
Slot opens **00:00Z Oct-27** (= 06:00 Dhaka). Fire window **00:05-00:10Z**.

## 1. The weapon: apex-v13 (dasshovon/arc26-b-apex-v13, version 1)

apex-v12 (D2: stall-knee + act_checked + guard-v2) **PLUS** D3, all fail-open:

| Delta | What | Receipt to verify (G2) |
|---|---|---|
| **M** Qwen3.8-27B-FP8 swap | saltb0x mirror (25.3GB) first in MODEL_DIR chain; 3.5 fallback; fingerprint prefer-3.8 break | `#OURS_V38 served=qwen38-27b-fp8 dir=...qwen3-8-27b-fp8` |
| **(a)** XPACK tools heal | `ours_transforms.py` shipped (v2 shipped only transforms.py → tools=False); heal re-registers module | `#OURS_XPACK ok ... tools=True` (v13 heal receipt `tools_heal=exec-ok`) |
| **(b)** #48 tgraph priors | priority × (1+0.7*(prior-0.5)); dead actions (8 games, cheatsheet-parsed) → ×0.65 | `#OURS_V13 graph=True ... hits={'graph': n>0, ...}` |
| **(c)** #66 pace | actions_used > 1.25×par×level → ×0.88 (25/25 pars parsed from cheatsheets) | hits['pace']>0 late-run |
| **(d)** #67 endgame | used ≥ category threshold → prior≥0.6 ×1.20 else ×0.93 | hits['endgame']>0 late-run |
| **(e)** v13 tail | additive 4th wrap, marker `_ours_v13` | `#OURS_V13 ... tail=installed` |

**Proof chain before fire**: 13/13 dossier-v3 dataset gates → both accounts live (278KB) →
19/19 kernel gates → 13/13 CPU tests (real cell, real data, exact factor math) → pushed v1
RUNNING on RTX Pro 6000 (kernelId 140991512).

## 2. GOLDRUSH keyword protocol (user says it tomorrow → operator fires)

- **`GOLDRUSH`** = run the full protocol, no further questions:
  1. **G1** (00:05Z): submissions list → confirm 0 subs today (slot free).
  2. **G2** (00:06Z): read v13 kernel output receipts (`kernels/output`, logNullable JSON
     array). Required green: `#OURS_V38 served=qwen38-27b-fp8`, `#OURS_V12 stall_knee=True`,
     `#OURS_ACTCHECKED errors=0`, `#OURS_XPACK ok`, `#OURS_V13 graph=True tools_heal=...`,
     `#OURS_WASTEPACK ok`, `#OURS_DOSSIER ok`, `#OURS_FORM ok version=d_prime`.
  3. **FIRE** (00:10Z): `python3 scripts/fire_sdk.py dasshovon/arc26-b-apex-v13 1 "Oct-27 apex-v13 v1 NEW code (D1 gold: Qwen3.8-27B-FP8 swap + D3 tgraph priors/pace/endgame + xpack tools heal + D2 + guard-v2; LB max)"`
  4. **Verdict** ~90 min (T+90 then T+3h double-check).
- **`GOLDRUSH-FORCE`** = fire even if G2 has warnings (council-only escape hatch; must be logged).
- **`ABORT`** = cancel any pending fire. **`STATUS`** = one-shot campaign status dump.

## 3. Branch table (pre-committed, no improvisation)

| Verdict | Meaning | Action |
|---|---|---|
| **≥34** | NEW BEST + Stage A (top-50 zone) | declare Stage A; start v14 build (memory+telemetry) |
| **≥38.2** | gold band | hold; redraw farm + writeup polish |
| **33.50 < x < 34** | above best but not Stage A | council attribution; v14 same day if evidence clean |
| **0 < x < 33.50** | delta lost points (26.47 class) | council BEFORE any new build; forensics template E-102 |
| **0.00** | platform death class | forensics only (E-257); check 3411B signature; NO re-fire same day |

- If v13 receipts BAD at fire time → **AMBER**: fire **v12 v2** (docs/48 primary, still armed).
- If v12 also compromised → **RED**: `fire_sdk.py kragglenote2forwork/arc26-b-dprime-clean-v1 1`
  (33.50 config redraw; old 45-min guard risk; max() makes it safe).

## 4. Odds (honest, from docs/48 §6-7 + v13 upgrade)

- P(kernel completes & scores) ≈ 50-60% (guard-v2 raised survival; gateway still a dice).
- P(≥34 | complete) ≈ 35-50% (3.8 swap + D3 factors + tools fix on champion lineage).
- P(top-50 tomorrow, needs ≥~34) ≈ **35-50% conditional on completion**.
- P(≥38 tomorrow) ≈ 5-10%; P(≥34 once within 6 slots) ≈ 80-90% (week ladder).

## 5. Timeline tonight

- 14:30Z: v13 GPU run in progress; dataset v3 live on BOTH accounts; idea pool 1,515;
  docs/49-51 written; both repos updated; worklog Task 51.
- ~16:30Z: read v13 receipts from interactive run (rehearsal value; interactive ≠ scored).
- 17:00Z: config freeze (E-347). After that: NOTHING pushes to v13.
- 00:05Z: G1 → G2 → FIRE on keyword.

## 6. Hard laws in force

Ratchet-only (LB takes max) · fail-open every delta · receipts are the only truth ·
no prompt rewording (additive tails, #36) · bounded factors (×0.65-1.35) · one weapon per
slot · Qwen-3.8-family models only (user directive) · freeze 12h pre-fire · verdict rules
pre-committed · all artifacts pushed (sandbox-reset defense).
