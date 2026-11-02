# docs/22 — Updated Master Plan (v4): World-Model Stack, qwen3.8 Dual Test, Evaluation Matrix

Date: 2026-09-30 · Task 14-e · Supersedes ordering in docs/19 (Plans A–E remain valid; this doc adds Plans F–H and re-prioritizes)

## 0. Context recap (what changed since docs/19)

1. docs/20 established Qwen-AgentWorld-35B-A3B as a viable world-model foundation and named the free offline probe that gates everything.
2. docs/21 defined MOAGS / MOA / MOAW — the system-level stack that converts "harness > model" (the 2026 lesson, docs/12) into concrete components.
3. qwen 3.8 resolved into **two distinct versions** that must be tested separately (§2).
4. Standing constraints unchanged: 1 sub/day, submission deadline 2026-11-02, LB #1 Tufa Labs 45.33, our official best 4.07 (41 levels), incumbent fast-lane checkpoint is **dead** (checkpoint-rot) → day-1 swap mandatory, ARC API key still expired (local engine is our environment).

## 1. Plan lineup (A–E from docs/19 unchanged in substance)

- **A — Playbooks + governor + 2×-human efficiency cap** → LB 7–12. (No regression; day-1 priority with the checkpoint swap.)
- **B — Two-lane swarm** (8B fast + 27B deep) → +3–8.
- **C — Algorithmic solvers** (tr87/su15/ls20/sb26 mechanisms) → +2–5, feeds MOAGS S2.
- **D — Deep capability** (LoRA/skills/JEPA on deep lane) → Phase 2.
- **E — Ops discipline** (gates, anonymity, quota) — continuous.
- **NEW F — Agentic world model line** (Qwen-AgentWorld probe → Mode C LoRA) — §3.
- **NEW G — MOAGS router** (formalize S1–S5 + learned gating) — §4.
- **NEW H — MOAW verifier + MOA proposal layer** — §4.

## 2. qwen 3.8 dual-version test protocol (user directive, both versions)

**Version 1 — Qwen3.8-27B (dense, 27.8 GB bf16, `unsloth/Qwen3.8-27B-NVFP4`).**
- Role: deep-lane policy upgrade (replaces Qwen3.6-27B lineage) **and** zero-shot world-model baseline in the docs/20 §3 probe.
- Test matrix: (a) serving smoke on NVFP4 tp=1; (b) offline action-accuracy on 1,000 recorded decision points vs incumbent 27B draw; (c) world-probe outcome accuracy; (d) if (b) wins → one submission with it in S4.
- ⚠ ericmao adapters do NOT attach (base mismatch) — run clean; queue an adapter retrain only if (b) shows headroom.
- Cost: 0.5 day + 0–1 submission. Risk: LOW (same arch family as current deep lane).

**Version 2 — Qwen3.8-Flash-Next (125B-A6B MoE, Qwen4Exp, 180 GB bf16; NVFP4 ≈ 55–65 GB).**
- Role: potential single-model replacement of BOTH lanes (6B active ≈ 8B-class speed, 125B-class quality, vision encoder could read raw frames).
- Test matrix: (a) **serving-stack check first** — `qwen4_exp` support was PR-stage on Aug 26 (SGLang draft PR; vLLM fork needed on some platforms). Pin a version that imports the arch before touching weights. (b) NVFP4 load on 96 GB + KV budget check. (c) offline decision-point accuracy vs Version 1 and vs 8B incumbent. (d) only if (a)–(c) pass: one gated submission.
- Cost: 0.5–1 day. Risk: MEDIUM-HIGH (arch support, KV room). Payoff: highest single-model ceiling we have access to.
- **Similar-model roster** (docs/20 §6) stays the fallback: Ornith-1.5-35B-A3B for a fast lane upgrade, primitive-ai/tcclaviger 8B for the mandatory day-1 swap.

## 3. Plan F — world model line (the new spine)

| Step | What | Gate | Days |
|---|---|---|---|
| F1 | Zero-shot fidelity probe (docs/20 §3): AgentWorld-35B-A3B + both qwen 3.8 versions as baselines, 1,000 recorded transitions | outcome-class acc ≥85% → adopt W1; 60–85% → F2; <60% → F2 on raw base | 1 |
| F2 | Mode-C ARC-native world LoRA (r=64) on 2M+ transitions; base A/B: AgentWorld vs Qwen3.5-35B-A3B-Base vs Qwen3.8-27B | 1-step outcome acc ≥90%, object-delta ≥75% | 3–5 |
| F3 | MOAW sidecar live in harness behind env flag; W3 tabular memory from append-only log | local ls20/tr87 replay smoke: zero wasted-action regressions | 1–2 |
| F4 | Synthetic rollout generation for policy-adapter training (paradigm 1) | adapter ≥ incumbent on offline eval | 2–3, rides on F2 |

## 4. Plans G+H — MOAGS router then MOA/MOAW (phased, each gated)

- **G (MOAGS-lite, 1 day):** wire existing switches (playbook mode, lane selection, governor) into a scored router with hand-weights + per-game leaderboard features. No VRAM change. Gate: local replay of all 25 games shows no regression vs incumbent policy selection.
- **G2 (learned router, 2 days):** train the bandit offline on recorded transitions; deploy behind env var. Gate: ≥+5% simulated action efficiency on held-out games.
- **H (MOA + MOAW, 2–3 days after F3):** decision-point proposal fan-out + vote + MOAW verification per docs/21 §2–3. Gate: offline counterfactual eval — replay recorded decision points, verify the stack would have spent ≥25% fewer wasted actions without missing any recorded win.

## 5. Next-week schedule (Oct 1–7, integrated with docs/19)

| Day | Main track (submission slot) | Parallel track (offline, no slot) |
|---|---|---|
| Oct 1 | **Checkpoint swap** (primitive-ai 8B NVFP4) + Plan A resubmit — unblocks quota | Flash-Next serving-stack check (F-qwen3.8-v2a) |
| Oct 2 | Best-of A/B variant | **F1 probe** (AgentWorld + qwen3.8 v1 + v2 zero-shot) |
| Oct 3 | Plan C algorithmic solver submission (tr87/ls20 exact) | F2 LoRA training start (GPU session 1) |
| Oct 4 | Plan A governor v2 | F2 continues; G MOAGS-lite wiring |
| Oct 5 | Best combined submission (A+C) | F3 MOAW sidecar smoke; G2 router training |
| Oct 6 | qwen3.8-27B v1 deep-lane submission (if offline win) | H MOA+MOAW build |
| Oct 7 | Full-stack candidate or F3-assisted Plan A' | F4 start; buffer for gates |

Go/no-go: each row's parallel track must pass its gate before its harness component ships; any two failed gates in the main track → freeze features, submit incumbent-best (E discipline).

## 6. Plan evaluation matrix (user directive: "evaluate plan")

Scores 1–5; EV = expected LB points by Nov 2; ρ = risk of burning submission slots.

| Plan | EV | Cost (days) | ρ | Deadline fit | Compounds with | Verdict |
|---|---|---|---|---|---|---|
| A playbooks+governor | 3–5 | 1 | low | ★★★★★ | everything | **RUN now** (day-1 with swap) |
| B two-lane swarm | 3–8 | 1 | low | ★★★★★ | A, C | RUN (incumbent) |
| C algo solvers | 2–5 | 2 | low | ★★★★☆ | MOAGS S2 | RUN |
| D deep LoRA/skills | 5–15 | 4–6 | med | ★★★☆☆ | F4 | QUEUED after F2 |
| E ops discipline | protects all | 0.2 | – | ★★★★★ | – | CONTINUOUS |
| **F world-model line** | **3–8 (shield), unlocks 70–90-level Phase 2** | 5–8 | med | ★★★★☆ | B, D, G, H | **NEW SPINE — start F1 day 2** |
| **G MOAGS** | 1–3 | 1–3 | low-med | ★★★★★ | A, B, C | RUN (lite immediately) |
| **H MOA+MOAW** | **3–8** | 2–3 | med | ★★★★☆ | F | GATED on F1/F2 fidelity |
| qwen3.8 v1 (27B) test | 0–2 | 0.5 | low | ★★★★★ | B | RUN (cheap) |
| qwen3.8 v2 (Flash-Next) test | 0–10 (bimodal) | 0.5–1 | med-high | ★★★☆☆ | B (replaces it) | SPIKE behind flag |

**Portfolio verdict:** the A+B+C incumbent path alone projects LB ~10–18 by Oct 7. Adding F+G+H (risk-adjusted) projects **LB ~18–30 by mid-October** and keeps the Phase-2 70–90-level trajectory alive; the Flash-Next spike is a free call option on a 10-point jump. The binding constraints remain KV budget (docs/17 lesson), 1 sub/day, and the F1 fidelity gate — all three have explicit mitigations above.

## 7. Immediate actions (today, in order)

1. HF Space update: add World-Model Stack section (docs/20/21/22 pointers), qwen3.8 dual-version notes, refreshed roster (Task 14-f).
2. Repo push docs/20–22 + research artifacts.
3. Worklog Task 14 entry.
4. (User-side) confirm GPU session for Oct 1 swap + Oct 2 probe booking.
