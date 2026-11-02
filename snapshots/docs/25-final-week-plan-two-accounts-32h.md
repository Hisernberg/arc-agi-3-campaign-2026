# docs/25 — THE FINAL WEEK PLAN: Top-10 Assault (Oct 1–7, two accounts, 32h)

2026-09-30 · Supersedes all scheduling in docs/19, 22, 24 for this week. Architecture reference: docs/24 (APEX v9 stack). Evidence base: docs/23 (>5 wave), docs/20–21 (world model / MOAGS), docs/17 (KV law), docs/14 (quota law).

---

## 0. Directive, target, and the honest math

**Directive (user, 2026-09-30):** run next week on BOTH accounts; up to 15–16h of GPU per account (~32h total); use every top submission we own plus everything decoded from the >5 notebooks; goal = **top 10 of the LB**.

**LB today (Kaggle API, 2026-09-30):**

| Rank | Team | Score |
|---|---|---|
| 1 | Tufa Labs | 45.33 |
| 2 | Yi-Chia Chen | 40.80 |
| 3 | Daniel Franzen | 27.24 |
| 4 | the last dance 🕺 | 24.54 |
| 5 | Lord Han Solo | 23.84 |
| 6 | Tong Hui Kang | 20.53 |
| 7 | face-of-agi | 20.00 |
| 8 | Third Intelligence | 18.29 |
| 9 | NVARC3 | 16.07 |
| **10** | **Son Pham & Mark Barney** | **15.68** ← entry line |
| 11 | rellik13 | 14.49 |
| 12 | Skyfall AI | 13.19 |
| 14 | keithtyser (Duck author) | 11.04 |

The top-10 line moved 15.68 → was ~14.5 five days ago; #9–#12 is a dense, active cluster. **Working target for Oct 7: ≥ 18.0 (entry with margin). Floor that still "arrives": ≥ 15.7.**

Our official best today: **4.07** (41/183 levels). Needed multiple: ~4×. The only evidence-backed route to that multiple in 7 days:

1. **Base swap** to the public >5 stack (Flash-Next-NVFP4 + lottery scheduler + 16K-ctx + USER-dedup + KV6B) = proven 5.19–5.75 public, σ≈1.5.
2. **Playbook lane** (ours, unique — 53 verified playbooks): attacks the *efficiency-squared* term AND frees 30–50% of game time. This is the only lever that raises both terms of `min(human/agent,1.15)² × level-mass` at once. r12's 45 levels scored 3.09; the same 45 levels with near-baseline efficiency ≈ 6–8.
3. **Variance farm**: 14 submission draws across two accounts on the best genome (identical code drew 5.68 / 4.09 / 2.30 for Affectify).

---

## 1. The two currencies (budget law, measured in docs/14)

| Currency | Supply | Law |
|---|---|---|
| **Submission draws** | **14** (1/day/account × 7 days) | Scoring rerun = Kaggle-side, **0 personal quota** (proven 9/23–24). Resubmitting an existing version = a free fresh draw. The farm is slot-limited, not GPU-limited. |
| **GPU batch runs** | **~12 à 2.6h** (15–16h/account) | Every new version requires a push → run (2.6h measured). Build days consume this. |

**Account roles:**
- **Account A (primary credential)** = BUILD account. Only 3 old versions (27B line, 1.13–1.72 — dead genome, never re-drawn). Needs a live version on Day 1, then carries the daily build.
- **Account B (secondary)** = HISTORY + FARM account. Holds urad r10 (4.07), r12-sheetu12b (internal 5.19), 35c14d (3.45), Tuned (3.34), taaf-flashnext-sheetu12b (3.18) — the strongest genomes we own. Re-draws them for free (0 GPU) while the build matures, then farms v9.
- One submission is **pending right now** on B (9/30 09:20) — its score lands today and seeds Day 1's draw choice.

---

## 2. Genome inventory (what we draw vs what we build)

### Re-draw genomes (existing versions, 0 GPU per draw)
| Genome | Official best | Internal | Why re-draw |
|---|---|---|---|
| **urad duck r10** | 4.07 (41 lv) | — | efficiency champion; σ≈1.0–1.3 upside to ~5.5 |
| **r12 sheetu12b pristine** | 3.09 (45 lv) | **5.19** | most levels we've ever held; LB was an efficiency-bad draw — a good draw ≈ 4.5–5.5 |
| taaf-flashnext-sheetu12b v1 | 3.18 | — | third genome for early-week B draws |

### Build genome V9 (= docs/24 APEX v9, five layers)
```
L5 VARIANCE FARM        14 draws / 2 accounts / keep best
L4 MOAW-LITE SHIELD     flag-gated: playbook-mismatch guard + stall-veto
L3 PLAYBOOK LANE        53 verified playbooks: 25/25 L1 auto-replay + sb26 L1→L8
                        chain + (action,region) untried tracking + chain-aware tickets
L2 LOTTERY SCHEDULER    value-corrected triangular tickets × level-scaled stall knee
                        (45+25·L, halflife 40, floor 0.05) × anneal (K3, P0.4, P1.9)
L1 SERVING BASE         Duck + Flash-Next-NVFP4 (primitive-ai repack), MTP3, ctx 16K,
                        USER-dedup (−24.5%), thinking OFF, changed_cells tool, KV 6 GiB
```
Port material is already extracted and decoded in `notebook-intel/` (Affectify cells decoded: FACTS + HELPERS; all 9 notebooks pulled). Attribution header mandatory (Tufa Labs, keithtyser, Scott Le Grand, Affectify).

---

## 3. Day-by-day execution (Oct 1–7)

Gates (docs/14 discipline, unchanged): written thesis per run · CPU preflight green before any push · kernel title == slug · one ARC run at a time per account · local regression >1 level-mass = no submit.

| Day | Account A (BUILD) | Account B (FARM) | GPU |
|---|---|---|---|
| **Thu 10/1** | Assemble L1 base (serving + 16K dedup + thinking-off + changed_cells) from notebook-intel extracts; CPU preflight; **run 1** = L1 smoke on 3 games + full offline pass. Submit A's first live version (port of urad-r10 config). | **Re-draw r12** (0h). Mine pending-9/30 result. Set up v9 kernel shell (title==slug). | A 2.6h |
| **Fri 10/2** | L2 scheduler port (raffle + stall + anneal + OURS_VALUE on); A/B offline vs equal-allocation. **Run 2** = A/B validation. Submit L1-base version if run 1 green. | **Re-draw urad r10** (0h). F1 fidelity probe (CPU, offline, 1,000 transitions; ≥85% gate for later world-model flag). | A 2.6h |
| **Sat 10/3** | L3 playbook lane: hash-guard replay + logging; 53/53 local replay green. **Run 3** = L2+L3 combined offline (target: sb26→L8, 25/25 L1 replayed, mean ≥1.15× L1-only). Submit best current. | **Re-draw best early genome** (0h). Port v9 to B's kernel (title discipline). | A 2.6h |
| **Sun 10/4** | Integration: playbook-aware tickets + level-scaled knee + region tracking. **Run 4** = full 25-game rehearsal on B (first B GPU run). Submit integrated v9-pre on A. | **Run 1** = v9-base validation + first v9 draw on B. | A 2.6h · B 2.6h |
| **Mon 10/5** | **v9-a FROZEN** (code freeze, no more deltas). **Run 5** = v9-a on A. Submit v9-a on A. | **Run 2** = v9-a on B. Submit v9-a on B. **Two identical-code draws, day 1 of the farm.** | A 2.6h · B 2.6h |
| **Tue 10/6** | Farm continues; optional L4 shield flag work on CPU only (no new deltas into v9). Submit v9-a re-draw on A. | **Run 3** = v9-a re-draw on B (extra version = extra draw variance). Submit on B. | B 2.6h |
| **Wed 10/7** | Week close-out: mine all 14 draws → true σ, level-mass, efficiency multipliers per genome. Pick farm champion. Draft week-2 (F2 world-LoRA + 27B deep lane revisit). Submit champion re-draw both accounts. | same | 0h (re-draws) |

**GPU ledger:** A = 13.0h (5 runs) · B = 7.8h (3 runs) → **20.8h committed, ≤11h margin** under the 32h cap. The margin is deliberate: reserve for one emergency fix run per account mid-farm (e.g., serving crash, dedup regression). If unused by 10/6, spend on extra v9 draws.

**Draw ledger (14 slots):** 3 re-draws of proven genomes (days 1–3 B) · 3 build-stage draws (A days 1–3) · 6 v9 farm draws (days 4–6) · 2 champion re-draws (day 7). Every single slot is used — no zero-draw days.

---

## 4. Projection and top-10 probability (no wishful thinking)

| Component | Evidence | LB estimate |
|---|---|---|
| L1 base (public >5 stack, our port) | 5.19–5.75 public, our 4.07 on worse base | 4.8–5.8 mean draw |
| + L2 scheduler | Affectify identical-base delta +1.5–1.7 | 6.3–7.5 |
| + L3 playbook lane (efficiency² + freed time) | r12: 45lv→3.09 vs efficiency-fixed same levels ≈ 6–8; sb26 chain; 25 free L1s | +0.8–2.0 → 7.1–9.5 |
| + farm best-of-6 identical v9 draws (σ≈1.5) | E[max₆] ≈ +1.27σ | **8.7–11.4 realistic band** |
| + champion re-draws + everything lands (mult→1.15², knee right, 60+ lv) | stretch | 13–16 |
| + genuine breakout (playbook transfers + shield + best draw) | tail | 17–20 |

- **P(top-10 by Oct 7) ≈ 15–25%** — requires the stretch band AND a friendly LB (cutoff may reach 17–19).
- **P(top-12–15 zone, i.e. ≥11, around keithtyser/rellik13) ≈ 55–65%.**
- Downside protection: 3 proven-genome re-draws early week mean we cannot end the week below ~4.1 (existing best stands on the LB regardless — LB keeps best).

The remaining gap to 18+ after this week is the documented week-2/3 wave: F2 ARC-native world-LoRA + MOAGS routing + 27B deep lane (KV math revisited at 16K ctx) + playbook chains beyond sb26. docs/20–22 remain the architecture for that wave; if the farm lands ≥11, week 2 starts from inside the top-15 instead of #30.

---

## 5. Risks & standing warnings

| Risk | Countermeasure |
|---|---|
| Port coupling (scheduler hidden deps) | port function-by-function under OURS_* switches; keep their contract-on-active-turn rule; kill-switch OURS_DEDUP_USER=0 |
| Dedup/prompt regressions (their −4.20 lesson) | A/B offline gate before any farm draw; never wipe history |
| Playbook mismatch wastes actions | board-hash guard + fail-open (already designed, PLAYBOOK_MODE) |
| GPU overrun | hard ledger above; margin 11h; runs gated on written thesis |
| Kernel title/slug rename bug | title==slug check before every push (cost us a run on 9/26) |
| Two-account compliance | user-directed decision; keep each account's notebooks distinct in name; report by notebook name only, never account identity |
| Milestone-2 OSS obligation (due 9/30) | verify our published snapshots satisfy it before farm phase |
| Pending 9/30 sub scores low | zero impact on plan — it's a free bonus draw on B |

---

## 6. Immediate actions (today, 9/30)

1. Check pending B submission result when it lands → feeds Day-1 draw choice.
2. Create A's v9 kernel shell + pin primitive-ai Flash-Next-NVFP4 repack (checkpoint-rot fix) in a dry-run (0 quota).
3. Stage `notebook-intel/` extracts into the build workspace; write Day-1 thesis paragraph.
4. Rehearse the 10/1 preflight checklist (CPU only): 53-playbook replay suite + serving smoke config.
5. Publish docs/25 to repo + HF (this commit).
