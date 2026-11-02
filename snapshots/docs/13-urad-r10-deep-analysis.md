# 13 — Deep Analysis: urad-duck-r10-targeted (4.68) + R9/R10 Fix Catalog

*Generated 2026-09-27 from the checkmpobbyacckraggle archive (Team AIRIS / poby7722 backup repo).*

## 1. What the archive is

`Hisernberg/checkmpobbyacckraggle` is a full API-pulled backup of Kaggle account **poby7722**
(Team AIRIS with krno1legend, aadigupta*, koushikrudra; one deleted member `del=46a2189…`).
ARC-AGI-3 standing: **Team AIRIS #69-77 of ~3397, best official score 4.68** via
`krno1legend/urad-duck-r10-targeted` (scriptVersionId 352406510), submitted 2026-09-26.
The same code was submitted 3 times: **2.78 → 3.78 → 4.68** — the official scorer re-plays the
agent stochastically, so identical work draws different official scores. The archive contains
the complete notebook, the full 282-file run bundle (transcripts, per-action benchmark.json,
vLLM receipts) and the whole submission history (50 visible).

## 2. Lineage

```
Tufa Labs Duck/TAAF (MIT)
  └─ jakobbrggen/taaf-kaggle-source-anim-20260807-anim  (CC0 Kaggle bundle, same base as ours)
      └─ JustAdev742/Arc-Agi-3-Kaggle-comp @ 8c9fe77   (R9 series, frozen fixes P1–P22)
          └─ krno1legend/urad-duck-r10-targeted         (R10 = R9 + first-level stall rescue)
```

Same anim bundle we forked for v4/v5 — but 22 surgical, trace-evidenced fixes on top.

## 3. Run economics of the 4.68 run (8B NVFP4, RTX Pro 6000)

| Metric | Value |
|---|---|
| Wall duration | 2.2 h (592 s setup + 7926 s run) |
| Model calls | 1327 attempts / 1302 success |
| Actions | 2541 (≈1.95 actions per call — batched) |
| Prompt tokens | 26.6 M (prefix caching OFF, KV 5 GiB) |
| Completion tokens | 2.0 M (13.3:1 prompt:completion) |
| Levels completed | **37 / 183 public levels (20%)** |
| Internal benchmark mean | 7.10 (their internal metric; official draws 2.78/3.78/4.68) |
| vLLM profile | KV 5 GiB, max_batched_tokens 8192, max_num_seqs 8, MTP 3 |

Per-game spread (score = their internal per-game metric): ft09 42.7 (4/6 lv), lp85/vc33 21.1,
re86 16.7 … sc25 0.0 (0/6 lv). Every game ran the full 2.1 h window in parallel (28 workers).

**Action distribution:** ACTION6 (mouse click) 35.9%, ACTION1 16.6%, ACTION3 15.0%,
ACTION4 14.6%, ACTION2 13.3%, ACTION5 3.7%, RESET 0.8%, ACTION7 0.1% (UNDO still unused).

**Failure modes by cluster:**
- *Grinders* (many actions, few levels): wa30 181 acts/1 lv, tn36 180/1, ls20 187/1,
  re86 224/3, ka59 194/2 — action grinding without model insight.
- *Thinkers* (few actions, huge tok/act): bp35 25 acts @ 3061 tok/act, su15 47 @ 1735,
  lf52 46 @ 1358, m0r0 38 @ 2481 — deliberation loops, rescue hints didn't convert to probes.
- *Winners*: ft09 (96 acts, 653 tok/act, 4 levels) — batched probing + clean mechanics.

## 4. The R9/R10 fix catalog (all evidence-driven)

Each patch is an exact-text (old,new) pair that must match exactly once — a changed upstream
fails loudly. P-numbers map to experiments (exp-032/034, stall analyses).

| Fix | What | Measured evidence |
|---|---|---|
| P1 | Read `World model:/Plan:` lines from **hidden reasoning** when visible reply is empty; last block per label, capped 600 chars | 67% of Qwen tool-call turns had empty visible content |
| P1B | Lenient label match ("World model update:", "World model (level 2):") | 272/1329 responses had qualifiers |
| P2 | Name ACTION7 = UNDO in the model-facing table | 15 rejected attempts in 6 games |
| P3 | Keep goal/action models across levels, marked "[from an earlier level; verify]" | win condition constant across levels |
| P4 | **History compression**: old user turns lose standing instructions/note/image; past assistant turns lose reasoning (env OURS_STRIP_PAST_REASONING=1) | past reasoning = 35% of prompt tokens |
| P6 | **Persistent defs store** across python calls: top-level funcs/classes/imports/UPPER_CASE constants (≤12k chars) replayed as silent prelude; prompt lists kept helper signatures | 54% of 1116 defs redefined existing names |
| P7 | Sandbox: pre-import json/math/collections/…, add __build_class__, exception classes, `__name__="__main__"`, json-convert final inside stdout redirect | 20 NameErrors; stray-print protocol bugs |
| P8 | At level transitions request a `Cross-level notes:` line before acting | median 3 calls/8 min before first action on a new level |
| P9 | Harness-computed **board diff line** after each action sequence: changed cells grouped into ≤3 regions w/ bounding boxes + top colour transitions in ARC colour letters | 62% of calls re-split `.ascii` themselves |
| P10 | Level-1 scoring note: "level 1 counts least, probe cheaply, batch probes" | score weights level k by k |
| P14 | Level-start lines: harness comparison vs L1 board, untried actions, run-length-encoded record of how the previous level ended | new-level cold start |
| P15 | Idle governor: no action ≥8 min AND level age ≥10 min → one probe hint (env-tunable) | same design as our Governor v0 |
| P16 | Prompt carries "Harness record of completed levels (exact)" (last 3) | cross-level memory |
| P17 | Animation error views keep the usual keys (no KeyError); animation hint re-fires only after a NEW transient animation | 12/34 failed calls involved animation(); s5i5 re-read one stale animation 7× |
| P18 | `expect:` line before each action call — predict, then compare with P9 diff (idea from VISTA/arc3cb) | catch wrong world model in 1 action |
| P19 | **Supervisor review**: one extra reviewer call when a level stalls ≥30 min (NVIDIA AVO-style): sees notes, RLE action tail, untried actions, board; returns 2 alternative hypotheses + probes | AVO supervisor pattern |
| P20 | **HUD/no-impact detector** (ported from thui-l1-v0, which scored 10.93 vs 9.32 base on public 25): learns rows changing on ≥90% of actions (≤4 rows, after 20 actions); actions changing only those rows → `no_impact`, "do not read as effects" | HUD ticks read as effects |
| P21 | **Weighted call gate** in front of vLLM: ≤8 in flight, priority = level-weight × wait, fade after 45-min stall; turn yields reshape to 2 calls/turn | KV fits 4–6 requests; 20 more wait ≈126 s each |
| P22 | Level-up transitions not offered as latest change (previous_frame/last_transition nulled on new level) | 5 level starts wasted reasoning on cross-level diff |
| R10 | First-level stall rescue: level ≥10 min + no action ≥8 min + ≥2 completed replies → 1 hypothesis/probe hint; ≤3/game, ≥10 min apart; disabled after a completed level | first-level stalls |

## 5. What this means for us

1. **Their internal 7.10 → official 4.68 (best draw) is the strongest *validated 8B harness* we
   can copy.** Our v4 (3.85) overlaps with ~7 of their fixes (governor≈P15, board diff≈P9,
   budget prior≈r9_budget, note discipline≈P1/P8) but lacks P4 (history compression),
   P6 (def store), P20 (HUD), P21 (gate), P22 — the four we don't have are exactly the
   highest-value ones by their ablation history.
2. **Score variance is a first-class lever.** Same code drew 2.78/3.78/4.68. Re-submitting a
   good kernel on consecutive days ratchets the LB (best draw counts).
3. **The 27B lever dwarfs everything.** Their own (deleted-member) `arc3-duck-v12-1d7d88` with
   Qwen3.8-27B-FP8 scored **LB ~9**. The 27B FP8 repack is now **public**
   (`foysalemonshanto/qwen3-8-27b-fp8-repacked-v1`, pyTorch/hf-fp8 v1, 16 layer shards +
   mtp/outside safetensors), and the LB-9 notebook itself is in our research cache with its
   full serving recipe (patch MODEL_OWNER/MODEL_SLUG/SERVED_MODEL_NAME in the bundle's
   setup_commands.json; wheelhouse `driessmit1/arc3-vllm-h100-wheelhouse-v3`; RTX Pro 6000).
4. Token budget: P4+P6+P9 *net-reduce* tokens (35% of prompt was past reasoning; 62% of calls
   re-derived diffs the harness can compute for free) — fully compatible with our KV 3.2-full-
   context serving constraint.

Sources: archive `arc-prize-2026-arc-agi-3/latest-full-code/`, `submissions/best/sub_56568844__pub-4.68/`
(urad_r10_sources_atpyd1b6/taaf_ours_patch.py = 1208-line patch catalog), benchmark.json/score.json.
