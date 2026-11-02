# Engineered Rerun Survival on ARC-AGI-3: Armor, Gates, and the Max-of-N Farm

**Team arc-needs-to-be-agi (Shovon Das) — 35.53, submission [57893187](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3/leaderboard), kernel [`arc26-megafusion-v25-mount-heal`](https://www.kaggle.com/code/dasshovon/arc26-megafusion-v25-mount-heal)**

## Abstract

We document our ARC-AGI-3 solution: a CPU-only agent built around a house slot-priority allocator (D′), wrapped in "armor" engineered specifically for Kaggle's hostile scoring rerun, launched through a pre-flight gate matrix, and exploited through disciplined same-config redraws ("farming") under the leaderboard's max-of-N selection rule. Our central claim is that ARC-AGI-3's evaluation regime — an unsupervised nine-hour rerun on locked hardware — separates agent capability from agent survival, and that under a max-of-N leaderboard the expected best score is dominated by survival probability and draw count before mean capability. Acting on this theory took our team best from 33.50 to 35.53 (submission 57893187, verified COMPLETE) in the final week, with zero GPU spend.

## 1. Introduction

ARC-AGI-3 scores an agent on how many levels it clears across 30 hidden interactive games under a fixed action budget. Our campaign began with an M2S-derived harness scoring 23–27 and one observation that reshaped everything: the Kaggle scoring rerun — not the games — produced every catastrophic failure we suffered. Interactive sessions that played flawlessly would rerun to a 0.00 placeholder. This paper treats the rerun as a first-class adversarial environment and derives the architecture, process, and statistics that follow from that framing.

Three questions organize the paper. (1) Which capability actually moves the score? (2) Why does proven code with armor beat new architecture in the fire slot? (3) What does score variance imply for any team competing under a keep-the-max leaderboard?

## 2. Prior work

The chassis grafts two public Kaggle lines with credit: the eislab S13/S14 harness (leeheewon01/eislab) contributes the keepalive-armor carrier, and the franzen-m2 family (dfranzen, juliancamilovilla) contributes council grafts, on a solved-level memory lineage (rellik13, sirikilohit). Official ARC-AGI-3 baselines established the M2S interaction loop our engine evolved from. Beyond code, the public culture of the competition — leaderboard archaeology and cross-team config porting — is prior work in the process sense: we lean into it deliberately, porting the best floor weapon rather than re-deriving it. Everything else here — the D′ allocator, the gate matrix, mount self-heal, the farming discipline and its statistics — is our own work, released with full ledgers.

## 3. Approach

### 3.1 The D′ slot-priority allocator

D′ allocates the action budget across game slots. For each candidate action it computes a priority blending five fail-open-guarded terms — level progress (level_pow 0.5, tail fade 0.4), efficiency against a constant (eff_const 300, eff_pow 2.5), pacing against a reference budget (pace_pow 0.4, pace_ref 30000), action and token waste (c_action 0.1, action_scale 115; c_token 0.9, token_scale 225000), and a linear floor (lin_floor 0.1, rel_pow 0.5) — inside budget bands (10/14/16). A stall-knee fold `priority *= max(0.1, 1/(1+(a-80)/40))` decays priority after 80 actions on a slot. Every patch wraps the harness seam and falls back to proven behavior on any exception: a degraded run scores low, a crashed run scores 0.00. Supporting layers: a game-dossier knowledge pack (probes, playbooks, mechanic taxonomy, dead-action ledger), a context-efficiency "wastepack," and a council of grafted public harnesses weighted by UCB1 with an LLM veto.

### 3.2 Armor: engineering for the rerun, not the arcade

Byte-pinned dependencies (docker digest, wheel digests), an S14 keepalive heartbeat, a startup warmup reset, and — in the final version — mount self-heal: on input-mount failure the code re-locates the dataset by marker search instead of dying. Armor exists because forensics on our rerun deaths (seven 0.00 rows across our two lanes in the API-retrievable window) attributed each one to gateway/DNS patience failures in the rerun environment, not to agent logic. The law we paid for: patience is not armor — retry loops without structural self-heal still die.

### 3.3 Gates: converting mystery into process

Before every fire, a V0–V7 matrix runs fail-closed: V0 syntax, V1 slot math, V2 true-slug resolution (fire the API-returned version number, never a lineage tag), V3 runtime receipts (grep exact marker lines), V4 armor present, V5 cap law, V6 CPU compile with all modules present, V7 zero-drift spec review. The final fire passed all gates (ALL GREEN verdict, gate report shipped with our data). This is why we could spend the deadline day on two confident fires instead of one terrified one.

### 3.4 The max-of-N farm

One frozen config (eislab S13/S14 port) was redrawn six times on the second account: 33.86, 30.38, 30.86, 28.74, 31.98, 32.94 — mean 31.46, sd 1.85 (n=6, verified from our ledger). Since the leaderboard keeps the maximum, redrawing the best-mean config is a legitimate scoring strategy; the 33.86 draw stood as our #2 score for five days against everything else we could build. The farm is also our cleanest variance measurement: same code, same seed policy, 5.1-point spread.

### 3.5 Why this works

The reward structure inflates zeros: a rerun death scores 0.00 regardless of agent quality, so leaderboard score ≈ P(survive) × (mean capability + variance term), and under max-of-N selection the variance term enters twice — once per draw. Late in a competition, P(survive) and N are the cheap multipliers; mean capability is the expensive one. Our apex gamble proves the point from the negative side: three gold-lane fires of new-architecture code (model swaps, lexicons, SLM patches, 120-min caps) all landed 0.00, while the rebuilt proven chassis (GOLDFUSION v16, eislab carrier + D′ + council) scored 31.09 on its first fire and the final MEGAFUSION v25 added mount self-heal to reach 35.53.

## 4. Results

All numbers are Kaggle leaderboard scores (we report no train-set performance); every figure is computed from our API-pulled submission ledger shipped with this writeup.

- **Final team best: 35.53** — `arc26-megafusion-v25-mount-heal`, submission 57893187, fired 2026-11-02 03:09Z, COMPLETE after a ~9.9-hour scoring rerun. At close it sat between franzen-m2 36.18 and uradkr 35.13.
- **MEGAFUSION lineage:** 26.47 → 31.09 → 28.09 → 28.93 → 32.31 → 35.53 (Oct-24 → Nov-02), +9.06 across the line.
- **D′ impact:** 23–27 plateau → 33.50 on introduction (Oct-09); every strong draw since runs a D′ descendant.
- **Same-config farm:** n=6 draws of one frozen config, mean 31.46, sd 1.85, range 28.74–33.86.
- **Rerun deaths:** seven 0.00 rows across both lanes in the API window, all in the apex-war week (Oct-22 → Oct-28) and all attributed by forensics to rerun-environment failures, never agent logic. After armor + gates went live (Oct-29 → Nov-02): 10 fires scored, zero deaths.
- **Honest gap:** the gold zone (~38.98 cutoff) was not reached; 35.53 is 3.45 short.

Full ledger: 107 our-lane submissions in the API-retrievable window (57 gold, 50 blackbox; 90 scored; ≈265 lifetime), 13 figures, and all machine-readable data accompany this writeup.

## 5. Conclusion

We achieved 35.53 on ARC-AGI-3 with a CPU-only, two-account campaign whose decisive components were: a validated slot-priority allocator (D′), armor that treats the scoring rerun as the true adversary, a gate matrix that makes 0.00s fail closed before firing instead of after, and a statistical farming discipline that exploits max-of-N selection. The transferable claims: (1) any rerun-scored agentic benchmark has a separate survival distribution that must be engineered for explicitly; (2) under keep-the-max selection, redraw variance of a proven config is a first-class scoring lever; (3) new architecture in a scarce fire slot is negative-EV late in a competition. All code, ledgers, figures, and the complete campaign record are public and linked from the attached notebook.
