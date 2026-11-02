# docs/20 — Qwen-AgentWorld & Agentic World Models × ARC-AGI-3: Proper Analysis

Date: 2026-09-30 · Task 14-c · Companion: docs/21 (MOAGS/MOAW architectures), docs/22 (updated plan)

## 0. TL;DR Verdict

| Question | Answer |
|---|---|
| Can agentic world models like Qwen-AgentWorld work in this competition? | **Yes, but not the naive way.** Zero-shot simulation fidelity on ARC gridworlds is unknown (domain shift); the high-EV path is **Mode C: ARC-native world-model LoRA** built on our 2M+ recorded transitions, with zero-shot Mode A as a free day-1 probe. |
| Can we use qwen 3.8 as the agentic world? | **Version 1 (Qwen3.8-27B dense): yes immediately** — deep-lane upgrade. **Version 2 (Qwen3.8-Flash-Next 125B-A6B): high-ceiling/high-risk** — NVFP4 fits 96GB, but `qwen4_exp` vLLM/SGLang support was still PR-stage at release (Aug 26). |
| Better/similar models? | Qwen-AgentWorld-35B-A3B itself (A3B active = 8B-class speed), Ornith-1.5-35B-A3B (same skeleton, policy-tuned), unsloth Qwen3.8-27B-NVFP4, nvidia/primitive-ai Flash-Next NVFP4. Full roster §6. |
| Does this change the path to top-3? | It upgrades docs/15 Phase 2 from "we should build a world model" to a **concrete recipe with an off-the-shelf foundation**. Efficiency-squared savings are the mechanism (§4). |

## 1. What Qwen-AgentWorld actually is (verified facts)

Source: HF card `Qwen/Qwen-AgentWorld-35B-A3B` (downloaded, in `research/`), arXiv:2606.24597 abstract, release 2026-06-25.

- **First native language world model** for agentic environment simulation: given an action + interaction history, it predicts the **next environment state** via long chain-of-thought. Environment modeling is the training objective from CPT onward — not a post-hoc prompt trick.
- **Three-stage training**: CPT (state-transition dynamics + professional corpora) → SFT (next-state-prediction reasoning) → RL (GSPO, hybrid rubric+rule rewards). Trained on **10M+ real environment trajectories**.
- **Two sizes**: 35B-A3B (fits us) and 397B-A17B (does not).
- **Seven domains**: MCP tool-calling, Search, Terminal, SWE, Android, Web, OS. Text + GUI (screenshots). **No game domain. No ARC. This is the central limitation.**
- **Architecture**: Qwen3_5MoeForConditionalGeneration on Qwen3.5-35B-A3B-Base; 256 experts / 8 routed + 1 shared active; Gated DeltaNet + Gated Attention hybrid layout (10×(3×DeltaNet→MoE)→1×Attn→MoE per 40 layers); hidden 2048; **context 262,144**; bf16 weights ≈ **34.7 GB**. Same MoE skeleton class as Ornith-1.5-35B-A3B, which we already validated for our stack (docs/14) → **low vLLM integration risk** (needs `--language-model-only` because the config declares visual modules that have no weights).
- **Quality signal**: AgentWorldBench overall 56.39 (35B-A3B) / 58.71 (397B-A17B) vs its own base Qwen3.5-35B-A3B 47.73 — i.e., the world-model recipe is worth **+8.7 points over base** and lands between Claude Sonnet 4.6 and GPT-5.4-class on their agentic rubric.
- **Two official usage paradigms** (paper): (1) **decoupled environment simulator** — generate synthetic/counterfactual rollouts to train or verify agents; (2) **unified agent FM** — world-model training as warm-up that transfers to downstream agentic performance.
- Claimed **zero-shot generalization to OOD environments** (e.g., OpenClaw). Note: OpenClaw is still a computer-use environment — OOD within-domain, not cross-domain into 2D gridworld games.

## 2. Why a world model matters HERE at all (the mechanism)

Our score is `min(human/agent, 1.15)²` per level — **wasted actions are punished quadratically**. r12 proved it: internal 5.19 → official 3.09 purely on the efficiency term. The engine is deterministic and free to *observe*, but every real action spent is scored forever within that level's run.

A world model adds a second, imaginary action channel:

1. **Action pre-filtering (efficiency shield).** Before committing ACTION_i in the real game, roll it out in imagination. Predicted outcomes: "nothing changes" (dead key press), "agent dies / softlock", "progress toward goal state". Only act when imagination predicts progress. If wasted actions drop by fraction *w* on a level where we used *a* actions vs human *h*, the efficiency factor improves directly — on action-heavy levels where a ≈ 2h, cutting wasted actions ~30% moves the per-level factor from 0.25 toward 0.3–0.45 territory. That is the difference between LB 4 and LB 10+.
2. **Look-ahead planning.** Beam k candidate action sequences in imagination 3–8 steps deep, score predicted frames against the goal prior (exit-open conditions), commit the best. This is Dreamer/MuZero logic transplanted to language world models, and it is exactly what "Reasoning with LLM is Planning with World Model" (RAPH) formalizes: LLM-as-world-model guides a reasoning tree, task-reward prunes it.
3. **Synthetic data for our own RL/SFT** (paper paradigm 1): imagination rollouts densify the 2M+ transitions we already recorded into counterfactual branches for training the ARC-native policy adapters (ericmao-style) without spending a single real action.
4. **Warm-start for the deep lane** (paper paradigm 2): if world-model LoRA training transfers, the same adapter can double as a policy warm-start — their +8.7-over-base result is the evidence.

**Honest counter-case (must be stated):** our games ship with the *actual* engine in-harness — a perfect, free, deterministic world model. What it cannot do: rewind, branch, or evaluate an action without committing it (no save/load; RESET costs real actions). So the learned world model's ONLY unique value is **non-destructive counterfactual branching** — branch, evaluate, discard. If imagination fidelity is <90% on 1-step transitions, the shield leaks (false "progress" predictions cause real wasted actions anyway; false "dead" predictions cause us to skip real wins). Hence §3's free offline test is the gate for everything else.

## 3. Test protocol — zero-shot fidelity probe (offline, free, day 1)

We hold **ground truth for every transition we ever played** (25 games' benchmark.json full trajectories + 53 verified playbooks; local arcengine ≡ scoring engine proven in r10 replay). No submissions needed:

1. Build 1,000 transition pairs `(frame_text_t, action) → frame_text_{t+1}` sampled stratified across 25 games × levels × outcome classes (no-op / move / death / level-up / key / door).
2. Serve `Qwen-AgentWorld-35B-A3B` (bf16, tp=1, ~35 GB) with a translated system prompt: "You are a language world model simulating a 2D grid puzzle game. Frames are text grids of object codes. Given the agent's action (ACTION1–ACTION6), predict the next frame grid and whether the agent died / level advanced."
3. Score next-frame exact-match, object-delta accuracy, and outcome-class accuracy (the last one is what the shield actually needs).
4. **Gates**: outcome-class accuracy ≥ 85% → Mode A shield viable as-is; 60–85% → build Mode C LoRA first; < 60% → skip to Mode C on the raw base (train dynamics from scratch on our traces; AgentWorld's CPT corpus may still help as initialization — A/B it).
5. Also probe **Qwen3.8-Flash-Next** and **Qwen3.8-27B** with the same prompt as zero-shot baselines — this *is* the "two versions of qwen 3.8 as agentic world" test, and it costs nothing beyond serving time.

Cost: one RTX PRO 6000 96GB session, ~2–3 h wall (35B-A3B at 3B active generates fast; 32K-token thinking outputs truncated to 4K for this probe — measure fidelity vs output length too).

## 4. Four integration modes (ranked by EV)

| Mode | What | Cost | EV | Verdict |
|---|---|---|---|---|
| **A. Zero-shot shield** | AgentWorld as action pre-filter / 1-step predictor (§3 prompt) | 1 day + 35 GB co-resident | Medium if gate passes; 0 if not | Run the probe; adopt only if ≥85% outcome accuracy |
| **B. AgentWorld-as-policy** | Its own benchmark shows agent FM capability near frontier; prompt it as the 27B-class deep-lane policy | 1 day | Low–medium — same unknowns as any zero-shot policy, but free to measure offline on recorded frames | Cheap experiment in the same session |
| **C. ARC-native world-model LoRA** ⭐ | Fine-tune (LoRA r=64) on our 2M+ transitions: input = frame_t + action, target = frame_{t+1} delta + outcome token. Base: AgentWorld-35B-A3B (inherits world-model CPT) vs Qwen3.5-35B-A3B-Base vs Qwen3.8-27B (dense ablation) | 3–5 days incl. training | **Highest — this builds the missing piece docs/15 Phase 2 named** | Primary build |
| **D. Synthetic rollout generator** | Use C's model to branch counterfactuals for policy-adapter training (ericmao recipe on our data) | rides on C | Medium — compounds with docs/19 Plan D | Phase 2+ |

Token-budget warning for A/C-inference: the model thinks in `<think>` blocks before emitting the predicted observation (card recommends 32K output tokens for full fidelity). For harness use we fine-tune/steer to ≤1–2K-token predictions; the probe measures exactly how much fidelity survives compression.

## 5. Serving fit on RTX PRO 6000 96 GB (our card)

- AgentWorld-35B-A3B bf16: 34.7 GB. AWQ-INT4 community quant (`cyankiwi`): ≈ 20 GB.
- Existing dual-lane: 8B NVFP4 ≈ 17 GB + 27B NVFP4 ≈ 16 GB.
- **Co-residency math**: 17 (8B lane) + 20 (AgentWorld AWQ) + 16 (27B lane) = 53 GB weights → ~35–40 GB left for KV across three vLLM instances at modest concurrency (8B: 8–12 workers; AgentWorld: 2–4; 27B: 2). Feasible but KV-tight — the 27B KV-collapse lesson (docs/17: ~199K-token cache budget per instance) says budget KV **before** adding the third instance; drop 27B to 1–2 workers when the world model is live.
- Alternative allocation: run AgentWorld as a *sidecar* only during decision points (not steady-state) and free it after — vLLM sleep/wake or a fourth lane toggled by env flag (our harnesses already do env-var switching).
- Flash-Next NVFP4 (nvidia or RadixArk): ≈ 55–65 GB weights → single-model-per-card; 6B active ≈ 8B-class speed with 125B-class quality. **This is the "one model to rule both lanes" endgame if `qwen4_exp` support lands** (SGLang draft PR was open Aug 26; re-check day 1 of next week).

## 6. Similar-or-better model roster for the agentic-world role (verified alive 2026-09-30)

| Model | Params / arch | Role fit | Notes |
|---|---|---|---|
| **Qwen/Qwen-AgentWorld-35B-A3B** | 35B-A3B MoE, Qwen3_5Moe | world model (the point of this doc) | bf16 34.7 GB; AWQ-INT4 available; GGUF/UD-Q8 by Brooooooklyn |
| **Qwen/Qwen3.8-27B** | 27B dense, Qwen3_5 | qwen3.8 v1: deep-lane policy + zero-shot world probe | NVFP4 by unsloth (2.68M dl); 27.8 GB bf16 |
| **Qwen/Qwen3.8-Flash-Next** | 125B-A6B MoE + 51B n-gram + 4B MTP, Qwen4Exp, VLM | qwen3.8 v2: dual-lane replacement; vision encoder could read raw frames | NVFP4: nvidia / RadixArk / Inferact / primitive-ai mixed-NVFP4-FP8; ⚠ serving-stack risk |
| **Ornith-1.5-35B-A3B** | 35B-A3B MoE (same skeleton) | fast policy lane upgrade over 8B | already vetted in docs/14 |
| **Qwen3.5-35B-A3B-Base** | base of AgentWorld | Mode-C control training if AgentWorld A/B loses | official weights |
| primitive-ai 8B mixed-NVFP4 / tcclaviger MXFP4-FP8 8B | 8B dense | fast-lane incumbents (checkpoint-rot replacements) | docs/19 day-1 blocker |
| ericmao arc-agi3-qwen36-human100 / spatial-continuation-100 | LoRA on Qwen3.6-27B | deep-lane policy adapters | **do not attach to Qwen3.8-27B** (different base) — need retrain if we switch |

Excluded: 397B-A17B (no fit), GLM/Kimi/DeepSeek (arch families outside our validated vLLM path — revisit only if Flash-Next support stalls).

## 7. Bottom line

Qwen-AgentWorld is not a drop-in winner — it has never seen a game grid. But it is (a) the first open, native language world model we can legally serve on our card, (b) a free day-1 probe against our recorded ground truth, and (c) the ideal skeleton for the ARC-native world model that docs/15 Phase 2 required us to build anyway. The two qwen 3.8 versions slot in as deep-lane upgrade (27B, low risk) and future single-lane endgame (Flash-Next, gated on serving support). Everything routes into the MOAGS/MOAW stack in docs/21.
