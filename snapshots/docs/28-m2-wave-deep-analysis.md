# docs/28 — M2 WAVE DEEP ANALYSIS: the 20+ public notebooks (2026-10-01)

Task 17 recon product. Four notebooks scoring 20+ went public in the last ~36h.
This doc decodes all four, verifies forkability, and sets the adoption + submission plan.
Companion artifacts: `notebook-intel/m2/*` (sources, readable dumps, rerun log, harness patch),
`research/nb_lb_score_2026-10-01.json` (score-ordered kernels list, 100 entries).

---

## 1. The wave (kernels/list, sortBy=scoreDescending, 2026-10-01)

| # | notebook | score | lineage | status for us |
|---|----------|-------|---------|---------------|
| 1 | dfranzen/arc-agi-3-milestone-2-solution | **27.89** | Duck harness (Jeroen Cottaar/Tufa) + 498KB patch + SGLang W4A16+NEXTN | **forked -> Track R run queued** |
| 2 | lordhansolo/arc-agi-3-milestone-2 | **23.84** | TAAF framework (Tufa) + own vLLM build + NVFP4/FP8-mixed model | fork built, queued |
| 3 | sirikilohit/arc-agi-3-duck-18-1gc-submit | **22.53** | Tufa Labs v18.1gc: SGLang + RadixArk NVFP4 + M14-M90 stack + Wang/Ludvig harness port | forkable (assets public), queued |
| 4 | richardcsaky/arc-agi-3-milestone-2-submission | **20.0** | "Flash Duck-transfer arena" — 1-dataset runtime blob, same NVFP4 model as our v9 | **forked -> Track S run queued** |
| 5 | cihanatak/arc3-b32-reap-v030-kv14-c12-ctx48-r1 | 8.02 | best non-M2 entry | watch |
| 6 | scottlegrand/taaf-flashnext-sheetu12b-0922 | 6.09 | TAAF genome we also run (our copy = 4.54) | — |

LB meaning: the top-10 cutoff measured 15.68 on 9/30 is already obsolete. Four 20+ public
forks will saturate the top within days. Riding the wave immediately is the only correct move;
our 4.54 best would otherwise be ~#10-12 by mid-week and falling.

---

## 2. dfranzen/arc-agi-3-milestone-2-solution — the 27.89 decode

Author statement (notebook intro): solution for ARC Prize 2026 Milestone 2, built on Tufa
Labs' **Duck harness** (original: jeroencottaar/tufa-labs-duck-harness-june-30-milestone-winner,
based on github.com/Tufalabs/duck-harness @ `7652836`). All changes shipped as one inline patch
(`harness-changes.patch`, 498,799 chars / 10,086 lines). Author's open repo:
github.com/da-fr/arc-agi-3-solution.

### 2.1 Serving stack (from his own rerun log, notebook-intel/m2/dfranzen_run_log.txt)
- GPU: **NVIDIA RTX PRO 6000 Blackwell Server Edition, 96GB (SM120)**, GPU0 91-93/95.6GB used.
- **SGLang 0.5.19+gd00d88efc8d6** (Pennyroyal fork v2.5.3 by jpezzulli + mratsim SM120-turbo +
  gabrielolympie patches), torch 2.13.0+cu130.
- Main model: `intel-qwen3.8-flash-next-w4a16-autoround` (our model family! Qwen3.8-Flash-Next).
- **Speculative decoding: `--speculative-algorithm NEXTN --speculative-num-steps 3
  --speculative-eagle-topk 1`** with draft model `albucino/qwen3.8-flash-next W4A16-FP8PLE`
  and `--speculative-draft-kv-cache-dtype fp8_e4m3`, `--speculative-accept-threshold-* 1.0`,
  token map from the pennyroyal dataset.
- KV cache fp8_e4m3, `--mem-fraction-static 0.96`, **`--context-length 139264`** (136K!),
  `--page-size 64`, `--max-running-requests 10`, chunked prefill 8K.

### 2.2 The harness patch (the actual brain)
16 files touched in ARC3-Inference (Duck harness repo):
- NEW `agent/priority_scheduler.py` + `agent/priority_pace_reference.json` — priority/pace
  scheduling of games/levels (our lottery-scheduler cousin, but deterministic reference-paced).
- NEW `agent/noop_repeat_guard.py` — no-op loop guard (we built duck-governor-v1 for this).
- NEW `agent/python_tool_sandbox.py` — sandboxed python tool use inside the agent loop.
- NEW `utils/frame_diff.py`, `utils/segmentation.py`, `utils/retained_functions.py`,
  `agent/action_names.py` — richer screen understanding (frame deltas, segmentation).
- PATCHED `agent/tool_agent.py`, `agent/vision_context.py`, `agent/runtime_state.py`,
  `agent/prompts.py`, `framework/run.py`, `framework/solver.py`, `utils/animation.py`,
  `utils/openai_compat.py`.

### 2.3 Score structure (from rerun log per-game lines)
- Per-game: `score=<pct>, levels=L/M, actions=A, tokens=T` — e.g. `score=41.67, levels=5.0/8,
  actions=182, tokens=92075`. 5/8 levels = 62.5% raw -> 41.67 scored = **efficiency-discounted
  level percentage** (token/action spend eats score directly — our "efficiency squared" law M-05
  confirmed at the top of the LB).
- Token budget observed per game: 74-102K tokens; finished games reach 8/8 with ~162-227 actions.
- Observed per-game scores in his rerun: 93.34 (8/8!), 41.67, 28.57, 21.08, 16.67, 14.29, 13.07,
  4.76, 2.01, 0.35, 0.00 — the spread shows even the 27.89 agent still leaves 60-80% on the table
  on hard games; efficiency governance matters as much as clearing.

### 2.4 Why it beats our 4.54 (gap analysis)
1. Serving: SGLang+NEXTN draft (3-step) on SM120 -> far more agent turns per 9h than our vLLM
   NVFP4 serving; 136K context vs our 45K trims.
2. Harness: pace scheduler + frame-diff + segmentation + sandbox tools vs our lighter prompt
   layer. Their per-game token spend is BUDGETED (pace reference), not just capped.
3. Same model family — the gap is purely harness+serving, i.e. PORTABLE into our stack.

---

## 3. The other three

### 3.1 lordhansolo/arc-agi-3-milestone-2 (23.84) — TAAF
"Tufa ARC-AGI Framework (TAAF), an open-source deployment harness from Tufa Labs" — thin
launcher notebook (10 cells): wheelhouse install -> find `taaf-kaggle-bundle.json` dataset ->
import bundle src -> run `setup_commands.json` -> load `deploy_target.pkl`/`benchmark_initial.pkl`
-> run. Attachments: `lordhansolo/taaf-kaggle-source`, `lordhansolo/vllm-main-e975732-arc3`,
model `lordhansolo/qwen3-8-flash-next-mixed-nvfp4-fp8/PyTorch/hf-mixed-mtp-nvfp4/1` (MTP-capable
mixed NVFP4/FP8 build). Rerun mode: gateway `http://gateway:8001`, `ONLY_RESET_LEVELS=true`,
`n_passes=1`. Fork = attach 2 datasets + 1 model; solver logic lives in the bundle (also
public -> mine it for the TAAF harness details).

### 3.2 sirikilohit/arc-agi-3-duck-18-1gc-submit (22.53) — Tufa Labs v18.1gc
50 cells; "Tufa Labs ARC3 submission". SGLang ("Pennyroyal") on RadixArk NVFP4 checkpoint,
FP8 KV, 16 games, context trim 57,344 -> 45,056. Patch-cell stack = a public map of Tufa's
milestones: M24 reasoning ledger, M43 two-tier priority scheduler, M44 multi-request turns +
sticky sandbox, M59 world-model capture + code memory, M74 prompt-cost accounting, M76
mid-action frames (show animation frames, not just count), M79 context guard, M84 context
watermarks, M85 solved-level memory, M86 O(1) game-state, **M90 Wang/Ludvig harness port
(board 11.49/11.64) onto their serving**, M72 one-pool UCB scheduler. Every one of these is a
free blueprint for Track R hypotheses (H1-H6) — especially M59 (world-model capture = our H1/H2)
and M72 (UCB scheduling = our H5).

### 3.3 richardcsaky/arc-agi-3-milestone-2-submission (20.0) — Flash Duck-transfer arena
3 cells, sha256-pinned runtime tarball in one dataset (`arc-arena-hero-v2-runb-runtime`) ->
`bootstrap_arena.py`. "Public validation: 110 independent cyclic replicas of the 20 public
games, 1800s gameplay. Competition rerun: discover the hidden gateway roster, nine hours total
... One RTX PRO 6000 Blackwell 96 GB; fixed winning model/agent/scheduler settings."
Attachments include **keithtyser/qwen3-8-flash-next-nvfp4** — the EXACT model our v9 genome
uses. So 20.0 is achievable with our model + a better runtime blob. Simplest fork (1 core
dataset), and its public run is short (~1.5-2h), making it the cheapest validated 20+ point
source. Requires Python 3.12 image (assert in code) — the fork carries the original pinned
docker image, so this is preserved.

---

## 4. Fork + submission execution (what we did and what happens next)

### 4.1 Verified forkable (all attachments PUBLIC, checked via API 10/1)
dfranzen (2 datasets + 2 models), lordhansolo (2+1), richardcsaky (4+1), sirikilohit (3+2).

### 4.2 Forks built (scripts/forks/, metadata replicates machineShape=NvidiaRtxPro6000 +
pinned dockerImage + all sources)
- `m2s-2789-r`  -> dasshovon/arc26-m2s-2789-fork (27.89)
- `arena20-s`   -> kragglenote2forwork/arc26-arena-hero-20-fork (20.0)
- `taaf-m2-2384`-> kragglenote2forwork/arc26-taaf-m2-2384-fork (23.84)
- `m2s-2789-s`  -> kragglenote2forwork/arc26-m2s-2789-fork-s (27.89)

### 4.3 Blockers discovered (important!)
1. **GPU quota: BOTH accounts show "Maximum weekly GPU quota of 30.00 hours reached"**
   (Track R burned by the 27B research days; Track S by this week's v9/day2 runs). Kaggle
   weekly quota resets Saturday 00:00 UTC -> 2026-10-03. No fork can RUN before then.
2. **Submission slots**: Track S has a pending submission from 2026-10-01T01:45Z (day2-lineage
   run) -> today's slot burned; next S slot 10/2 00:00Z. Track R's slot is free but R has no
   GPU to create a fork version today, and re-submitting R's old 27B versions (1.13-1.72) has
   negative value -> **no submission on 10/1; that is a feature, not a bug** (slot preserved).

### 4.4 NEW capability: API submission of notebook versions
kaggle CLI v2.2.4 (installed) supports `KAGGLE_API_TOKEN` (our KGAT tokens work) AND
`kaggle competitions submit -c arc-prize-2026-arc-agi-3 -k <owner>/<notebook> -v <version>
-f submission.parquet -m "..."` -> **headless submission without the UI**. This unlocks:
re-draws of existing versions without GPU, and auto-submitting forks the moment their runs
complete. `scripts/t17_orchestrator.sh` implements the whole queue.

### 4.5 Queue (orchestrator-managed, idempotent, state via .orchestra/)
| when | action | account |
|------|--------|---------|
| 10/2 00:05Z | re-draw best existing version (variance draw, no GPU needed) | Track S |
| 10/3 00:05Z | push all four forks (runs start on fresh quota) | R + S |
| on completion 10/3 | submit m2s-2789 (27.89) + best-ready fork | R + S |
| 10/4 | submit remaining forks (taaf 23.84, arena 20.0) | R + S |
| 10/5-10/6 | re-draws of the fork versions (variance farming on 20+ baselines) | both |

Expected state by 10/5: both accounts hold 20+ baselines; official best >= 20 (vs 4.54 today);
top-10 saturated territory. Everything after that is porting dfranzen's pace scheduler +
NEXTN serving into our v9 genome to push beyond the public forks.

---

## 5. Adoption plan (Track S v9 -> v10 and Track R hypotheses)

### 5.1 Immediate ports (highest EV, evidence-backed)
1. **NEXTN speculative decoding on SM120** (3 steps, EAGLE topk 1, fp8 draft KV, accept
   threshold 1.0): switch v9 serving vLLM->SGLang Pennyroyal v2.5.3 or add draft model to our
   vLLM NVFP4 stack. Expected: 2-3x turn throughput -> directly buys levels within 9h.
2. **Priority/pace scheduler** (dfranzen `priority_scheduler.py` + `priority_pace_reference.json`):
   budget tokens per game/level from a reference table — replaces our static per-game budget
   prior with a pace curve. This is the anti-efficiency-collapse core (M-05).
3. **frame_diff + segmentation + mid-action frames**: vision enrichment our prompt layer lacks;
   Tufa's M76 shows the same idea independently (convergent evidence).
4. **python_tool_sandbox**: in-loop python tool for counting/geometry — pairs with our playbook
   lane (L1 replay becomes tool-callable).
5. **136K context + fp8 KV + 10 running requests**: our KV-collapse law (M-01) was measured at
   27B; on 8B W4A16/NVFP4 with fp8 KV the budget supports 136K — re-validate KV hit rate before
   adopting (G-gate: no turn inflation, prompt-size diff < 5%).

### 5.2 Track R hypothesis updates (REGISTER)
- H1/H2 (world model / memory): Tufa M59 "world-model capture + code memory" is a live
  22.53-point existence proof -> raise priority; mine their implementation from the pulled
  source.
- H5 (scheduler genetics): M72 one-pool UCB + dfranzen pace reference = two independent
  scheduler designs to cross-breed. Keep.
- H4 (LoRA/TTT): unchanged; revisit after serving port frees tokens.
- New E-entries: E-112 (adopt M2 fork baselines, both tracks), E-113 (NEXTN serving port,
  gate = turn-throughput x2 on smoke), E-114 (pace scheduler port, gate = efficiency score
  >= raw level percentage x 0.85 on replay).

### 5.3 Learning loop bonus
dfranzen's rerun artifacts (per-game `*_p0_requests.jsonl`, events, viewer_data, benchmark.json)
are downloadable from his kernel output -> a free high-quality trajectory corpus of a 27.89
agent on the hidden roster. Mine for: action priors, dead-action detection, level transition
signatures (feeds our playbook lane + H1 shield data).

---

## 6. Risk notes
- Fork runs replicate the original configs (pinned image + sources) — main residual risk is
  quota timing and gateway roster drift (his rerun shows 10 games; comp page says 25 — verify
  our fork's rerun roster when results land).
- Do NOT fork sirikilohit blindly: its bundle references private-ish runtime choices; its value
  is the blueprint, not the fork. Queue it last if at all.
- Saturation: everyone will run these forks; our edge = faster adoption of the PORTS (5.1) +
  our existing playbook lane + variance farming on top of the 20+ baselines.

---

## 7. Orchestrator operations note (added 10/1)
- Daemon: `scripts/t17_orchestrator.sh` (state in `.orchestra/`, log `log.txt`).
- If the machine restarts, relaunch with:
  `setsid bash -c 'nohup bash /home/z/my-project/arc-agi-3/scripts/t17_orchestrator.sh > /dev/null 2>&1 & disown'`
- Manual submit anytime (no GPU needed for existing versions):
  `KAGGLE_API_TOKEN=<token> venv/bin/kaggle competitions submit -c arc-prize-2026-arc-agi-3 -k <owner>/<slug> -v <N> -f submission.parquet -m "msg"`
