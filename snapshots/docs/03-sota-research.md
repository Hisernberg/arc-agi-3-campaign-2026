# 03 · State-of-the-Art Research (Sept 2026)

Full research report cached by research sub-agent (Task 2-a) — raw pages in
`/home/z/my-project/research/arc-agi-3/`. This is the distilled version.

## Kaggle leaderboard snapshot (2026-09-17/18)

| Rank | Team | Score |
|---|---|---|
| 1 | **Tufa Labs** | **18.81** |
| 2 | Daniel Franzen | 13.12 |
| 3 | Matija Ludvig & Zhongwei Wang | 11.49 |
| 4 | NVARC3 | 11.04 |
| 5 | Lord Han Solo | 9.88 |
| 6 | Tong Hui Kang | 8.72 |
| 7 | Ebi | 8.68 |
| 8 | Third Intelligence | 8.21 |
| 11 | Kyutai | 7.19 |
| — | **Us (Kragglenote2 Forwork)** | **3.45** |

No public write-ups found for ranks 2–11 (verified explicitly). Tufa Labs is the only
top team with a detailed public methodology.

## Platform leaderboard (unconstrained — shows the ceiling)

| System | RHAE public | Key idea |
|---|---|---|
| **Schema** (Impossible Research/Berkeley/CMU) | 99% | Agent writes game theory as executable `step(state,action)` + `is_goal()`, **backtests against full transition history**, BFS-plans inside certified simulator, acts to run discriminating experiments. Same model w/o harness: 42.8% → harness = +56 pts |
| **NVIDIA AVO** | 100% (183 levels, 6,624 actions) | Text-only 64×64 grids, persistent memory, supervisor detects stagnation & redirects. "Benchmark performance = complete agent system, not model" |
| **Tycho** (NIMI) | 100% | Formalizes games as deterministic Moore machines; coding agent builds executable per-game hypotheses; delegation policy |
| **GPT-6 Astra** | 62.7% semi-private std harness; 99.9% provider-adapter | Preserving opaque reasoning state + compaction = 1.6× | 
| **OpenAI 2-settings** | 13.3% → 38.3% | Retained reasoning + compaction ≫ rolling truncation (3× score, 6× fewer tokens) |
| **INT21 SwarmOS** | 13.3% → 100% | Self-improving agent swarms, no ARC specialization |
| **Strands (AWS)** | 99.95% | Text grids + append-only log + action-queue loop; "agent did its own context engineering" |
| **Symbolica ARCgentica** | 36.08% (day 1) | Recursive language models; solves through code |
| **RGB Agent** | — | Opus 4.6 + READ/GREP/BASH over uncompressed log.txt; "search is sufficient"; pre-built helpers gave ≤0 return |
| **Graph exploration** (Rudakov et al.) | 3rd on preview (training-free) | Segmentation + salience + directed state-graph exploration, no LLM |

**Ceiling insight: harness ≈ 2×+ the score of the same model.** The Kaggle-relevant question
is how much of Schema/AVO-style world-modeling fits in a 9 h notebook with a Qwen3.8-8B-class
model instead of Opus-class frontier models.

## Tufa Labs Duck (M1 winner, our base)

- CodeAct REPL agent + python tool; segmentation view (position-invariant object hashes);
  4× upscaled frame image each turn; world-model note carried across turns; 64k context,
  evict-oldest-user-turn; UNDO withheld; batched verified action plans; RESET-keeps-level.
- Public-25 mean 1.60 ± 0.45 (20 runs) with Qwen3.6-27B-FP8 in June → 18.81 Kaggle now
  (they iterated heavily: September submissions moved from ~12 to 18.81).
- Their stated lessons: gains came from **better base models + multimodality**, NOT
  hand-crafted tools; prompts encode generic ARC knowledge (HUD/timer traps, BFS advice,
  frame-diff hygiene); see headroom in context compaction/memory.

## Milestone-1 runners-up (Kaggle-viable recipes)

- **Reki (2nd):** vision-LLM-as-policy, local Gemma-4-31B, recent frames as labeled images,
  one JSON per step (what changed / plan / 1–4 actions), reflection memory ~every 10 steps,
  JSON self-repair, legal-action constraints, numpy click heuristic (no GPU) preferring
  small/rare/button-like objects, dead-signature detector for hopeless click targets.
- **forge (3rd):** same family + candidate-generator/arbiter; best run disabled all extras.
  Lesson: **local public scores are an unreliable leaderboard proxy**.

## Cross-cutting lessons applicable to Kaggle RTX6000 9 h / Qwen3.8

1. **Generic code execution beats bespoke tools** (Tufa, RGB, Stochastic Goose lineage).
2. **Executable world models + backtesting** = the single biggest known lever (Schema
   +56 pts with identical model; controlled experiment).
3. **Discriminating probes**: when 2+ hypotheses live, pick the action whose outcomes
   differ across them — maximizes information per real action (real actions are what's scored).
4. **Context compaction/retained reasoning** ≈ 1.6–3× (OpenAI, Astra).
5. **Text grids work for strong models** (AVO/Strands) but Qwen3.8-8B is weaker — keep
   Duck's multimodal frame image + segmentation.
6. **UNDO (ACTION7) withholds well-earned trust** (Tufa found LLMs waste budget).
7. **Variance management**: ±0.4 swings; submit same notebook 2×; avoid overfitting to
   public-25 single runs.
8. **Kaggle ops**: verify provisioned GPU actually = RTX Pro 6000; smoke-test `/v1/models`
   before playing; don't mix wheelhouses; expect submission queues.
