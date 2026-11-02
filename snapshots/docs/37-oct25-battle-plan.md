# 37 — OCT-25 BATTLE PLAN: CH1 Qwen3.5 challenger day + anchor verdict ladder

*Task 38, 2026-10-24 (session: 10:19–11:05 UTC). User directive: "plan for tomorrow with
best possible ideas and models top open source as we discussed and plan to submit and
setup everything on kragglenote2 account today, with best open source work and ideas and
everything {new code, notebook, model etc} and submit best work, possible if any slots
today or tomorrow, and use new ideas and codes and public notebooks."*

---

## 1. What this session did (Oct-24, 10:19–11:05 UTC)

**Sandbox rebuilt from GitHub recovery layer.** The October container was gone; the
campaign repo (165 commits, e7763bd → d8956a4) was recovered via fresh credentials.
Kaggle token verified as `kragglenote2forwork` (kernel push landed there). GitHub token
live (pushes work). ARC hosted API key stale (401, non-blocking — Kaggle-internal runs).

**Live state audited (REST):** today's 6 submissions (57584929/57585952/57586479/57587298/
57588966/57589586) all `error`, zero batch-recovery scores yet; NO pending submission;
both lane kernels `COMPLETE` (`dasshovon/arc26-b-dprime-fix-v1` v3 = hardened anchor,
`kragglenote2forwork/arc26-a-dprime-fix-v1` = paired anchor). Old B-lane token still valid.

**Attempt 7 armed (fire at 11:30Z).** `scripts/fire_retry_oct24_a7.py` — gates G1
(kernel COMPLETE) + G2 (commit-log verify: gateway=False, RUN_FULL=False commit signature,
[diag:F-1024] JSON, placeholder written) already **PASS** at 10:33Z; G3 = 60-min cooldown
after attempt-6 error; G4 slot check (no pending, today's rows all error ⇒ allowance
frees) runs at fire time; CreateCodeSubmission v3 + 2 h poll, results to
`reports/oct24_draw_a7.json`.

## 2. kragglenote2 setup — DONE today (new code + notebook + model)

| Artifact | Ref | State |
|---|---|---|
| **CH1 model challenger** | `kragglenote2forwork/arc26-a-ch1-qwen35-v1` v1 | PUSHED, commit queued on A's fresh 30 h quota |
| Y22 fork: Glimmer+DFlash2 parser | `arc26-fork-glimmer-dflash2` | PUSHED (CPU, private) |
| Y22 fork: LB-9 27B config | `arc26-fork-lb9-27b` | PUSHED |
| Y22 fork: NVFP4 MTP harness | `arc26-fork-nvfp4-mtp` | PUSHED |
| Y22 fork: Tufa June-30 winner | `arc26-fork-tufa-june30` | PUSHED |
| Y22 fork: S12b variant | `arc26-fork-s12b` | PUSHED |

Y22 was due before **Oct-26 23:59** (kernelsPublishingDisabled) — done 2 days early.
Y21 MIT-0 LICENSE + third-party audit cell is embedded in the CH1 build and becomes the
standard build-gate for every future kernel (incl. finals).

## 3. THE MODEL TRACK — what "top open source" resolved to (evidence, not vibes)

The discussed challengers were probed against **what can actually mount on Kaggle**:

- **Sage-A1.5 35B-A3B → BLOCKED.** `InternScience/Sage-A1.5` absent from Kaggle Models
  AND Datasets (API search empty ×2, no dfranzen pack). vllm-native per docs/35 but
  weights cannot reach the offline kernel. Revisit trigger: a Kaggle-hosted pack appears.
- **Gemma-4-26B-A4B → BLOCKED.** Only community GGUF (llkh0a Q4_K_M) / MLX packs;
  official NVFP4 absent; GGUF cannot serve on Pennyroyal SGLang.
- **CH1 = Qwen3.5-27B-FP8 → GO.** Dataset `eliork/qwen3-5-27b-fp8` (25.3 GB) mounts
  directly. Feasibility chain, all CPU-verified today:
  1. dataset `config.json` architectures == `Qwen3_5ForConditionalGeneration`;
  2. Pennyroyal SGLang fork `qwen3_5.py:2564` EntryClass **exact match**;
  3. same hybrid-linear family as the incumbent (`full_attention_interval=4`,
     GDN-style linear attention, `attn_output_gate`) ⇒ stack's mamba/linear-attn
     flags stay valid — minimal serving surgery;
  4. KV budget: 16 full-attn layers × 4 kv-heads × 256 head_dim ≈ 32 KB/token FP8
     ⇒ ~1.9 GB/seq @57k, ~19 GB @10 streams — fits 96 GB with headroom;
  5. `max_position_embeddings` 262,144 > CTX 139,264;
  6. block-FP8 (128×128, dynamic activation) supported by the fork's fp8.py.
- **NEW lever discovered:** `qwen3_5_mtp.py` in the fork = **native MTP drafter for
  Qwen3.5** — a spec-decode lever for CH1's own family, parked until CH1 verdicts.

**Build discipline held:** single lever (model+quant+served-name only), drafter OFF
(`SPEC=False, FRSPEC=False`), sampling env unchanged, F-1024 fail-open guard + diag
canary inherited, F-1026 lesson generalized into a **fingerprint resolver** (finds the
model root by `model_type==qwen3_5` if the mount layout shifts again), Y29 byte-gate
**PASS** (harness-patch cell md5 `d8dce0d88c5c` — harness untouched), 14/14 build gates
PASS (raw-source checking, after fixing a JSON-escaping false-negative in the checker).

## 4. Oct-25, day by day (all times UTC)

**Standing:** team allowance 1/day; error frees, pending blocks; no fire without its
pre-registered read; verdict ≤1 h after score lands; drift-adjusted mu is the only metric
(clean-dprime slope −0.63/day, noise floor ±1.9).

| Time | Lane | Action |
|---|---|---|
| 00:00Z | escalation | **If attempt 7 also errored: Y25 forum post goes up** — evidence chain (6 kernels-attempts incl. bare-CPU probe, zero rerun logs, mount audit clean, staff queue-crunch pattern match). Template pre-drafted in §6. |
| morning | watch | Poll attempt-7 ref (fire_retry log) + all 6 errored refs for **batch-recovery retro scores** (staff-documented behavior). Poll CH1 commit status (queued → running → complete; 6–9 h from queue). |
| on anchor read | verdict ladder | **≥24** ⇒ base re-anchored ⇒ **fire CH1** (the anchor IS the same-day incumbent baseline; A lane carries the challenger kernel already) ⇒ challenger verdict rule: keep only if > baseline + 1.9. **19–23** ⇒ band re-bench first (1 clean-dprime redraw, B lane) ⇒ CH1 the day after. **<2.45 / 0.00** ⇒ read [diag:F-1024] from the rerun log FIRST, hold all fires, escalate. **error** ⇒ retry protocol (60–120 min cooldown, no blind resubmits). |
| on CH1 commit | forensics | **COMPLETE** ⇒ verify log: `[paths] qwen3.5 root`, guard line, diag JSON, server health; build CH1-v2 with MTP drafter ONLY if CH1 v1 read promotes. **ERROR** ⇒ forensics into `artifacts/daily/2026-10-25/`, decide: fixable-in-one-cycle (fix + re-push on A) vs park CH1 (SGLang↦Qwen3.5 serving bug = paper-track finding). |
| evening | prep | Y7 offline expect= chamber (CPU, free): replay the 16 recorded traces, measure whether expect=-mismatch separates solved/failed levels — prices the B46 lever BEFORE Oct-28. Kill: AUC < 0.6 ⇒ B46 never ships. |
| night | freeze | Retry protocol continues automatically if platform still broken; do NOT stack fires; do NOT touch finals kernels. |

**Freeze calendar unchanged:** Oct-26 fork deadline (DONE), Oct-29 best-of, Oct-30/31
Phase-3 stack + code freeze, Nov-01 both finalists submitted, Nov-02 23:59 close.

## 5. Slot & quota ledger (post-session)

- Team: ~9 scored-slot-days left (Oct-25..Nov-02). Verdict-bearing requirement stands.
- A (kragglenote2): fresh 30 h; CH1 commit will consume ~6–9 h; paired-anchor kernel
  already COMPLETE (no new commit needed for a paired read).
- B (dasshovon): anchor v3 COMPLETE (no new commit needed); quota alive for reruns.
- Worst-case both-dry guard: finals stacks must be pushed+COMPLETE by Oct-30 (R1).

## 6. Y25 forum escalation draft (post only if attempt 7 errors)

> Title: Scoring reruns system-erroring pre-notebook since Oct-24 06:20 UTC (7 attempts,
> 4 kernels, incl. a bare-CPU placeholder — zero rerun logs)
>
> Body: competition arc-prize-2026-arc-agi-3, team arc-needs-to-be-agi. Since 06:20 UTC
> Oct-24, every submission rerun errors with "system error" before notebook execution:
> refs 57584929, 57585952, 57586479, 57587298, 57588966, 57589586 (+attempt 7). Four
> distinct kernels, including a no-dataset, no-GPU, placeholder-only CPU kernel
> (arc26-rerun-probe-v1) — our code cannot be the cause; `kernels/output` shows clean
> commit runs and NO rerun logs (our kernels always log, even on 23 s placeholder exits —
> cf. Oct-22/23 F-1024 forensics). This matches the queue-crunch pattern staff described
> (submissions marked Kaggle Error even when they ran; batch recovery re-scores). Two
> asks: (1) confirm the rerun pipeline status for this comp; (2) confirm errored
> submissions will be batch-recovered + retroactively scored, or whether we should keep
> resubmitting (allowance frees on each error, so cadence is free on our side). Evidence
> pack: commit logs + probe kernel + mount audit available on request.

## 7. Ledger cross-refs

- ev_tracker: Sage/Gemma → BLOCKED (evidence recorded); **CH1 Qwen3.5-27B-FP8 → BUILT+PUSHED**;
  **Qwen3.5 native MTP → PARKED (new lever, fork-probe discovery)**.
- Artifacts: `artifacts/daily/2026-10-24/push_a_ch1_qwen35/` (notebook + metadata),
  `artifacts/forks/y22/` (5 forks), `reports/oct24_draw_a7.json` (attempt-7 draw),
  `scripts/build_ch1_qwen35_v1.py`, `scripts/fire_retry_oct24_a7.py`.
- F-chain: F-1024 (guard) → F-1025 (gateway) → F-1026 (wheelhouse) → F-1028 (rerun
  pipeline) — attempt 7 is the first fire with ALL THREE breakers fixed + verify-gated.

---

## 8. SESSION ADDENDUM (Oct-24 13:35Z): F-1029 discovered — CH1 commit blocked; Y19 fallback armed

**F-1029 (new platform failure class): `eliork/qwen3-5-27b-fp8` + competition-source
co-attachment dies pre-notebook with an EMPTY log.** 5 repros (CH1 v1/v2/v3 commits,
probe v5, probe v11). 10-probe bisection (`arc26-a-qwen35-mount-probe-v1` v1–v11, ~zero
quota burn) isolated it: GPU pipeline OK; docker pin + machine_shape OK; every attachment
OK alone; both datasets OK together; B-kernel attachment set (pennyroyal+taaf+competition)
OK; 38 GB without competition OK. Only eliork+competition kills. Not our code.

**Consequences:**
1. CH1 (any version) cannot COMMIT while F-1029 holds — and firing it would hit the same
   mount path in reruns. CH1 lane = parked, watch for platform heal (probe push per session).
2. The fallback challenger on the PROVEN healthy attachment set = **Y19 sampling A/B**
   (`arc26-b-sample-heat-v1`, temp 0.7→1.0 single env delta, 9/9 gates, Y29 parity) —
   **BUILT, verdict-gated: push to dasshovon ONLY after the anchor verdict ≥ 24**; fire
   Oct-25/26 with the anchor as the same-day baseline; keep only if > baseline + 1.9.
3. The Oct-25 verdict-ladder watcher is LIVE (`scripts/fire_oct25_ch1.py`, log
   `artifacts/daily/2026-10-25/fire_ch1.log`): polls the newest pending/complete
   dprime-fix submission; on score ≥ 24 → gate-checks CH1 (will loud-HALT while F-1029
   holds → next session pushes Y19 instead per §4 ladder, CH1 when healed).

**Oct-25 morning decision tree (replaces §4 rows where they conflict):**
- anchor ≥ 24 → push Y19 (B lane) + if F-1029 healed (probe push runs) also push CH1 v4
  (A lane) → both fire next 48 h as paired reads. CH1 > Y19 in fire priority once unblocked.
- anchor 19–23 → council, re-bench day, no lever fires.
- anchor error / 0.00 → retry protocol / diag-first; Y25 forum post at 00:00Z (§6 draft).
- Attempt 8 (ref 57594680) has been PENDING since 12:45:03Z — past the ~40 min historical
  death window ⇒ the rerun may be executing; score ETA ~19:00–22:00Z.
