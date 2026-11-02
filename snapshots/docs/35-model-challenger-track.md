# 35 — MODEL CHALLENGER TRACK: external analysis reconciled, probed, and integrated

*Task 35, 2026-10-22. User supplied an external model-selection analysis (KV-headroom rubric,
challengers Sage-A1.5 / Muse Glimmer / Gemma-4-26B-A4B / Nemotron Bolt) and asked to analyze
the models for ARC-AGI-3. This doc: (1) fact-checks it against Kaggle metadata + our ledger,
(2) probes serving feasibility CPU-only, (3) integrates the survivors into the endgame
calendar. Raw probe: research/model_probe_1022/.*

## 1. Fact-check verdicts (external analysis vs ground truth)

| Claim | Verdict | Evidence |
|---|---|---|
| "Up to 5 submissions a day" | **FALSE** | Kaggle metadata `maxDailySubmissions=1`, `maxPendingSubmissionsPerTeam=1`; empirically **2/day team total** via dual accounts (n≥7 days accepted+scored). Challenger cadence = 1/day, not 3-in-2-days. |
| Team merge deadline Oct-26 | TRUE | `teamMergerExplicitDeadline=2026-10-26T23:59Z`. We already merged (team arc-needs-to-be-agi, #214d). |
| Submissions due Nov-2 | TRUE | `deadline=2026-11-02T23:59Z` (also our ledger #216). |
| Prizes need permissive license | REFINED | Official rule: **submitter-authored** code/methods → CC0/MIT-0; **third-party** code/weights → public-shareable open license (Apache-2.0, GPLv3 ok). Qwen community license passes as third-party. **Action: add MIT-0 LICENSE for our patches (we are the submitter).** |
| KV headroom is the binding constraint; rank models on it | **DOES NOT HOLD FOR US** | Incumbent Flash-Next = Gated DeltaNet ×36 (constant state) + QSA ×12 @ 2 KV heads × 256 dim → **~350 MB KV @57k FP8** on a 96 GB card. Sage-A1.5 = same hybrid-linear family (2 KV heads, ~260 MB). Memory is not binding for either. Rubric's 25% KV weight collapses in our comparison. |
| Vision helps (20% weight) | WEAKENED | NVIDIA AVO (95–100% closed track) fed **64×64 text grids, zero images**. Vision is one of two viable paths; our incumbent is itself a VLM but harness feeds text grids. Vision input stays a SEPARATE later lever — not part of a model swap. |
| "Qwen3.8-Flash-Next + Duck = only open stack near 69%" | CONTEXT | Tufa 68.91 runs the same harness family — our own lineage's demonstrated ceiling is ~+35 pts above our 33.50. Headroom is in config/tuning, which is why levers still beat model religion. |

## 2. CPU-only probe results (no GPU quota consumed)

Pinned runtime: vllm==0.19.0 + torch==2.10.0 + flashinfer==0.6.6 (#164). Method: registry.py
source inspection @ v0.19.0 tag + config.json fetches (research/model_probe_1022/).

| Model | vllm 0.19.0 | License | Vision | Verdict |
|---|---|---|---|---|
| **Sage-A1.5 35B-A3B** | ✅ `Qwen3_5MoeForConditionalGeneration` + MTP native | Apache-2.0 ✅ | ✅ | **CHALLENGER-1** |
| **Gemma-4-26B-A4B NVFP4** | ✅ `Gemma4ForConditionalGeneration` | nvidia repo Apache-2.0 (base Gemma terms nuance — verify) | ✅ | **CHALLENGER-2** |
| Muse Glimmer 30B | ❌ no Muse arch in 0.19.0 → runtime bump = 2nd lever | Apache-2.0 ✅ | ✅ | PARKED |
| Nemotron Bolt 74B-A9B | ⚠️ arch present, weights IQ2_XXS GGUF-first | nvidia open | ✅ | PARKED |

Key config numbers: Sage = 40 layers, kv_heads 2, head_dim 256, 3:1 linear:full; Gemma = 30
layers, kv_heads 8, 5:1 sliding:full, sw 1024, NVFP4 ~15.7 GiB. Both fit our card with the
drafter and 57k history trivially.

## 3. What actually differentiates Sage-A1.5 (Challenger-1) for OUR loop

Not memory. These:
1. **Verification mode** (opt-in self-review inside CoT via `chat_template_kwargs:
   {"verification": true}`) — directly attacks the **quadratic wasted-action penalty**
   (scoring `min(115, (human/agent actions)²×100)` per level; our throughput doctrine
   #203/204). A model that pauses to review unproductive paths wastes fewer actions.
2. **Agent-native post-training** (GAIA 95.1, subagent orchestration) — the Duck harness is
   a tool-REPL loop; action quality per token is the lever.
3. **Freshness** (Oct-21 release, trained for long-horizon tool work).
4. Integration notes (gates in build script): non-empty system message REQUIRED (HTTP 400
   otherwise — our kernel always sets one; assert in smoke); sampling defaults temp 1.0 /
   top_p 0.95 / top_k 20 / presence_penalty 1.5 (review env cell; presence_penalty 1.5 may
   interact with our prompt-surgery patches — base is CLEAN D-prime, minimal surgery, OK);
   Qwen3.6 base lineage = parser/template mechanics close to incumbent (lower integration
   risk, less diversity).

## 4. Endgame calendar (2/day proven cadence; A returns ~Oct-24)

| UTC day | B (dasshovon) | A (kragglenote) | Notes |
|---|---|---|---|
| Oct-23 | **CONTROL** dprime-recal-v1 (ARMED, fire_oct23.sh) | — | isolator for memsolve 0.00 |
| Oct-24 | **Sage challenger** (if COMPLETE) | **control** (paired read n=2) | build Oct-23 daytime; commit-run on B quota |
| Oct-25 | **Gemma challenger** | **incumbent baseline redraw** | paired same-day baseline for both challengers |
| Oct-26 | best-of config | challenger n=2 / baseline | **kernels publishing disabled 23:59** — fork parser notebooks BEFORE |
| Oct-27..29 | verdict-enforced iteration (zones pre-committed) | paired reads | mu n≥3 per surviving config |
| Oct-30/31 | **Phase-3 stack**: winner model + verified harness levers | same | code freeze Oct-31 |
| Nov-01 | final draws | final draws | select 2 final submissions (`numScoredSubmissions=2`) |
| Nov-02 23:59 | CLOSE | — | papers due Nov-08 (draft Oct-28, #219) |

**Challenger verdict rule (pre-registered):** a challenger is KEPT only if its same-day
paired read beats the incumbent baseline draw by **> 1.9** (noise floor #114) — same
instrument as all our verdicts; single-draw wins inside the floor do NOT count.

**Build gates for each challenger kernel (byte-gate standard #178 + W7 loud-fail):**
model path via dual-layout resolver (#166) → config/tokenizer attachment invariants (#168)
→ chat-template + processor swap → sampling env-cell review → compile + cell-position gates
→ MIT-0 LICENSE cell (compliance, section 1) → loud-fail marker (W7) → offline smoke
(RUN_FULL=false; no GPU-quota burn beyond one commit-run).

## 5. Pool additions (W41–W50)

- W41 [SWAP] Challenger-1 = Sage-A1.5 swap kernel (single lever: model+processor+template+sampling). Probe-passed.
- W42 [SWAP] Challenger-2 = Gemma-4-26B-A4B NVFP4 swap kernel. Probe-passed.
- W43 [GATE] Challenger verdict = same-day paired read > incumbent + 1.9 else reject.
- W44 [COMPLIANCE] MIT-0 LICENSE for submitter-authored code (patches/builds); third-party license audit cell in build gates.
- W45 [INTEL] `kernelsPublishingDisabled` Oct-26 23:59 → fork/clone all candidate parser notebooks (Glimmer/vLLM-0.28 parsers, DFlash drafter examples) BEFORE deadline.
- W46 [CORRECTION] KV-headroom criterion non-binding for our stack (incumbent ~350 MB KV @57k); memory-play thesis retired for us.
- W47 [EVIDENCE] AVO 64×64 text-grid path (95–100%) — vision input demoted to separate lever; text-grid harness stays primary.
- W48 [SAMPLING] Per-model sampling profile table (Sage: temp 1.0/top_p 0.95/top_k 20/presence 1.5) — env-cell lever, part of swap, documented per model.
- W49 [PARK] Glimmer (runtime bump) + Bolt (2-bit GGUF) parked with re-entry conditions (≥4 days left + both challengers fail).
- W50 [PAPER] Model-swap paired-read methodology joins the paper track (determinism + drift + throughput + swap protocol).

## 6. Ledger cross-refs

- Throughput doctrine #203/204 → wasted-action quadratic penalty → Sage verification mode rationale.
- Hidden-cost caution #189 → why challenger verdicts need same-day paired reads, not paper benchmarks.
- Byte-gate builds #178 + loud-fail W7 → challenger build gates unchanged.
- Noise floor #114 (1.9) → W43 verdict threshold.
- Fork window #155/177 → W45 Oct-26 fork deadline (NEW hard deadline, same date as merger).
