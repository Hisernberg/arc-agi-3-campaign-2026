# 18 — HF Hub Command Center + Full Frontier Mirror (2026-09-29)

## What was built (all public, user account `Nabidnur`)

| Asset | Link | Contents |
|---|---|---|
| **Space** | https://huggingface.co/spaces/Nabidnur/arc-agi-3-command-center | One-page command center: LB vs us, frontier systems, models, 7-gap analysis, wave plan, results trail |
| **GitHub collection** | https://huggingface.co/datasets/Nabidnur/arc-agi-3-github-collection | **45 mirrored repos** (~4.6GB, .git stripped, GITHUB-INDEX.md + provenance JSON): Retrodict, Tycho, Crystalline, TWIN, PRO-LONG, TELL, agno, dream-team, Continual Harness, arcprize official ×7, Tufa duck-harness incl. **full example-run trace corpus** (2.8GB events/transcripts/prompts), our checkmpobby Kaggle archive (237-run history) |
| **Datasets combined** | https://huggingface.co/datasets/Nabidnur/arc-agi-3-datasets-combined | 7 frontier trace sets (Codex-GPT5.5/Kimi-K2.7/Fable-5 on ls20/ar25/ft09/su15) + schema-harness traces (741MB) + ARC-AGI-1/2 evals + human-testing + indexes (LB JSON, discovery dumps) |
| **Models + analysis** | https://huggingface.co/datasets/Nabidnur/arc-agi-3-models-and-analysis | MODELS.md (serving shortlist), ANALYSIS.md (5.19/6.68 vs world), PLAN-18-28.md, live intel |
| **Collection** | https://huggingface.co/collections/Nabidnur/arc-agi-3-toolkit-models-repos-datasets-plan-6abbc63ac53a2bedf7532441 | 12 curated items (7 models + 5 assets) |

## Credentials used
- GitHub: new token (Hisernberg) — repo sync OK (campaign at a94dcdb)
- HF: new token (user **Nabidnur**, fine-grained w/ repo.write + collection.write)
- Kaggle: KGAT token works ONLY via `Authorization: Bearer` (basic auth 401) — LB pull OK

## Live LB (2026-09-29 API): Tufa 45.33, Yi-Chia 36.73, Franzen 26.55 (top-3 cutoff), Han Solo 22.24, THK 20.53, last dance 20.51, Third Intelligence 18.29, NVARC3 16.07, keithtyser 9.17. Us: 6.68 (45/183).

## The 7 gaps (ANALYSIS.md) → PLAN-18-28 waves
G1 plan-queue w/ predicted-cells (Retrodict) · G2 free hypothesis replay (Retrodict/TWIN) · G3 append-only searchable log (PRO-LONG) · G4 typed persistent memory (Crystalline +40pp ablation) · G5 executable twin (TWIN 7.8→93.3 same model) · G6 engine-wheel introspection in Kaggle env (Crystalline path; rules-check first) · G7 MoE throughput swap (Qwen3-30B-A3B-FP8).

Waves: W0 ship v8 APEX (→7-9) → W1 G1+G3 (→10-13) → W2 G7+G2 (→13-17) → W3 G4+G5 (→18-24) → W4 G6+ratchet (→24-28+). One mechanism per run, tok/action gate, env-var switches, rollback ladder.

## Ops notes / gotchas
- Sandbox kills ALL background processes between tool calls → inline only, resumable patterns
- HF upload_large_folder = ~20 files/commit → burns the 128 commits/hour limit fast. Use per-folder `upload_folder` (1 commit each) for everything
- HF downloads: 2.23MB/s single-stream, ~6MB/s @ 8 workers; uploads much faster
- v1_public_eval (946MB/27k files) + v2 eval partial → referenced at source, not fully mirrored
- Nemotron-SFT (18GB) → reference-only
- Mirror completion: ~4.4k minor files pending across 30 small repos (rate-limit window); all Tier-S complete. Re-run `scripts/complete_mirror.py` after window reset.

## Immediate next actions
1. Ship v8 APEX on dasshovon (W0) — 61/61 green, built & validated
2. Re-run complete_mirror.py in ~1h for the final ~4.4k files
3. Wave-1 build: plan-verify runner (G1) + search_log tool (G3) on the 3.85/6.68 artifact
4. Check dasshovon GPU quota before each wave run
5. M2 go/no-go: recommend NO-GO (deadline 9/30)
