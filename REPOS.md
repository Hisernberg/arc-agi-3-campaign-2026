# REPOS.md — Complete ARC asset index (GitHub · Hugging Face · Kaggle)

Everything the team (`arc-needs-to-be-agi`, operator account **Hisernberg** / **Nabidnur**)
built or used across the ARC-AGI-2 and ARC-AGI-3 campaigns, in one table set.
This repository (`arc-agi-3-campaign-2026`) is the combined public writeup; the private
repositories remain the system of record.

## 1. GitHub — ARC-AGI-3 (this campaign)

| Repository | Visibility | What's in it |
|---|---|---|
| **[arc-agi-3-campaign-2026](https://github.com/Hisernberg/arc-agi-3-campaign-2026)** | **public** | **This repo** — the combined master writeup: chapters 00–11, 8-figure viz pack, machine-readable ledgers, scrubbed builders, campaign agent roles |
| [arc-agi-3-campaign](https://github.com/Hisernberg/arc-agi-3-campaign) | private | Full campaign workspace (7,000+ files): harness, agents, research, artifacts, daily protocol |
| [arc-agi-3-campaign-writeup](https://github.com/Hisernberg/arc-agi-3-campaign-writeup) | private | Master writeup source: chapters 00–10 + raw snapshots (its content is merged here) |
| [arc-forwork](https://github.com/Hisernberg/arc-forwork) | private | ARC-2 + ARC-3 evidence locker: frozen candidates, validation, dossiers, production manifests |
| [arc26-endgame-v63-finalday](https://github.com/Hisernberg/arc26-endgame-v63-finalday) | private | Endgame kernel builder v63 (final-day validation builds); scrubbed copy in [`code/`](code/) |
| [arc26-endgame-v45s](https://github.com/Hisernberg/arc26-endgame-v45s) | private | Endgame kernel builder v45s/v44-mixture; scrubbed copy in [`code/`](code/) |

## 2. GitHub — ARC-AGI-2 (prior campaign, same lineage)

| Repository | Visibility | What's in it |
|---|---|---|
| [arc-agi-2-solver](https://github.com/Hisernberg/arc-agi-2-solver) | public | High-scoring ARC-AGI-2 solution — NVARC+ with Qwen3-4B, ensemble + test-time compute |
| [arc-agi-2-kaggle](https://github.com/Hisernberg/arc-agi-2-kaggle) | private | Full ARC-AGI-2 competition workspace (NVARC+ pipeline, shape-prior selection, RL harness) |
| [arc26-nvarc-2026](https://github.com/Hisernberg/arc26-nvarc-2026) | private | NVARC lineage builds, gates, receipts for ARC Prize 2026 |

## 3. Hugging Face — datasets & models

| Repo | Type | What's in it |
|---|---|---|
| **[arc-agi-3-campaign-2026](https://huggingface.co/datasets/Nabidnur/arc-agi-3-campaign-2026)** | dataset | **Mirror of this writeup**: chapters, figures, ledgers (data/) |
| [arc-agi-3-traces](https://huggingface.co/datasets/Nabidnur/arc-agi-3-traces) | dataset | Agent interaction traces from ARC-AGI-3 gameplay |
| [arc-unified-corpus](https://huggingface.co/datasets/Nabidnur/arc-unified-corpus) | dataset | Unified ARC-2+3 training/analysis corpus |
| [arc-superbrain-small-models](https://huggingface.co/Nabidnur/arc-superbrain-small-models) | model | Small-model collection used in superbrain experiments |
| [arc-agi-2-grids](https://huggingface.co/datasets/Nabidnur/arc-agi-2-grids) | dataset | ARC-AGI-2 grid datasets |
| [arc-agi-2-cot-sft](https://huggingface.co/datasets/Nabidnur/arc-agi-2-cot-sft) | dataset | Chain-of-thought SFT data for the ARC-2 solver |
| [arc-agi-2-synthetic-v1](https://huggingface.co/datasets/Nabidnur/arc-agi-2-synthetic-v1) | dataset | Synthetic augmentation set |
| [arc-agi-2-vision](https://huggingface.co/datasets/Nabidnur/arc-agi-2-vision) | dataset | Vision-format renderings of ARC tasks |
| [arc-agi-2-task-panels](https://huggingface.co/datasets/Nabidnur/arc-agi-2-task-panels) | dataset | Task panel images |
| [arc-agi-2-atlas-images](https://huggingface.co/datasets/Nabidnur/arc-agi-2-atlas-images) | dataset | Atlas-style visualizations |
| [arc-agi-2-solution-methods](https://huggingface.co/datasets/Nabidnur/arc-agi-2-solution-methods) | dataset | Solution-method annotations |
| [arc-agi-2-jepa-episodes](https://huggingface.co/datasets/Nabidnur/arc-agi-2-jepa-episodes) | dataset | JEPA-style episode data |
| [arc-agi-2-verifier-router](https://huggingface.co/datasets/Nabidnur/arc-agi-2-verifier-router) | dataset | Verifier/router training data |
| [arc-agi-2-multiformat](https://huggingface.co/datasets/Nabidnur/arc-agi-2-multiformat) | dataset | Multi-format task encodings |
| [arc-agi-2-solver-qwen3-4b](https://huggingface.co/Nabidnur/arc-agi-2-solver-qwen3-4b) | model | Qwen3-4B NVARC+ solver weights |

## 4. Kaggle — kernel lineage (team arc-needs-to-be-agi)

Scores are public-leaderboard values, API-verified Nov-02 2026. Kernel slugs link to the code page.

### Gold lane (dasshovon)

| Kernel | Score | Fired | Role in the story |
|---|---|---|---|
| [arc26-megafusion-v25-mount-heal](https://www.kaggle.com/code/dasshovon/arc26-megafusion-v25-mount-heal) | **35.53** | Nov-02 | **FINAL TEAM PB** — mount self-heal + gate matrix + S14 armor |
| [arc26-megafusion-v18b-cards-fd](https://www.kaggle.com/code/dasshovon/arc26-megafusion-v18b-cards-fd) | 32.31 | Nov-01 | first fully gate-armed fire; lineage PB +3.22 |
| [arc26-goldfusion-v16-d-prime](https://www.kaggle.com/code/dasshovon/arc26-goldfusion-v16-d-prime) | 31.09 / 28.93 | Oct-29/31 | the 0.00-streak breaker (v16) + its redraw |
| [arc26-megafusion-v17-motion-](https://www.kaggle.com/code/dasshovon/arc26-megafusion-v17-motion-tok) | 28.09 | Oct-30 | MOTION_TOK delta on the v16 chassis |
| [arc26-b-dprime-clean](https://www.kaggle.com/code/dasshovon/arc26-b-dprime-clean-v1) | **33.50** | Oct-09 | the D′ breakthrough; board best for 19 days |
| [arc26-b-apex-v11/-v13/-v14](https://www.kaggle.com/code/dasshovon/arc26-b-apex-v11) | 0.00 ×3 | Oct-26→28 | the apex gamble (failure museum, ch. 08) |

### Blackbox lane (koushikrudra)

| Kernel | Score | Fired | Role in the story |
|---|---|---|---|
| [arc3-eislab-s13-s14-k4s13-port](https://www.kaggle.com/code/koushikrudra/arc3-eislab-s13-s14-k4s13-port) | **33.86** / 30.38 / 30.86 / 28.74 / 31.98 / **32.94** | Oct-28 → Nov-02 | the eislab port: team PB + the 6-draw max-of-N farm |

### Constellation reference (Team Alicia — watched daily, not ours)

| Kernel | Score | Owner | Date |
|---|---|---|---|
| [arc3-hfx-15-original](https://www.kaggle.com/code/uradkr/arc3-hfx-15-original) | **36.89** | uradkr | Nov-01 |
| [arc3-franzen-m2-ours-v2](https://www.kaggle.com/code/gyuyoungpark09/arc3-franzen-m2-ours-v2) | 36.18 | gyuyoungpark09 | Oct-28 (now private; public forks: `juliancamilovilla/arc-agi3-franzen-m2`, `-s1`) |
| arc3-h3649-scout180 | 35.13 | uradkr | Oct-13 |
| [eislab-m2-st-s13-s14-k4s13](https://www.kaggle.com/code/leeheewon01/eislab-m2-st-s13-s14-k4s13) | 34.98 / 34.83 | leeheewon01 | Oct-24/26 (now private) |
| arc3-spx-recovery-1a7a68 | 36.49 | uradkr | Oct-16 (lineage PB) |

## 5. Where to read what

- New to the story → [`README.md`](README.md) then [`00-EXECUTIVE-SUMMARY.md`](00-EXECUTIVE-SUMMARY.md)
- Want the numbers → [`01-SCORE-LEDGER.md`](01-SCORE-LEDGER.md) + [`data/`](data/)
- Want the final week → [`11-ENDGAME-FINAL-WEEK.md`](11-ENDGAME-FINAL-WEEK.md)
- Want the methods → [`03-ARCHITECTURE.md`](03-ARCHITECTURE.md) + [`04-INNOVATIONS.md`](04-INNOVATIONS.md)
- Want the failures → [`08-GRAVES-AND-LESSONS.md`](08-GRAVES-AND-LESSONS.md)
