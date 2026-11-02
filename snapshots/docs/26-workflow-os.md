# docs/26 — THE WORKFLOW OS: Dual-Track Operating System (validated funnel → nightly learning → paper)

2026-09-30 · User directive: staged validation (many CPU tests → small GPU tests → big run → submit), 1 submission/day, resubmission draws only 3–4/week at night, learn from every output, keep scouting better notebooks/methods, **dasshovon account = research lab for new architectures (MOAGS / MOAW / world-agent models / own innovations)**, **kraggle-for-work account = serious scoring track with concrete proof of improvement**, and everything documented to **paper quality**. This document is the standing operating system; docs/25 remains the week-1 schedule (account roles are re-mapped here).

Naming rule (standing): public artifacts and reports reference **notebook names only**, never account identities.

---

## 1. The four-stage funnel (every change passes through all gates)

```
STAGE 0  DESK            thesis paragraph + byte-diff review + quota check        (cost: 0)
STAGE 1  CPU TESTS       unit suite (51 checks) + smoke 123 steps + preflight     (cost: 0, unlimited,
                         53-playbook replay + offline engine sims + A/B sims       run as many as needed)
STAGE 2  SMALL GPU       interactive session ≤45 min: vLLM boot, serving config,  (cost: ~0.5–0.75h,
  SMOKE                  3-game × 100-step live probe, token/ctx budget check      only when serving changed)
STAGE 3  BIG RUN         push → batch run (~2.6h) → full offline public-25 pass   (cost: 2.6h, max 1/day/account)
STAGE 4  SUBMIT          score submission (+ nightly re-draws per §3)             (cost: 0 personal GPU)
```

**Gate rules (hard, no exceptions):**
- G1: no Stage-3 push without a written thesis naming the mechanism, expected direction, and the falsifying trace signal (docs/14 discipline).
- G2: Stage-1 must be green on the *exact* artifact pushed; kernel title == slug.
- G3: Stage-2 only if serving config changed; otherwise skip (save quota).
- G4: Stage-3 local result regressing >1 level-mass vs prior = **no submit**; mine traces first (local signal is free).
- G5: one ARC run at a time per account; never mix ARC and non-ARC batch runs the same day.
- G6: every Stage-3/4 output gets mined into the ledger within 12h (see §4 nightly cycle).

**Weekly GPU division (32h cap, ~11h deliberate margin):**

| Account | Track | Big runs | Small-GPU smokes | Weekly total |
|---|---|---|---|---|
| kraggle-for-work | **S — Serious scoring** | ≤5 à 2.6h | ≤2 à 0.6h | ≤14.2h |
| dasshovon | **R — Research lab** | ≤5 à 2.6h | ≤2 à 0.6h | ≤14.2h |
| Margin (reserve) | emergency fix / extra draw | — | — | ~3.6h |

---

## 2. The two tracks (one architecture, two mandates)

### TRACK S — Serious scoring (kraggle-for-work account)
**Mandate: concrete, provable score improvement every single week.** Runs only *validated* technology; every delta is ablated before adoption.

- Genome: **v9 = APEX stack** (docs/24): Flash-Next-NVFP4 base + lottery scheduler (value-corrected) + **playbook lane (53 verified)** + KV6B + 16K dedup + efficiency governor.
- Adoption rule: a mechanism enters the S genome only after (a) Stage-1 A/B offline win ≥ +10% levels-reached, or (b) an R-track run proves it live, and (c) it survives one S-track validation run.
- Proven genomes kept warm for re-draws: urad r10 (4.07), r12 sheetu12b (internal 5.19/45lv), taaf-sheetu12b (3.18).
- Reporting: weekly proof table (score before → after, levels, efficiency multiplier, ledger link).

### TRACK R — Research lab (dasshovon account)
**Mandate: discover the next architecture; feed validated winners to Track S; produce the paper's novel content.** Runs *hypotheses*, not production code. Each hypothesis is registered before any GPU is spent.

**Standing hypothesis queue (each: thesis → metric → kill criterion → max 2 big runs):**

| ID | Hypothesis | Metric (offline unless noted) | Kill if |
|---|---|---|---|
| H1 | **World-model zero-shot shield** (Qwen-AgentWorld / qwen3.8): F1 fidelity probe on 1,000 logged transitions; if ≥85% outcome-class acc → shield mode (counterfactual veto of irreversible actions) | probe acc ≥85% | <60% (then raw base or W2 LoRA) |
| H2 | **MOAW-lite**: agree→commit / disagree→conservative ensemble of W1 (zero-shot WM) + W3 (playbook table memory = exact world model); no new LLM | veto precision on 25-game sim; no level regression | any level-mass regression >0.5 |
| H3 | **MOAGS micro-router**: 2 experts (playbook executor vs LLM policy) + contextual-bandit routing | actions-to-L1 vs baseline; routing win-rate ≥60% | ≤50% after 2 runs |
| H4 | **ARC918-LoRA + same-game TTT** (Cassowary components) on our base | L1 actions vs cold start; transfer to unseen games | no L1 speedup on 10-game sim |
| H5 | **Scheduler genetics**: value-ticket exponent, knee slope, anneal shape (grid on CPU sims, 1 live confirm) | offline level-mass +10% | <+5% offline |
| H6 | **World-model synthetic rollouts** (AgentWorld decoupled simulator) to pre-train W2 ARC-native LoRA (only if H1 gate passes) | W2 probe acc vs W1 | <W1 baseline |

R-track outputs are *artifacts*: every hypothesis gets a numbered experiment folder, a result card, and a go/no-go verdict. Winners graduate via the S adoption rule.

---

## 3. Submission & re-draw policy (both tracks)

- **Fresh submission: exactly 1/day per account** — the day's Stage-3 output (or, if no run that day, the standing best genome).
- **Re-draws (resubmission of an identical version): 3–4 per week, on Track S only, launched each night** (scoring rerun = Kaggle-side, 0 quota — proven 9/23–24). Purpose: farm the σ≈1.5 draw variance (Affectify's identical code drew 5.68/4.09/2.30).
- Nightly draw launcher checklist: pick genome (standing best or current champion) → confirm slot free → submit → log draw ID in ledger → morning: mine result.
- LB keeps best per account, so draws are strictly non-destructive.
- Week-1 draw calendar (Track S): nights of 10/2, 10/3, 10/4, 10/5 (4 draws).

---

## 4. The learning loop (daily/weekly cadence)

**Nightly cycle (every day, 30–60 min):**
1. **Mine**: per-game levels, dead-action flags, efficiency multipliers, scheduler ticket flows, playbook replay hit/miss, token economy (input chars, generation chars, turns).
2. **Ledger**: append to `experiments/REGISTER.md` (run ID, stage, gate results, one-line verdict).
3. **Mistakes page**: any surprise gets an entry in `experiments/MISTAKES.md` with root cause + the gate/change that prevents recurrence (examples on file: KV collapse docs/17, checkpoint-rot, title-slug rename, state-key bug v7).
4. **Thesis update**: tomorrow's run thesis must cite today's evidence.

**Scouting SOP (Mon + Thu, 45 min):**
- Sweep the public notebook LB; pull any new notebook ≥4.5 into `notebook-intel/`, decode deltas, update the docs/23 family tree.
- Scan arXiv/blog feeds for world-model & agentic-harness releases; update research cards.
- Output: one "adopt / watch / ignore" verdict per item, logged in the register.

**Weekly close (Sun, 1h):** proof table per track · σ estimate refresh from the week's draws · next week's genome + hypothesis queue re-prioritization · paper section drafts advanced (§6).

---

## 5. Artifact & evidence conventions (paper-grade from day one)

```
experiments/
  REGISTER.md          # append-only: E-xxx entries (id, date, track, hypothesis, stage, gates, verdict, score)
  MISTAKES.md          # root-cause log with prevention rule per entry
  H1-worldmodel-shield/   # one folder per hypothesis:
    thesis.md · results.json · traces/ · card.md   # card = 1-page: claim, evidence, verdict, S-adoption
analysis/playbooks/    # 53 verified playbooks + transfer maps (S-track evidence)
notebook-intel/        # decoded competitor notebooks (scouting evidence)
docs/                  # 01–26 knowledge base; every claim cites its experiment ID
```

Rules: every score claim carries (notebook name, version, date, internal vs LB) · every mechanism claim carries an A/B · every curve has its raw JSONL preserved · internal scores are always labeled internal.

---

## 6. The paper (target: release after the campaign; writing starts now)

**Working title:** *"Allocation, Memory, and Imagination: Engineering Lessons from ARC-AGI-3"* — a systems paper from one campaign's full evidence trail.

| Section | Content | Evidence source |
|---|---|---|
| 1 Intro | competition scoring anatomy (triangular weights, efficiency², variance σ≈1.5) | docs/02, draw ledger |
| 2 Related | Tufa Duck, Affectify scheduler, TAAF/KV6B, Cassowary LoRA+TTT | docs/23 family tree |
| 3 System | 5-layer APEX stack + playbook lane + value-corrected raffle | docs/24, S-track ablations |
| 4 Research architectures | MOAGS router, MOAW ensemble, world-model shield — what worked, what didn't, and why | R-track H1–H6 cards |
| 5 Experiments | ablations: scheduler ±, playbook lane ±, efficiency governor ±, shield ±; variance study (best-of-N draws) | REGISTER.md |
| 6 Discussion | KV=concurrency law, turns=budget law, allocation value (+1.5–1.7), memory-as-code | docs/23 §5 laws |
| 7 Limitations | single-seed variance, gated models, quota constraints | ledger |

Writing cadence: §1–2 draft week 1 · §3–5 accumulate from ledgers weekly · full draft when the farm ends (≈10/20) · polish before 11/02 deadline freeze.

---

## 7. Week-1 instantiation (Oct 1–7, roles re-mapped to this OS)

| Day | TRACK S (kraggle-for-work) | TRACK R (dasshovon) |
|---|---|---|
| 10/1 | S0 funnel: assemble v9 L1 base from notebook-intel extracts; Stage-1 CPU all-green; **Big run 1** (smoke→full pass); submit port of urad-r10 config | H1 Stage-1: F1 probe harness on 1,000 transitions (CPU only); scout sweep |
| 10/2 | L2 scheduler port; Stage-1 A/B sim ≥+10%; **Big run 2**; submit L1 base | **night draw ①** (r12 pristine) · H1 verdict; if ≥85% → H2 build (CPU) |
| 10/3 | L3 playbook lane; 53/53 replay green; **Big run 3**; submit best | **night draw ②** (urad r10) · H2 smoke (Stage-2) |
| 10/4 | Integration (chain-aware tickets + knee + region tracking); **Big run 4** on S; submit v9-pre | **night draw ③** · H2 **Big run 1** (MOAW-lite live) |
| 10/5 | **v9-a FROZEN**; **Big run 5**; submit v9-a | **night draw ④** · H2 verdict → H3 build (CPU) |
| 10/6 | L4 flag work (CPU only); submit v9-a re-draw | H3 **Big run 1** (MOAGS micro-router) |
| 10/7 | Week close: proof table + σ refresh; submit champion re-draw | H3 verdict + result card; H4 prep; weekly close per §4 |

S-track GPU: 5×2.6h = 13h · R-track GPU: 2×2.6h (+1 optional) = 5.2–7.8h → **total ≤ 20.8h, margin ≥ 11h** (unchanged from docs/25, now with research content in the R slots instead of mirror-builds).

## 8. Standing warnings (inherited)

Kernel title==slug (rename cost a run 9/26) · never wipe history (−4.20 lesson) · KV budget before adding any expert (docs/17) · Milestone-2 OSS obligation check · multi-account compliance is a user-directed decision — keep notebook identities distinct and report by notebook name only.
