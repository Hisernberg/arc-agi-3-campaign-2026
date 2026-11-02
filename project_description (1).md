# Engineered Rerun Survival on ARC-AGI-3: Armor, Gates, and the Max-of-N Farm

**Team arc-needs-to-be-agi** — final best **35.53**, submission [57893187](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3/leaderboard), kernel [`arc26-megafusion-v25-mount-heal`](https://www.kaggle.com/code/dasshovon/arc26-megafusion-v25-mount-heal)

## Team Members

1. **Nabidnur Abrar** (`kragglenote2forwork`) — Leader
2. **Shovon Das** (`dasshovon`)

## Abstract

We document our ARC-AGI-3 solution: a CPU-only agent built around a house slot-priority allocator (D′), wrapped in rerun-survival armor, launched through fail-closed gates, and exploited through same-config redraws ("farming") under the leaderboard's max-of-N selection rule. Our central claim: the unsupervised ~9.9-hour rerun on locked hardware separates agent capability from agent survival, and under max-of-N selection the expected best score is dominated by survival probability and draw count before mean capability. Acting on it took the team best from 33.50 to 35.53 (submission 57893187) in the final week, zero GPU spend.

## 1. Introduction

![Figure 1. The score journey: 23–27 plateau → D′ 33.50 → apex 0.00s → 35.53](https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F29006516%2F12f425442c74ad15e64e38998d141b75%2Ffig01_score_journey.png?generation=1793632959621194&alt=media)

ARC-AGI-3 scores an agent on levels cleared across 30 hidden interactive games under a fixed action budget. Our campaign began with an M2S-derived harness scoring 23–27 — and one observation that reshaped everything: the Kaggle scoring rerun, not the games, produced every catastrophic failure; flawless interactive sessions reran to 0.00. We treat the rerun as a first-class adversary, and ask which capability moves the score, why proven armored code beats new architecture in the fire slot, and what variance implies under keep-the-max.

**Table 1 — Final results (all scores are leaderboard scores).**

| | |
|---|---|
| **Final team best (both lanes)** | **35.53** — `arc26-megafusion-v25-mount-heal`, ref 57893187, COMPLETE |
| Lane bests | gold 35.53 (prev 33.50) · blackbox 33.86 (Oct 28) |
| Top cluster at close | uradkr 36.89 · 36.18 · **ours 35.53** · eislab 34.98 |
| Honest gap | gold zone ≈38.98 — **3.45 points short** |

![Figure 2. 107 own-lane submissions, running best per lane, rerun deaths marked](UPLOAD__fig12_campaign_map)

## 2. Prior Work — the Campaign in Five Acts

![Figure 3. MEGAFUSION lineage ladder: 26.47 → 35.53](https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F29006516%2F2ab0aba4936da3aa5961dda4bdd19ae3%2Ffig02_lineage_ladder.png?generation=1793633230284616&alt=media)

**Act 1 — recon (Sep → Oct 4).** We entered with the M2S harness and one thesis: this is an *agent-harness* competition, not a model competition.

**Act 2 — the D′ breakthrough (Oct 9).** A clean re-derivation of the **D′ slot-priority allocator** broke the plateau: **33.50**, #106/4,799; every strong draw since runs a descendant.

**Act 3 — variance and the rerun war (Oct 10 → 25).** Same-config redraws spanned 27.8–33.5 — draw variance is the second-largest force after the allocator — while the rerun kept killing fires as 0.00s (§3.2).

**Act 4 — the apex gamble fails; the farm begins (Oct 26 → 28).** Three gold-lane fires of new-architecture code all landed **0.00**, while the second account's eislab S13/S14 armor-harness port drew **33.86** first try. The signal of the campaign: *new code dies in the rerun; proven code plus armor scores.*

**Act 5 — GOLDFUSION → MEGAFUSION (Oct 29 → Nov 2).** The gold lane was rebuilt on proven parts: v16 scored 31.09 and broke the 0.00 streak; final fires added the gate matrix (V0–V7) and mount self-heal (v25). Deadline day both slots fired — farm draw 7 (32.94) and v25 — and the rerun returned **35.53**.

The chassis grafts two public lines with credit: eislab S13/S14 (leeheewon01/eislab) contributes the keepalive-armor carrier; the franzen-m2 family (dfranzen, juliancamilovilla) contributes council grafts on a solved-level memory lineage (rellik13, sirikilohit); official baselines established the M2S loop. Everything else — D′, the gate matrix, mount self-heal, the farming discipline — is our own work, released with full ledgers.

## 3. Approach: Engine, Armor, Gates

![Figure 4. Flagship architecture: platform, armor, council, knowledge, engine, gates, scoring process](https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F29006516%2F021f687c6974d43ab742f2f73d9bb57e%2Ffig11_architecture.png?generation=1793633552811928&alt=media)

The v25 chassis is six layers: platform (Kaggle kernel, docker pin `57e612b484cf`, CPU-only), armor, pre-fire gates, the D′ engine, knowledge packs (game dossiers, mechanic taxonomy, dead-action ledger, transition priors), and a council of grafted harnesses weighted by UCB1 with an LLM veto.

### 3.1 The D′ slot-priority allocator

D′ allocates the action budget across game slots; for each candidate action it computes a priority blending five fail-open-guarded terms — level progress (level_pow 0.5, tail fade 0.4), efficiency (eff_const 300, eff_pow 2.5), pacing (pace_pow 0.4, pace_ref 30000), action and token waste (c_action 0.1, action_scale 115; c_token 0.9, token_scale 225000), and a linear floor (lin_floor 0.1, rel_pow 0.5) — inside budget bands (10/14/16). A stall-knee fold `priority *= max(0.1, 1/(1+(a-80)/40))` decays priority after 80 stalled actions. Every patch wraps the harness seam and falls back to proven behavior on any exception: a degraded run scores low, a crashed run scores 0.00.

![Figure 5. D′ allocator anatomy: the stall-knee fold and the five fail-open-guarded terms](UPLOAD__fig09_dprime_anatomy)

### 3.2 Armor: engineering for the rerun, not the arcade

Byte-pinned dependencies, an S14 keepalive heartbeat, a startup warmup reset, and — finally — mount self-heal: on input-mount failure the code re-locates the dataset by marker search instead of dying. Forensics on our rerun deaths (seven 0.00 rows, all Oct 22 → 28) attributed each to gateway/DNS patience failures, never agent logic — hence armor. The law we paid for: **patience is not armor** — retry loops without self-heal still die.

![Figure 6. Rerun survival: 7 deaths Oct 22→28; then 10 gated fires, zero deaths](UPLOAD__fig13_survival_timeline)

### 3.3 Gates: converting mystery into process

Before every fire, a V0–V7 matrix runs fail-closed: V0 syntax, V1 slot math, V2 true-slug resolution (fire the API-returned version, never a lineage tag), V3 runtime receipts, V4 armor present, V5 cap law, V6 CPU compile, V7 zero-drift spec review. The final fire passed all gates (gate report shipped).

![Figure 7. The v25 chassis as a component view](UPLOAD__fig05_architecture)

### 3.4 The max-of-N farm

One frozen config (the eislab S13/S14 port) was redrawn six times on the second account. The leaderboard keeps the maximum, so redrawing the best-mean config is a legitimate scoring strategy. It is also our cleanest variance measurement: same code, same seed policy, 5.1-point spread.

**Table 2 — Same-config farm draws (n=6, from `farm_draws.csv`).**

| Draw | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Score | 33.86 | 30.38 | 30.86 | 28.74 | 31.98 | 32.94 |

![Figure 8. Farm variance: six draws of one frozen config — mean 31.46, sd 1.85](https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F29006516%2F101ff821fad224485ab26510acf14e0b%2Ffig03_farm_variance.png?generation=1793633285644937&alt=media)

### 3.5 Why this works

The reward structure inflates zeros: a rerun death scores 0.00 regardless of agent quality, so leaderboard score ≈ **P(survive) × (mean capability + variance term)**, and under max-of-N selection the variance term enters once per draw. The model checks against the measured distribution: expected max of 6 draws ≈ 33.81 vs 33.86 observed (Table 2), and ≈ 34.68 at N=15. The apex gamble proves the survival factor negatively: three new-architecture fires 0.00'd while the proven chassis scored first try; the final version added mount self-heal to reach 35.53.

![Figure 9. Expected best-of-N: observed 33.86 matches the N=6 prediction 33.81](UPLOAD__fig10_farm_math)

## 4. Results and the Highest-Scoring Notebook, Evaluated

![Figure 10. Deadline day: gate matrix → two fires → 9.9-hour rerun → COMPLETE](UPLOAD__fig06_final_day_timeline)

All numbers are leaderboard scores, computed from our API-pulled ledger. After armor and gates went live (Oct 29 → Nov 2), **10 fires scored, zero rerun deaths** — versus seven before.

`arc26-megafusion-v25-mount-heal` — the 35.53 submission — is the proven-chassis composition: eislab S14 carrier (survival) + D′ allocator (skill) + council + mount self-heal (rerun insurance). Its evaluation: ALL-GREEN V0–V7 before fire; fired Nov 2 03:09 UTC as submission 57893187; survived a ~9.9-hour rerun and returned the team's best score — the fifth consecutive survivor. Its lineage is fully attributable, and its score matches the model in §3.5.

**Table 3 — The highest-scoring notebook against the official criteria.**

| Criterion | Evidence in this writeup |
|---|---|
| Accuracy | Table 1: 35.53, ref 57893187; the public notebook recomputes every number |
| Theory | §3.5: score ≈ P(survive) × (mean + variance), validated by expected-max math |
| Universality | Three transferable claims (§5) |
| Progress | The five-act record plus negative results |
| Completeness | Full architecture, exact D′ parameters, gate matrix, farm statistics, ledgers shipped |
| Novelty | D′ allocator, V0–V7 gate matrix, mount self-heal, farming as a measured process |

![Figure 11. Closing constellation: our 35.53 slot in the top cluster](UPLOAD__fig04_final_board)

![Figure 12. Variance lesson: redraw spread vs. architecture deltas](UPLOAD__fig07_variance_lesson)

![Figure 13. Verdict ratchet: the running best only moved up](UPLOAD__fig08_ratchet)

## 5. Conclusion

35.53 came from a CPU-only, two-account campaign whose decisive components were the validated D′ allocator, armor that treats the scoring rerun as the true adversary, a gate matrix that makes 0.00s fail closed before firing, and a farming discipline that exploits max-of-N selection. Transferable claims: (1) any rerun-scored agentic benchmark has a separate survival distribution that must be engineered for explicitly; (2) under keep-the-max selection, redraw variance of a proven config is a first-class scoring lever; (3) new architecture in a scarce fire slot is negative-EV late in a competition.

Full ledger: 107 own-lane submissions (57 gold, 50 blackbox; 90 scored), 13 figures, and machine-readable data accompany this writeup. Complete record: GitHub `Hisernberg/arc-agi-3-campaign-2026`; Hugging Face mirror `Nabidnur/arc-agi-3-campaign-2026`.
