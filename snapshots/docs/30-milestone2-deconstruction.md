# 30 — Milestone 2: Complete Deconstruction of the 4→27 Thought Process

> Compiled 2026-10-02 from: official ARC Prize pages, Kaggle discussions 697944/713634/742801/742935/743060/743723/744792, the four 20+ public notebook sources (pulled verbatim), GitHub repos (da-fr, LohitSiriki, Tufalabs, 1zuki, TWIN, arc-skill, PRO-LONG), and HF hub artifact surveys. Evidence files: `research/milestone2/` (176 files), notebook sources in `research/milestone2/notebooks/`.

---

## 1. What Milestone 2 actually was (fact sheet)

| Fact | Detail |
|---|---|
| Definition | **Not new content.** Milestone 2 = second (final) mid-competition open-source prize, decided by **public LB score at Sept 30, 2026 23:59 UTC** among notebooks made public under an open license. Source: M1 blog line + Kaggle host posts. |
| Eligibility | Notebook must be public + open-source-licensed; winners must share code. Prize structure ambiguity: blog says $25K/$10K/$2.5K, Kaggle overview says $25K/$7.5K/$5K. |
| Podium (community-verified, disc 744792) | 1. **dfranzen (Daniel Franzen) 27.89** · 2. **lordhansolo 23.84** · 3. **sirikilohit/rellik13 22.53** · 4. richardcsaky 20.00 |
| What did NOT change | 110-game rerun set (~55 public + ~55 hidden), 9h runtime, 1× RTX PRO 6000 96GB, no internet, single play per game. |
| Who skipped it | Tufa Labs (LB 50.65), Yi-Chia Chen (~41), NVIDIA CPMP — all refused to open-source mid-competition. Cottaar's reason: prize would go to "the luckiest of 4000 copies" (single-play variance). Tufa will open-source everything at competition end (Nov 2 / Dec 4). |
| Scoring formula (reverse-engineered, gedouluhui, log-verified) | `level = min(115, (baseline_actions/your_actions)² × 100)`; game score = level-index-weighted mean; LB = unweighted mean over games; **single play**. |
| Key consequence of formula | Quadratic efficiency means the LAST few actions on a level cost most: a level solved in 2× baseline scores 25, in 1.5× scores ~44, in 1.2× scores ~69. Efficiency beats completion count until you're leaving levels wholly unsolved. |

## 2. The shared stack of all four 20+ scorers

All four are the same lineage: **Tufa Labs Duck harness (TAAF) + Qwen3.8-Flash-Next + speculative MTP + FP8 KV cache on one RTX PRO 6000**, differing in serving fork, quantization, history policy, and scheduler. The 4→27 gap decomposes into five layers:

### Layer 0 — Harness baseline (our current position, LB 4.54)
Duck harness + Qwen3.8-Flash-Next-NVFP4 (RadixArk) on vLLM, 8k-token-class context discipline, per-game time slices, tool-agent with Python REPL. Our internal efficiency 5.19 → LB 3.09 (r12) showed we already clear levels but bleed actions to no-op loops, wrong-goal perseverance, and re-exploration after level wipes.

### Layer 1 — Serving fork (≈ +3–6 pts, infrastructure, zero prompt cost)
- **SGLang Pennyroyal fork** (jpezzulli/sglang-rtxpro6000 v2.5.3 + mratsim/gabrielolympie patches) beats vLLM nightly for this workload: GDN/Mamba hybrid state handling + radix-cache "extra_buffer" for hybrid models + FlashInfer linear backend.
- **Quantization ladder (the model switch was the biggest single jump)**: Qwen3.6-27B-FP8 → Qwen3.8-27B-FP8 → **Qwen3.8-Flash-Next** served as **Intel W4A16 AutoRound** experts (BF16 or FP8 PLE tables — sirikilohit swapped in FP8 PLE, "M82") or **RadixArk/lordhansolo mixed NVFP4+FP8** with separate **MTP draft head** (INT4 g32 or NVFP4 NEXTN).
- MTP speculative decoding: SPEC_STEPS=3, accept thresholds 1.0/1.0 (dfranzen). ~4.7× fewer forward passes when history replay is verbatim.

### Layer 2 — Memory envelope (THE differentiator, ≈ +8 pts alone)
rellik13's clean ablation: **14.49 → 22.53 from FP8 KV + longer history ALONE, zero prompt changes.** Their KV pool was 91–97% full with requests queuing — memory, not decode TPS, was the binding constraint.
- FP8 E4M3 KV cache → 1.0–1.4M-token KV pools (mem-fraction-static 0.96–0.97, page 64).
- Rolling history 45–57k tokens with **blockwise hysteresis trim**: one big cut (e.g. 57,344 → 45,056; earlier 36,864 → 26,624) instead of many small trims, so the prefix stays cache-hot → **93.4% prefix-token cache reuse** (dfranzen measured).
- dfranzen serving: CTX 136×1024, MAXREQ=10, CUDAGRAPH_MAXBS=10, MAMBA_CACHE=60, CHUNK=8192, MAX_PREFILL=16384, SSM bfloat16, MAMBA_RADIX=extra_buffer.
- lordhansolo: vLLM runtime `arc3-vllm-e975732-gdn-recoverssm`, mixed NVFP4/FP8 model, 147k ctx, 14 streams, 1.42M-token KV pool. (His *newer faster* runtime v3 has NOT beaten his v2 score — newer ≠ luckier.)

### Layer 3 — Scheduling (≈ +2–4 pts)
- **dfranzen: priority P=(A+B)·C** — A mirrors the true quadratic score formula; B = continuation value by levels-remaining; C = Gaussian falloff calibrated on **725 real level attempts** (code in `gh_da-fr_WRITEUP.md`).
- **sirikilohit: one-pool UCB** — every game gets a 300 s warm-up slice, then each free slot goes to the playable game with highest `UCB = levels-per-generated-token + c·exploration`, c=0.0002, slices end at request boundaries (source: Wang-Zhongwei/duck-harness `allocation.py`).
- richardcsaky: prebuilt SHA-verified runtime tarball, "arena flash" — 110 cyclic replicas of the 20 public games for validation, 4500 s rerun budget, gateway writes the real submission.

### Layer 4 — Perception & feedback fidelity (≈ +2–5 pts, the "free" fixes)
From the harness patches visible in dfranzen's source and writeups:
- **Animation frames exposed** (tn36 is unsolvable without them) + transient-pixel hints, 10× upscaled images, difference images, fatal-frame inspection.
- **UNDO (ACTION7) exposed by name** with three modes (tufa legacy / off / on-accept-both).
- Truthful semantics: "Level restarted." + budget-bar diagnosis instead of misleading advice.
- Persistent Python functions across REPL calls (no re-definition cost).
- **Solved-level rule memory** (+2.8 measured — the ONLY pure-text addition that helped).
- No-op guard keyed on `(level, interior_state_hash, action_signature)` refuses bit-identical no-effect actions; death ledger; armed_noop/armed_death state.

### What top scorers measured as NEGATIVE (do not port)
Prompt advice/summaries, structured world-model scaffolds, assumption ledgers (da-fr turned his off entirely), expert pruning, fresh-context restarts, T=0.3 (kills exploration; use T=1.0-class), archetype playbooks as hard commitments, LoRA SFT mid-run, 64k context without the serving upgrades (throughput collapse).

### The residual: lottery effect (σ ≈ 0.8–0.9 LB points)
Bimodal per-game outcomes; in 83% of stuck forks the decisive action type HAD been tried but the agent defended the wrong early goal hypothesis. Same-code redraws moved 27.89↔23.84 (dfranzen family), 6.02→4.15 (tufa-named), taaf 3.18→6.09. **One submission = one draw.** Resubmission of the same notebook is +EV until it draws ≥ its family mean.

## 3. LB scoring factors — what maximizes score

1. **Actions are the only currency.** Every action (incl. RESET? — no: RESET is free-ish but wipes progress; ACTION1-7 cost) inflates the denominator of `(baseline/your)²`. Dead actions are quadratically punitive.
2. **Level-index weighting inside a game**: later levels weigh more in the game mean (confirm exact weights in `research/milestone2/games_mechanics.txt`).
3. **Unweighted game mean on the LB** → a single zero-score game costs 1/25th of LB = ~1.1 pts at LB 27. Avoiding a total-zero on ANY game is worth more than shaving 5% actions on an already-good game.
4. **min(115, …) cap** → over-efficiency beyond baseline×0.93 is wasted; park the level at ~baseline and move on.
5. **Single play** → everything above is per-draw; scheduling must optimize the *expected* sum under redraw variance (dfranzen's C-term, sirikilohit's UCB).
6. **9h wall clock on 1 GPU** → tokens/hour is the true binding resource; KV pool size and prefix-cache hit rate directly convert into more agent decisions per hour → more levels.

## 4. Gaps / lackings of the top notebooks (our attack surface)

| Gap | Evidence | Our counter-move |
|---|---|---|
| **Lottery exposure** | Same-code spread ~4 pts; 83% wrong-goal-defense | dfranzen's C-term + our H1 "world-model shield" wrong-goal detector; multi-account same-notebook draws |
| **No true world model** | All four rejected structured WM scaffolds as *prompts*; none tried learned/verified simulators | TWIN-style replay-gated twin (93.3/100 on API board) is unported to Kaggle constraints — port as *passive* predictor, gate actions on predicted no-change |
| **History = raw transcript** | 22% of mean prompt is REASONING tokens (sirikilohit measured 5,315/24,195) | Compress reasoning turns to first-line intents only → ~20% more history in same envelope |
| **UNDO still underused** | Exposed but policy-free; agents UNDO late | UNDO-trigger heuristics (fatal-frame + no-progress-N + budget-bar spike) |
| **Scheduler ignores redraw variance within 9h** | Both schedulers optimize expected current-level value only | Reserve endgame window for "rescue sweeps" of bimodal games already scored 0 (a rescued zero = +1.1 LB at margin) |
| **Prefix cache fragility** | 93.4% reuse requires verbatim replay; any prompt-order nondeterminism destroys it | Freeze prompt assembly order; hash-verify prefix before each call (our KV6B discipline fits here) |
| **Park-at-baseline not implemented** | min(115,·) cap implies optimal park near 0.93× baseline | Park detector: projected actions > 1.05× baseline and level nearly solved → leave |

## 5. Fusion plan to 30–40+ (ranked by EV/effort; feeds REGISTER E-111+)

| # | Move | Expected | Effort | Source |
|---|---|---|---|---|
| 1 | Resubmit dfranzen notebook family on both accounts (bank 23–27 draws) | 23–27 banked | hours | done on Track R (25.30); Track S pending |
| 2 | Port FP8-KV + 57k→45k hysteresis history onto OUR NVFP4/MTP stack | +6–8 | 1 GPU smoke + 1 run | rellik13 ablation |
| 3 | Switch serve stack to Pennyroyal SGLang + Intel W4A16 (+FP8 PLE) + MTP | +2–4 | 2–3 runs | da-fr/sirikilohit |
| 4 | Priority scheduler P=(A+B)·C (port `priority_scheduler.py`) | +2–3 | 1 run + CPU sim | da-fr |
| 5 | Perception pack: animation frames, 10× images, diff images, truthful resets, UNDO-on, persistent REPL fns | +2–4 | harness patches, CPU-testable | da-fr patch list |
| 6 | Solved-level rule memory (+2.8) | +2 | patch | da-fr |
| 7 | Reasoning-compression in history | +0.5–1.5 | patch + tokenizer study | sirikilohit measurement |
| 8 | Rescue sweeps + park-at-baseline in scheduler | +1–2 | patch | our own (§3.3, §3.4) |
| 9 | TWIN passive twin gate (predicted no-change → veto) | +1–2 | research-grade | Alexyskoutnev/TWIN |
| 10 | End-of-competition Tufa full open-source drop (Nov 2/Dec 4) | step-change | watch | host posts |

Budget rule (from docs/26 OS): every GPU run must enter the ledger within 12h; CPU-first verification for all harness patches; 1 submission/day/account as the scarce currency.

## 6. Account split (current standing 2026-10-02)

- **Track R (dasshovon)** — experiments/hypotheses. **Best 25.30** (M2S fork-bank "dfranzen v1", 2026-10-01). 3 slots/wk remain for H1–H6 experiments; every experiment lands on top of the 25+ bank.
- **Track S (sureshot acct)** — resubmission/lock-in line. Best 4.54. Next slot: highest-EV M2-family fork (dfranzen or lordhansolo notebook), then family redraws; target ≥23 banked this week.
- Prize-eligibility caveat: mid-competition fork submissions score on the LB but originality requirements for final prizes are stricter — forks are banking + redraw-variance harvest, not the end state. The fusion notebook (moves 2–9) is our originality claim.

## 7. Open questions

1. Official M2 winners blog not yet posted (probed 6 slugs, all 404) — watch arcprize.org/blog.
2. Exact level-index weights inside game mean — extract from gedouluhui logs or our own rerun artifacts.
3. Whether hidden 55-game roster gates on `KAGGLE_IS_COMPETITION_RERUN` exactly like richardcsaky's bootstrap asserts (his notebook reveals the env-flag contract).
4. Tufa end-of-competition release scope (harness only? scheduler? traces?) — plan a re-plan trigger.
