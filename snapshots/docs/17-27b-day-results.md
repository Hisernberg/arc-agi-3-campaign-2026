# 17 — 27B Day Results: Repro + R11/R11.1/R11.2 Ablation (2026-09-27/28)

## Setup
Account **dasshovon** became the submission account (user instruction). Three kernels run on
RTX Pro 6000, all on the LB-9 stack (anim bundle + wheelhouse v3 + Qwen3.8-27B-FP8):

| Kernel | Config | Internal mean | Actions | tok/action | Levels |
|---|---|---|---|---|---|
| `arc26-qwen3-8-27b-lb9-v1` (repro) | clean Duck v12 + 27B, no patches | **5.13** | 1476 | 1363 | 26 |
| `arc26-qwen38-27b-r11-uradfix` | + urad P-set ALL (P1–P20,P22; P21 off) | 2.23 | 567 | 4100 | 16 |
| `arc26-qwen38-27b-r111-hfix` | + harness-only subset (14 groups) | 1.95 | 779 | 3127 | — |
| `arc26-qwen38-27b-r112-ablate` | + subset minus P4+P6 (12 groups) | 2.45 | 1247 | ~1950 | — |

All 44/35/22 patches applied exactly-once on Kaggle, 0 tracebacks in all runs — the exact-text
patch machinery is solid; the REGRESSION is behavioral, not mechanical.

## Findings

1. **The urad P-set does not transfer to the 27B stack.** Three independent draws (full set,
   harness-only, harness-minus-P4/P6) all scored 1.95–2.45 vs the clean repro's 5.13. The set
   was tuned on the 8B NVFP4 stack (their internal 7.10); on the 27B wheelhouse stack it is
   net-negative in every configuration we tested.
2. **Action suppression is systematic**: tok/action went 1363 → 3127–4100 in patched runs.
   Any added prompt content (even harness-computed facts like P9 diffs) shifts Qwen3.8-27B's
   think/act balance. With per-turn wallclock budgets fixed, more thinking = fewer actions
   = fewer level completions (P4+P6 removal recovered actions to 1247 but not the score).
3. **Draw variance is huge and must be priced in**: same-code official draws for the 8B R10
   were 2.78/3.78/4.68. Single internal draws are weak evidence — but 3/3 patched draws below
   2.5 vs 1/1 clean at 5.13, plus the action-count collapse, is a consistent signal.
4. **The clean 27B repro is the best-known config for this account today** — official
   submission `56620520` (submitted 22:13 UTC 09-27, pending official rerun at write time).

## Submission policy applied
- R11 (2.23) and R11.1 (1.95) NOT submitted — protects the daily quota.
- R11.2 (2.45) NOT submitted for the same reason.
- Fresh-draw kernel `arc26-qwen38-27b-lb9-d2` (identical clean code) launched 06:13 UTC as
  the candidate for today's quota; submit on green health.

## Next levers (in EV order)
1. **More clean-repro draws** (variance ratchet; LB keeps the max) while the P-set issue is open.
2. **27B-aware fix design from scratch** — only *token-removing* mechanisms (nothing that adds
   prompt text): e.g. serving-side prefix caching ON + KV tuning for the 27B, P20 HUD detector
   ALONE (it only annotates tool results on no-impact actions), P2 UNDO naming ALONE (3 tokens).
   One mechanism per run, judged on tok/action first, score second.
3. **v8 APEX mechanisms** (built for the 8B duck bundle) would need the same one-at-a-time
   protocol — its WM_TOKCAP design law already anticipates this.
4. If the official score of 56620520 lands ≥ 6: keep ratcheting draws; if ≤ 3: pivot to
   serving-side optimization (prefix caching, KV 65GiB profile) which needs zero prompt changes.

## Infrastructure notes (repeatable submit recipe)
- Submit requires `kaggle competitions submit -f submission.parquet -k owner/slug -v N`
  (the `file_name` parameter is mandatory for CreateCodeSubmission; a missing one 400s).
- Sandbox watchdogs kill background watchers between tool calls → inline polling only.
- Slug normalization: title dots/dashes get rewritten ("qwen38" → "qwen3-8"); use the URL slug.
