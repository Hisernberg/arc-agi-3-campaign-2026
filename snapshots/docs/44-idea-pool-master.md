# 44 · IDEA POOL MASTER INDEX — 1,515 entries (Oct-27 wave: +495 D + +500 E)

Curated pool: docs/40-oct26-idea-pool.md (**112** entries, evidence-tagged, §1-11).
Mined batches: A=113, B=169, C=126 → **408** entries; batch D (Oct-26 curated) = **495**;
batch E (Oct-27 arena wave) = **500** (E-001..E-500, public-kernel mining + grandmaster
norms + expert domains + qwen3.8 intel + law codification).
**Total: 1,515 ideas** across 55 public notebooks + LB intel + own forensics.

## Distribution (mined batches)
- by category: {'serving': 72, 'eval': 64, 'submission': 45, 'sandbox': 41, 'meta': 40, 'scheduling': 34, 'waste-guard': 33, 'memory': 25, 'exploration': 20, 'perception': 19, 'prompt': 15}
- by applicability to our stack: {'port-cell': 165, 'already-have': 149, 'flip-config': 52, 'future': 42}
- by effort: {'S': 325, 'M': 72, 'L': 11}
- richest sources: {'dennis6886__arc3-d-prime-public-base': 54, 'dfranzen__arc-agi-3-milestone-2-solution': 40, 'shiiin9__affectify-arc-31-54-in-a-single-sub': 26, 'foysalemonshanto__lb-9-arc3-duck-v12-with-qwen-3-8-27b': 26, 'sirikilohit__arc-agi-3-duck-18-1gc-submit': 21, 'muhibullahansir__duck-qwen3-8-anim-base': 20, 'projectforty2__forge-arc-agi-3-agent': 17, 'keithtyser__duck-qwen3-8-27b-fp8': 15}

## Immediate actionability (cross-batch, our stack)

| Rank | Idea | Source | Why |
|---|---|---|---|
| 1 | A-016 prefix-caching OFF won a measured A/B | chiakazirim | SGLang --disable-radix-cache A/B candidate on our smoke |
| 2 | A-019 seq-cap valve 8 vs 28 concurrency | chiakazirim | serving stability lever |
| 3 | A-044 completion-ceiling metric | muhibullahansir | direct D'/endgame-fade input |
| 4 | A-029 active-probe nudge after 3 action-less calls | muhibullahansir | port-cell, kills inspection stalls |
| 5 | B-016 whole-frame state hash (border=0) | jingshuifu/M2 | risk check on our death ledger today |
| 6 | B-023 read-timeout -> yield not rollback | dfranzen M2 | saves ~900s round trips |
| 7 | B-028 KM TAIL_LOOKUP_80K pace table | shiiin9 | drop-in D' upgrade |
| 8 | B-050/051 shiiin9 serving args (kv fp8, page 64, memfrac .96) | shiiin9 | diff ours tonight |
| 9 | C-010/019 prefix-band slot economics | skarin | cache-warmth-aware scheduling |
| 10 | C-069 action-grant scheduler (pts/action cliff at 60) | bang1850 | scheduling A/B |
| 11 | C-077 image-token fix (66 vs 505-622) | poonszesen | 1-3k prompt tokens/turn back |
| 12 | C-084 context watermarks 32k±4k | poonszesen | ~10% faster than trim-at-budget |
| 13 | C-081 exact-token guard via /v1/tokenize | leoprovorov | kills frozen-run failure mode |
| 14 | C-114 eval power math (MDE=2σ√(2/N)) | gregkamradt | A/B methodology |

Full entries: `reports/oct26_sweep/ideas_batch_A.jsonl` (schema: id/source/title/category/
mechanism/evidence/our_stack/effort/cell_hint), `_B.jsonl`, `_C.jsonl`. Curated 112 with
evidence tags: `docs/40-oct26-idea-pool.md`. Top-50 personalities: `top50_dossier.md`.

## Update 2026-10-26 (batch F)

Batch F = **60 ideas** (F-001..F-060) from the six-notebook teardown (docs/52) +
three mixture architectures (docs/53). Schema: id/source/title/category/mechanism/
evidence. File: `reports/oct26_sweep/ideas_batch_F.jsonl`.
**Pool total: 1,575.** Top adoptions: F-001 solved-level memory (v14 core),
F-002 retry-3600, F-003 noop-parity audit, F-004 redraw farm v1.
